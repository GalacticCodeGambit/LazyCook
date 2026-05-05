"use client";

import React, { Suspense, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Field from "@/app/components/fields";
import styles from "@/app/homepage/page.module.css";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3000";

function ResetPasswordContent() {
    const params = useSearchParams();
    const router = useRouter();
    const token = params.get("token") ?? "";

    const [password, setPassword] = useState("");
    const [confirm, setConfirm] = useState("");
    const [busy, setBusy] = useState(false);
    const [error, setError] = useState("");
    const [done, setDone] = useState(false);

    const pwValid =
        password.length >= 8 &&
        /[A-Z]/.test(password) &&
        /[a-z]/.test(password) &&
        /[0-9]/.test(password) &&
        /[^A-Za-z0-9]/.test(password);
    const pwMatch = password === confirm && confirm.length > 0;

    const handleSubmit = async () => {
        setError("");
        if (!pwValid) {
            setError("Passwort erfüllt nicht alle Anforderungen.");
            return;
        }
        if (!pwMatch) {
            setError("Passwörter stimmen nicht überein.");
            return;
        }
        setBusy(true);
        try {
            const res = await fetch(`${API_URL}/auth/reset-password`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ token, new_password: password }),
            });
            if (!res.ok) {
                const data = await res.json();
                setError(data.detail ?? "Fehler beim Zurücksetzen.");
                return;
            }
            setDone(true);
            setTimeout(() => router.push("/"), 2500);
        } catch {
            setError("Verbindungsfehler.");
        } finally {
            setBusy(false);
        }
    };

    if (!token) {
        return (
            <div style={{ maxWidth: 420, margin: "4rem auto", padding: "2rem" }}>
                <h2 className={styles.title}>Ungültiger Link</h2>
                <p className={styles.subtitle}>
                    Der Link ist unvollständig. Bitte fordere einen neuen an.
                </p>
            </div>
        );
    }

    if (done) {
        return (
            <div style={{ maxWidth: 420, margin: "4rem auto", padding: "2rem" }}>
                <h2 className={styles.title}>Erledigt!</h2>
                <p className={styles.subtitle}>
                    Dein Passwort wurde zurückgesetzt. Du wirst gleich weitergeleitet…
                </p>
            </div>
        );
    }

    return (
        <div style={{ maxWidth: 420, margin: "4rem auto", padding: "2rem" }}>
            <h2 className={styles.title}>Neues Passwort festlegen</h2>
            <p className={styles.subtitle}>Wähle ein sicheres neues Passwort.</p>
            {error && <p className={styles.error}>{error}</p>}
            <Field
                label="Neues Passwort"
                type="password"
                value={password}
                onChange={setPassword}
                placeholder="••••••••"
                state={password && !pwValid ? "error" : "default"}
            />
            <Field
                label="Passwort bestätigen"
                type="password"
                value={confirm}
                onChange={setConfirm}
                placeholder="••••••••"
                state={confirm && !pwMatch ? "error" : pwMatch ? "success" : "default"}
            />
            <button className={styles.btn} disabled={busy} onClick={handleSubmit}>
                {busy ? "Wird gespeichert…" : "Passwort zurücksetzen"}
            </button>
        </div>
    );
}

export default function ResetPasswordPage() {
    return (
        <Suspense
            fallback={
                <div style={{ maxWidth: 420, margin: "4rem auto", padding: "2rem" }}>
                    <p className={styles.subtitle}>Wird geladen…</p>
                </div>
            }
        >
            <ResetPasswordContent />
        </Suspense>
    );
}