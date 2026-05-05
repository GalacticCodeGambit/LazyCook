import {Button} from "@/app/components/ui/button";
import {fetchWithAuth} from "@/lib/auth";
import {useState} from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3000";
export default function ChangeEmail (){


    const [newEmail, setNewEmail] = useState("");
    const [emailMsg, setEmailMsg] = useState("");

    async function handleEmailChange() {
        setEmailMsg("");
        try {
            const res = await fetchWithAuth(`${API_URL}/users/me`, {
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
        <div className="popup">
                <h2 className="text-lg font-semibold text-gray-900">E-Mail ändern</h2>
                <input
                    type="email"
                    placeholder="Neue E-Mail-Adresse"
                    value={newEmail}
                    onChange={(e) => setNewEmail(e.target.value)}
                    className="border rounded-lg px-3 py-2 text-sm w-full"
                />
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