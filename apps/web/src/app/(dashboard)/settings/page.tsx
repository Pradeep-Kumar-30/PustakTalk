import Link from "next/link";
export default function SettingsPage() { return <main className="grid min-h-screen place-items-center bg-[var(--paper)]"><div className="text-center"><p className="eyebrow">Settings</p><h1 className="display mt-2 text-4xl text-[var(--navy)]">Local model settings live on the server.</h1><p className="mt-3 text-[var(--slate)]">Configure models and storage through the deployment environment.</p><Link className="mt-6 inline-block font-bold text-[var(--orange-deep)]" href="/dashboard">Back to dashboard</Link></div></main>; }

