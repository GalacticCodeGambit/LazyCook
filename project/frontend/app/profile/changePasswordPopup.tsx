import {fetchWithAuth} from "@/lib/auth";
import {useState} from "react";
import {Button} from "@/app/components/ui/button";
import {Eye, EyeOff} from "lucide-react";
import "../recipeFinder/style.css"

function PasswordInput({ value, onChange, placeholder }: {
    value: string;
    onChange: (v: string) => void;
    placeholder: string;
}) {
    const [show, setShow] = useState(false);
    return (
        <div style={{ position: "relative", width: "100%" }}>
            <input
                type={show ? "text" : "password"}
                placeholder={placeholder}
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className="popup__input"
                style={{ width: "100%", paddingRight: 38 }}
            />
            <button
                type="button"
                onClick={() => setShow((s) => !s)}
                aria-label={show ? "Passwort verbergen" : "Passwort anzeigen"}
                tabIndex={-1}
                style={{
                    position: "absolute",
                    right: 10,
                    top: "50%",
                    transform: "translateY(-50%)",
                    background: "none",
                    border: "none",
                    cursor: "pointer",
                    padding: 0,
                    display: "flex",
                    alignItems: "center",
                    color: "#666",
                }}
            >
                {show ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
        </div>
    );
}

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3000";

type Modus = "change" | "forgot";

interface ChangePasswordProps {
    modus: Modus;
    onSuccess?: () => void;
}

export default function ChangePassword({ modus, onSuccess }: ChangePasswordProps) {

    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [passwordMsg, setPasswordMsg] = useState("");

    const isForgot = modus === "forgot";

    async function handlePasswordChange() {
        setPasswordMsg("");

        // Bestätigung prüfen (nur im forgot-Modus relevant, aber sinnvoll auch beim Ändern)
        if (newPassword !== confirmPassword) {
            setPasswordMsg("Die Passwörter stimmen nicht überein.");
            return;
        }

        try {
            const endpoint = isForgot
                ? `${API_URL}/users/forgot-password`
                : `${API_URL}/users/me`;

            const body = isForgot
                ? { newPassword }
                : { currentPassword, newPassword };

            const fetcher = isForgot ? fetch : fetchWithAuth;

            const res = await fetcher(endpoint, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            });

            if (!res.ok) {
                const err = await res.json();
                setPasswordMsg(`❌ ${err.detail}`);
                return;
            }

            setPasswordMsg(
                isForgot
                    ? "Passwort erfolgreich zurückgesetzt."
                    : "Passwort erfolgreich geändert."
            );
            setCurrentPassword("");
            setNewPassword("");
            setConfirmPassword("");
            onSuccess?.();
        } catch {
            setPasswordMsg('❌ Unbekannter Fehler');
        }
    }

    return (
        <div className="popup w-[480px] max-w-full">
            <h2 className="popup__title">
                {isForgot ? "Passwort zurücksetzen" : "Passwort ändern"}
            </h2>

            <div className="popup__fields popup__fields--stacked">
                {!isForgot && (
                    <PasswordInput
                        placeholder="Aktuelles Passwort"
                        value={currentPassword}
                        onChange={setCurrentPassword}
                    />
                )}

                <PasswordInput
                    placeholder="Neues Passwort"
                    value={newPassword}
                    onChange={setNewPassword}
                />

                <PasswordInput
                    placeholder="Neues Passwort bestätigen"
                    value={confirmPassword}
                    onChange={setConfirmPassword}
                />
            </div>

            {passwordMsg && <p className="text-sm">{passwordMsg}</p>}

            <div className="flex gap-3 justify-end">
                <Button
                    className="px-4 py-2 rounded-lg bg-black text-white hover:bg-gray-800 text-sm font-medium"
                    onClick={handlePasswordChange}
                >
                    {isForgot ? "Zurücksetzen" : "Speichern"}
                </Button>
            </div>
        </div>

    );
}