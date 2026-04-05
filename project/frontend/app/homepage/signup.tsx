import React, {useState} from 'react';
import "./page.module.css"
import {useAuth} from "@/lib/auth";
import Field from "@/app/components/fields"
import styles from "./page.module.css";
import {useRouter} from "next/navigation";


function PasswordChecklist({ password }: { password: string }) {
    const rules = [
        { label: "Mindestens 8 Zeichen", pass: password.length >= 8 },
        { label: "Ein Großbuchstabe (A–Z)", pass: /[A-Z]/.test(password) },
        { label: "Ein Kleinbuchstabe (a–z)", pass: /[a-z]/.test(password) },
        { label: "Eine Zahl (0–9)", pass: /[0-9]/.test(password) },
        { label: "Ein Sonderzeichen (!@#$%…)", pass: /[^A-Za-z0-9]/.test(password) },
    ];

    return (
        <ul className={styles.checklist}>
            {rules.map((r) => (
                <li key={r.label} className={`${styles.checkItem} ${r.pass ? styles.checkPass : styles.checkFail}`}>
                    {r.pass ? "✓" : "○"} {r.label}
                </li>
            ))}
        </ul>
    );
}

export default function RegisterForm({ onClose, onSwitch }: { onClose: () => void; onSwitch: () => void }) {
    const { register } = useAuth();
    const router = useRouter();
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [busy, setBusy] = useState(false);
    const [submitFailed, setSubmitFailed] = useState(false);
    const [serverError, setServerError] = useState("");
    const [emailTaken, setEmailTaken] = useState(false);

    // Blur-Tracking pro Feld
    const [nameBlurred, setNameBlurred] = useState(false);
    const [emailBlurred, setEmailBlurred] = useState(false);
    const [passwordBlurred, setPasswordBlurred] = useState(false);
    const [confirmBlurred, setConfirmBlurred] = useState(false);

    const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    const pwValid =
        password.length >= 8 &&
        /[A-Z]/.test(password) &&
        /[a-z]/.test(password) &&
        /[0-9]/.test(password) &&
        /[^A-Za-z0-9]/.test(password);
    const pwMatch = password === confirmPassword && confirmPassword.length > 0;

    const nameState = (): "default" | "error" => {
        if ((!nameBlurred && !submitFailed) || !name && !nameBlurred && !submitFailed) return "default";
        return name.trim() ? "default" : "error";
    };

    const emailState = (): "default" | "error" | "success" => {
        if (emailTaken) return "error";
        if (!emailBlurred && !submitFailed) return "default";
        if (!email) return "error";
        return emailValid ? "success" : "error";
    };

    const confirmState = (): "default" | "error" | "success" => {
        if (!confirmBlurred && !submitFailed) return "default";
        if (!confirmPassword) return "error";
        return pwMatch ? "success" : "error";
    };

    const pwFieldState = (): "default" | "error" | "success" => {
        if (!passwordBlurred && !submitFailed) return "default";
        if (!password) return "error";
        return pwValid ? "success" : "default";
    };

    const handleSubmit = async () => {
        setSubmitFailed(true);
        setNameBlurred(true);
        setEmailBlurred(true);
        setPasswordBlurred(true);
        setConfirmBlurred(true);
        setServerError("");
        setEmailTaken(false);
        if (!name.trim() || !emailValid || !pwValid || !pwMatch) return;
        setSubmitFailed(false);
        setBusy(true);
        try {
            await register(email, name, password);
            onClose();
            router.push("/recipeFinder");
        } catch (e: unknown) {
            const msg = e instanceof Error ? e.message : "Registrierung fehlgeschlagen";
            if (msg.toLowerCase().includes("bereits")) {
                setEmailTaken(true);
            }
            setServerError(msg);
        } finally {
            setBusy(false);
        }
    };

    return (
        <div>
            <h2 className={styles.title}>Account erstellen</h2>
            <p className={styles.subtitle}>Melden Sie sich an, um Ihre Lieblingsrezepte zu speichern.</p>
            {serverError && <p className={styles.error}>{serverError}</p>}
            <Field label="Name" value={name} onChange={setName} placeholder="Name" onBlur={() => setNameBlurred(true)} state={nameState()} />
            <Field label="Email" type="email" value={email} onChange={(v: string) => { setEmail(v); setEmailTaken(false); setServerError(""); if (emailBlurred) setEmailBlurred(false); }} placeholder="Email" onBlur={() => setEmailBlurred(true)} state={emailState()} />
            <Field label="Password" type="password" value={password} onChange={setPassword} placeholder="••••••••" onBlur={() => setPasswordBlurred(true)} state={pwFieldState()} />
            <PasswordChecklist password={password} />
            <Field label="Passwort bestätigen" type="password" value={confirmPassword} onChange={setConfirmPassword} placeholder="••••••••" onKeyDown={(e: React.KeyboardEvent) => e.key === "Enter" && handleSubmit()} onBlur={() => setConfirmBlurred(true)} state={confirmState()} />
            <button className={styles.btn} disabled={busy} onClick={handleSubmit}>
                {busy ? "Wird erstellt…" : "Account erstellen"}
            </button>
            <p className={styles.switchText}>
                Bereits registriert?{" "}
                <button className={styles.switchBtn} onClick={onSwitch}>Anmelden</button>
            </p>
        </div>
    );
}