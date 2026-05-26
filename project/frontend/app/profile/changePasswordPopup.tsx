import {fetchWithAuth} from "@/lib/auth";
import {useState} from "react";
import {Button} from "@/app/components/ui/button";
import {Eye, EyeOff} from "lucide-react";
import "../recipeFinder/style.css"
import Field from "@/app/components/fields";

function PasswordInput({ value, onChange, placeholder, onKeyDown, ariaLabel }: {
    readonly value: string;
    readonly  onChange: (v: string) => void;
    readonly placeholder: string;
    readonly onKeyDown?: (e: React.KeyboardEvent) => void;
    readonly ariaLabel?: string;
}) {
    const [show, setShow] = useState(false);
    return (
        <div style={{ position: "relative", width: "100%" }}>
            <input
                type={show ? "text" : "password"}
                placeholder={placeholder}
                aria-label={ariaLabel ?? placeholder}
                value={value}
                onChange={(e) => onChange(e.target.value)}
                onKeyDown={onKeyDown}
                className="popup__input"
                style={{ width: "100%", paddingRight: 38 }}
            />
            <button
                type="button"
                onClick={() => setShow((s) => !s)}
                aria-label={show ? "Passwort verbergen" : "Passwort anzeigen"}
                aria-pressed={show}
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

interface ChangePasswordProps {
    onSuccess?: () => void;
}

export default function ChangePassword({ onSuccess }: Readonly<ChangePasswordProps>) {

    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [passwordMsg, setPasswordMsg] = useState("");
    const [pwBlurred, setPwBlurred] = useState(false);

    async function handlePasswordChange() {
        setPasswordMsg("");

        if (!currentPassword) {
            setPasswordMsg("Bitte das aktuelle Passwort eingeben.");
            return;
        }
        if (!newPassword) {
            setPasswordMsg("Bitte ein neues Passwort eingeben.");
            return;
        }
        if (!confirmPassword) {
            setPasswordMsg("Bitte das neue Passwort bestätigen.");
            return;
        }

        if (newPassword !== confirmPassword) {
            setPasswordMsg("Die Passwörter stimmen nicht überein.");
            return;
        }

        try {
            const res = await fetchWithAuth("/users/me", {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ currentPassword, newPassword }),
            });

            if (!res.ok) {
                const err = await res.json();
                setPasswordMsg(`❌ ${err.detail}`);
                return;
            }

            setPasswordMsg("Passwort erfolgreich geändert.");
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
            <h2 className="popup__title">Passwort ändern</h2>

            <div className="popup__fields popup__fields--stacked">
                <Field label="Aktuelles Passwort" type="password" value={currentPassword} onChange={setCurrentPassword} placeholder="••••••••" onBlur={() => setPwBlurred(true)} onKeyDown={(e) => e.key === "Enter" && handlePasswordChange()} state={pwBlurred && !currentPassword? "error" : "default"} />


                <PasswordInput
                    placeholder="Neues Passwort"
                    value={newPassword}
                    onChange={setNewPassword}
                    onKeyDown={(e) => e.key === "Enter" && handlePasswordChange()}
                />

                <PasswordInput
                    placeholder="Neues Passwort bestätigen"
                    value={confirmPassword}
                    onChange={setConfirmPassword}
                    onKeyDown={(e) => e.key === "Enter" && handlePasswordChange()}
                />
            </div>

            {passwordMsg && <p className="text-sm">{passwordMsg}</p>}

            <div className="flex gap-3 justify-end">
                <Button
                    className="px-4 py-2 rounded-lg bg-black text-white hover:bg-gray-800 text-sm font-medium"
                    onClick={handlePasswordChange}
                >
                    Speichern
                </Button>
            </div>
        </div>

    );
}