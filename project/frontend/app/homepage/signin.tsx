import React, {useState} from 'react';
import "./page.module.css"
import {useAuth} from "@/lib/auth";
import Field from "@/app/components/fields"
import styles from "./page.module.css";
import {useRouter} from "next/navigation";

export default function LoginForm({ onClose, onSwitch }: { onClose: () => void; onSwitch: () => void }) {
    const { login } = useAuth();
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [busy, setBusy] = useState(false);
    const [emailBlurred, setEmailBlurred] = useState(false);
    const [pwBlurred, setPwBlurred] = useState(false);

    const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

    const emailState = (): "default" | "error" | "success" => {
        if (emailBlurred && !email) return "error";
        if (!email) return "default";
        return emailValid ? "success" : "error";
    };

    const handleSubmit = async () => {
        setEmailBlurred(true);
        setPwBlurred(true);
        setError("");
        if (!emailValid || !password) return;
        setBusy(true);
        try {
            await login(email, password);
            onClose();
            router.push("/recipeFinder");
        } catch {
            setError("E-Mail oder Passwort falsch.");
        } finally {
            setBusy(false);
        }
    };

    return (
        <div>
            <h2 className={styles.title}>Anmelden</h2>
            <p className={styles.subtitle}>Willkommen zurück! Melden Sie sich an, um fortzufahren.</p>
            {error && <p className={styles.error}>{error}</p>}
            <Field label="Email" type="email" value={email} onChange={(v: string) => { setEmail(v); if (emailBlurred) setEmailBlurred(false); }} placeholder="Email" onBlur={() => setEmailBlurred(true)} state={emailState()} />
            <Field label="Password" type="password" value={password} onChange={setPassword} placeholder="••••••••" onKeyDown={(e: React.KeyboardEvent) => e.key === "Enter" && handleSubmit()} onBlur={() => setPwBlurred(true)} state={pwBlurred && !password ? "error" : "default"} />
            <button className={styles.btn} disabled={busy} onClick={handleSubmit}>
                {busy ? "Wird geladen…" : "Anmelden"}
            </button>
            <p className={styles.switchText}>
                Noch kein Konto?{" "}
                <button className={styles.switchBtn} onClick={onSwitch}>Registrieren</button>
            </p>
        </div>
    );
}