import {Button} from "@/app/components/ui/button";
import {fetchWithAuth} from "@/lib/auth";
import {useState} from "react";
import "../recipeFinder/style.css"

export default function ChangeEmail (){


    const [newEmail, setNewEmail] = useState("");
    const [emailMsg, setEmailMsg] = useState("");

    async function handleEmailChange() {
        setEmailMsg("");
        try {
            const res = await fetchWithAuth(`/users/me`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: newEmail }),
            });
            if (!res.ok) {
                const err = await res.json();
                setEmailMsg(`${err.detail}`);
                return;
            }
            setEmailMsg("E-Mail erfolgreich geändert.");
            setNewEmail("");
        } catch {
            setEmailMsg("Unbekannter Fehler.");
        }
    }

    return (
        <div className="popup w-[480px] max-w-full">
                <h2 className="popup__title">E-Mail ändern</h2>
                <div className="popup__fields">
                    <input
                        type="email"
                        placeholder="Neue E-Mail-Adresse"
                        value={newEmail}
                        onChange={(e) => setNewEmail(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleEmailChange()}
                        className="popup__input"
                    />
                </div>
                {emailMsg && <p className="text-sm">{emailMsg}</p>}
                <div className="flex gap-3 justify-end">
                    <Button
                        className="px-4 py-2 rounded-lg bg-black text-white hover:bg-gray-800 text-sm font-medium"
                        onClick={handleEmailChange}
                    >
                        Speichern
                    </Button>
                </div>
        </div>
    );
}