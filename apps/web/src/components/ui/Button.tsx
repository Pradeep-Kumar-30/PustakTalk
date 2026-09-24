import type { ButtonHTMLAttributes, ReactNode } from "react";

export function Button({ children, className = "", ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { children: ReactNode }) {
  return <button className={`focus-ring inline-flex items-center justify-center gap-2 rounded-xl bg-[var(--navy)] px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-[#24395d] disabled:cursor-not-allowed disabled:opacity-50 ${className}`} {...props}>{children}</button>;
}

