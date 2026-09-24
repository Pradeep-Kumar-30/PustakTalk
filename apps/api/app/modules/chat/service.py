from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.orm import Session

from app.ai.agents.graph import resolve_intent
from app.ai.agents.nodes.page_locator import PageLocator
from app.ai.embeddings.factory import get_embedding_provider
from app.ai.llm.factory import get_llm_provider
from app.ai.rag.answer_generator import AnswerGenerator
from app.ai.rag.citation_validator import validate_citations
from app.ai.rag.context_builder import build_context
from app.ai.rag.groundedness import has_sufficient_grounding
from app.ai.rag.pipeline import RagPipeline
from app.ai.reranking.factory import get_reranker
from app.ai.retrieval.dense import DenseRetriever
from app.ai.retrieval.hybrid import HybridRetriever
from app.ai.retrieval.lexical import LexicalRetriever
from app.core.config import Settings
from app.core.exceptions import NotFoundError
from app.infrastructure.vectorstore.qdrant import QdrantVectorStore
from app.modules.chat.models import Citation, Message
from app.modules.chat.repository import ChatRepository
from app.modules.chat.schemas import ChatRequest
from app.modules.conversations.memory import compact_memory
from app.modules.conversations.models import Conversation
from app.modules.conversations.repository import ConversationRepository
from app.modules.documents.repository import DocumentRepository
from app.modules.workspaces.service import WorkspaceService
from app.shared.enums import Intent, MessageRole
from app.shared.types import ChunkEvidence


@dataclass(frozen=True, slots=True)
class ChatResult:
    conversation: Conversation
    message: Message
    intent: Intent
    answer: str
    citations: list[Citation]
    grounded: bool


class ChatService:
    def __init__(self, session: Session, settings: Settings, enable_reranker: bool = True) -> None:
        self._session = session
        self._settings = settings
        self._conversations = ConversationRepository(session)
        self._chat = ChatRepository(session)
        self._documents = DocumentRepository(session)
        self._workspaces = WorkspaceService(session)
        dense = DenseRetriever(
            get_embedding_provider(),
            QdrantVectorStore(
                str(settings.qdrant_url), settings.qdrant_collection, settings.embedding_dimension
            ),
        )
        reranker = get_reranker() if enable_reranker and settings.enable_reranker else None
        self._rag = RagPipeline(
            HybridRetriever(dense, LexicalRetriever(self._documents)), self._chat, reranker
        )
        self._answers = AnswerGenerator(get_llm_provider())

    def respond(self, owner_id: UUID, payload: ChatRequest) -> ChatResult:
        self._workspaces.require_owned(payload.workspace_id, owner_id)
        conversation = self._resolve_conversation(owner_id, payload)
        intent = resolve_intent(payload.question)
        self._chat.add_message(
            Message(
                conversation_id=conversation.id,
                role=MessageRole.USER.value,
                content=payload.question,
                intent=intent.value,
                metadata_json={"selected_text": payload.selected_text.model_dump(mode="json")}
                if payload.selected_text
                else None,
            )
        )
        recent = self._conversations.recent_messages(conversation.id)
        memory = compact_memory(conversation.summary, recent)
        allowed_ids = set(payload.document_ids) if payload.document_ids else None
        query = self._query_with_selected_text(payload, memory)
        evidence = self._rag.retrieve(query, payload.workspace_id, allowed_ids)
        answer = self._answer(intent, payload.question, memory, evidence)
        verified_evidence = validate_citations(evidence)
        assistant_message = self._chat.add_message(
            Message(
                conversation_id=conversation.id,
                role=MessageRole.ASSISTANT.value,
                content=answer,
                intent=intent.value,
            )
        )
        citations = self._chat.persist_citations(assistant_message.id, verified_evidence)
        self._session.commit()
        self._session.refresh(assistant_message)
        return ChatResult(
            conversation=conversation,
            message=assistant_message,
            intent=intent,
            answer=answer,
            citations=citations,
            grounded=has_sufficient_grounding(answer, verified_evidence),
        )

    def _resolve_conversation(self, owner_id: UUID, payload: ChatRequest) -> Conversation:
        if payload.conversation_id:
            conversation = self._conversations.get_owned(
                payload.conversation_id, payload.workspace_id, owner_id
            )
            if not conversation:
                raise NotFoundError("Conversation not found")
            return conversation
        return self._conversations.add(
            Conversation(
                workspace_id=payload.workspace_id, user_id=owner_id, title=payload.question[:120]
            )
        )

    @staticmethod
    def _query_with_selected_text(payload: ChatRequest, memory: str) -> str:
        parts = [payload.question]
        if payload.selected_text:
            parts.append(f"Selected source text: {payload.selected_text.text}")
        if memory:
            parts.append(f"Recent conversation context: {memory[-1500:]}")
        return "\n".join(parts)

    def _answer(
        self, intent: Intent, question: str, memory: str, evidence: list[ChunkEvidence]
    ) -> str:
        if intent is Intent.PAGE_SEARCH:
            return PageLocator().answer(question, evidence)
        return self._answers.generate(question, memory, build_context(evidence), evidence)
