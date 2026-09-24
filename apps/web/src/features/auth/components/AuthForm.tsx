"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { BookOpenText } from "lucide-react";
import { login, register } from "@/features/auth/api/auth";
import { Button } from "@/components/ui/Button";

export function AuthForm({ mode }: { mode: "login" | "register" }) {
  const router = useRouter();
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);
  const isRegister = mode === "register";

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError(""); setPending(true);
    const form = new FormData(event.currentTarget);
    try {
      if (isRegister) await register({ email: String(form.get("email")), password: String(form.get("password")), display_name: String(form.get("name")) });
      else await login({ email: String(form.get("email")), password: String(form.get("password")) });
      router.push("/dashboard");
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Could not sign you in"); }
    finally { setPending(false); }
  }

  return <main className="grid min-h-screen place-items-center bg-[#f6f6f1] p-6"><section className="w-full max-w-md rounded-3xl border border-[var(--line)] bg-white p-8 shadow-xl shadow-slate-200/50"><Link href="/" className="flex items-center gap-2 font-bold text-[var(--navy)]"><span className="grid h-9 w-9 place-items-center rounded-xl bg-[var(--navy)] text-white"><BookOpenText size={18}/></span>PustakTalk</Link><p className="eyebrow mt-10">Your private library</p><h1 className="display mt-2 text-4xl text-[var(--navy)]">{isRegister ? "Begin a better study session." : "Welcome back."}</h1><p className="mt-3 text-sm leading-6 text-[var(--slate)]">{isRegister ? "Create your account to keep every source and conversation in one place." : "Pick up exactly where you left off."}</p><form onSubmit={submit} className="mt-7 grid gap-4">{isRegister && <label className="grid gap-1.5 text-sm font-semibold">Name<input required name="name" className="focus-ring rounded-xl border border-[var(--line)] px-3 py-2.5 font-normal" placeholder="Your name"/></label>}<label className="grid gap-1.5 text-sm font-semibold">Email<input required type="email" name="email" className="focus-ring rounded-xl border border-[var(--line)] px-3 py-2.5 font-normal" placeholder="you@example.com"/></label><label className="grid gap-1.5 text-sm font-semibold">Password<input required minLength={isRegister ? 12 : 1} type="password" name="password" className="focus-ring rounded-xl border border-[var(--line)] px-3 py-2.5 font-normal" placeholder={isRegister ? "At least 12 characters" : "Your password"}/></label>{error && <p role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}<Button disabled={pending} type="submit">{pending ? "Please wait…" : isRegister ? "Create account" : "Sign in"}</Button></form><p className="mt-6 text-center text-sm text-[var(--slate)]">{isRegister ? "Already have an account?" : "New to PustakTalk?"} <Link className="font-bold text-[var(--orange-deep)]" href={isRegister ? "/login" : "/register"}>{isRegister ? "Sign in" : "Create one"}</Link></p></section></main>;
}

