import React, { useState } from "react";
import Field from "@/app/components/fields";
import styles from "./page.module.css";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3000";

export default function ForgotPasswordForm({ onClose, onBack,}: { onClose: () => void; onBack: () => void; }) {
    const [email, setEmail] = useState("");
    const [busy, setBusy] = useState(false);
    const [submitted, setSubmitted] = useState(false);
    const [emailBlurred, setEmailBlurred] = useState(false);

    const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

    const handleSubmit = async () => {
        setEmailBlurred(true);
        if (!emailValid) return;
        setBusy(true);
        try {
            await fetch(`${API_URL}/auth/forgot-password`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email }),
            });
            setSubmitted(true);
        } finally {
            setBusy(false);
        }
    };

    if (submitted) {
        return (
            <div>
                <h2 className={styles.title}>E-Mail versendet</h2>
                <p className={styles.subtitle}>
                    Falls ein Konto mit dieser E-Mail existiert, haben wir dir einen
                    Link zum Zurücksetzen geschickt. Prüfe auch deinen Spam-Ordner.
                </p>
                <button className={styles.btn} onClick={onClose}>
                    Schließen
                </button>
            </div>
        );
    }

    return (
        <div>
            <h2 className={styles.title}>Passwort vergessen</h2>
            <p className={styles.subtitle}>
                Gib deine E-Mail-Adresse ein. Wir schicken dir einen Link zum
                Zurücksetzen.
            </p>
            <Field
                label="Email"
                type="email"
                value={email}
                onChange={(v: string) => setEmail(v)}
                placeholder="Email"
                onBlur={() => setEmailBlurred(true)}
                onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
                state={
                    emailBlurred && !emailValid ? "error" : emailValid ? "success" : "default"
                }
            />
            <button className={styles.btn} disabled={busy} onClick={handleSubmit}>
                {busy ? "Wird gesendet…" : "Link anfordern"}
            </button>
            <p className={styles.switchText}>
                <button className={styles.switchBtn} onClick={onBack}>
                    Zurück zur Anmeldung
                </button>
            </p>
        </div>
    );
}