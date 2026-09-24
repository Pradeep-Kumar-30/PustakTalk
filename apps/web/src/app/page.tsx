import Link from "next/link";
import { ArrowRight, BookOpenText, Mic, Quote } from "lucide-react";

const promises = [
  ["Page-true answers", "Each source chip carries the page and source passage behind it."],
  ["Your language, naturally", "Ask in Hindi, English, or the Hinglish you actually use."],
  ["Private by design", "Run the language model, embeddings, speech, and documents on your own infrastructure."],
];

export default function HomePage() {
  return (
    <main className="shell grain overflow-hidden">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6 lg:px-10">
        <Link href="/" className="flex items-center gap-2 font-bold tracking-tight text-[var(--navy)]">
          <span className="grid h-9 w-9 place-items-center rounded-xl bg-[var(--navy)] text-white"><BookOpenText size={19} /></span>
          PustakTalk
        </Link>
        <div className="flex items-center gap-5 text-sm font-semibold text-[var(--slate)]">
          <Link href="#how">How it works</Link>
          <Link href="/login" className="hidden sm:block">Sign in</Link>
          <Link href="/register" className="rounded-full bg-[var(--navy)] px-4 py-2 text-white">Start free</Link>
        </div>
      </nav>

      <section className="mx-auto grid max-w-7xl gap-14 px-6 pb-24 pt-14 lg:grid-cols-[1.05fr_.95fr] lg:px-10 lg:pb-32 lg:pt-24">
        <div className="max-w-2xl">
          <p className="eyebrow">Document intelligence, without the guessing</p>
          <h1 className="display mt-5 text-5xl leading-[.96] text-[var(--navy)] sm:text-6xl lg:text-7xl">अपनी किताबों से <em className="text-[var(--orange)]">बात</em> कीजिए।</h1>
          <p className="mt-6 max-w-xl text-lg leading-8 text-[var(--slate)]">Talk to your documents. Find answers. Hear them. See the source. PustakTalk makes research feel less like searching and more like a real conversation.</p>
          <div className="mt-9 flex flex-wrap gap-3">
            <Link href="/register" className="focus-ring inline-flex items-center gap-2 rounded-full bg-[var(--orange)] px-6 py-3 font-bold text-white shadow-lg shadow-orange-200 transition hover:bg-[var(--orange-deep)]">Open your library <ArrowRight size={18} /></Link>
            <a href="#how" className="focus-ring rounded-full border border-[var(--line)] bg-white px-6 py-3 font-semibold text-[var(--navy)]">See how it works</a>
          </div>
          <p className="mt-5 text-sm text-[var(--slate)]">Built for notes, textbooks, papers, and very curious students.</p>
        </div>

        <div className="relative mx-auto w-full max-w-xl">
          <div className="absolute -inset-6 -rotate-3 rounded-[2.2rem] bg-[#dcece4]" />
          <div className="relative overflow-hidden rounded-[1.8rem] border border-white/80 bg-[var(--cream)] p-4 shadow-2xl shadow-slate-300/50">
            <div className="flex items-center gap-2 border-b border-[var(--line)] pb-3 text-xs font-semibold text-[var(--slate)]"><span className="h-2 w-2 rounded-full bg-[#f6a56e]"/><span className="h-2 w-2 rounded-full bg-[#f2d469]"/><span className="h-2 w-2 rounded-full bg-[#8ccbb4]"/><span className="ml-2">Computer Networks.pdf</span></div>
            <div className="grid min-h-[330px] grid-cols-[1fr_1.1fr] gap-4 pt-4 text-sm">
              <div className="rounded-xl bg-[#f2f0e9] p-4 text-[var(--slate)]"><p className="font-bold text-[var(--navy)]">Chapter 3</p><p className="mt-4 leading-7">Congestion control is a mechanism used to regulate data transmission...</p><div className="mt-8 h-2 w-4/5 rounded bg-[#dad6ca]"/><div className="mt-2 h-2 w-3/5 rounded bg-[#dad6ca]"/></div>
              <div className="flex flex-col justify-end rounded-xl bg-[var(--navy)] p-4 text-white"><span className="mb-auto grid h-9 w-9 place-items-center rounded-full bg-white/10"><Mic size={17}/></span><p className="font-medium text-white/65">You asked</p><p className="mt-1 font-semibold">“Slow Start simple language me samjhao.”</p><div className="mt-4 rounded-lg bg-white/10 p-3 text-sm leading-6">It begins cautiously, then the sending rate grows fast until the network signals congestion.</div><p className="mt-3 inline-flex items-center gap-1 text-xs text-[#ffbd8b]"><Quote size={13}/> Computer Networks — p. 37</p></div>
            </div>
          </div>
        </div>
      </section>

      <section id="how" className="border-y border-[var(--line)] bg-white/60 py-16">
        <div className="mx-auto max-w-7xl px-6 lg:px-10"><p className="eyebrow">A calmer research workflow</p><div className="mt-7 grid gap-7 md:grid-cols-3">{promises.map(([title, body], index) => <article key={title} className="rounded-2xl border border-[var(--line)] bg-white p-6"><span className="text-2xl font-bold text-[var(--orange)]">0{index + 1}</span><h2 className="mt-7 text-lg font-bold text-[var(--navy)]">{title}</h2><p className="mt-3 leading-7 text-[var(--slate)]">{body}</p></article>)}</div></div>
      </section>
    </main>
  );
}
