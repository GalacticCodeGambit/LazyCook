"use client";

import { useState } from "react";
import { useAuth, fetchWithAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { ChefHat } from "lucide-react";
import { Button } from '../components/ui/button';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3000";

export default function Profile() {
    const { user, logout } = useAuth();
    const router = useRouter();
    const [showConfirm, setShowConfirm] = useState(false);

    // E-Mail ändern
    const [newEmail, setNewEmail] = useState("");
    const [emailMsg, setEmailMsg] = useState("");

    // Passwort ändern
    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [passwordMsg, setPasswordMsg] = useState("");

    if (!user) return null;

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

    async function handlePasswordChange() {
        setPasswordMsg("");
        try {
            const res = await fetchWithAuth(`${API_URL}/users/me`, {
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
        } catch {
            setPasswordMsg("Unbekannter Fehler.");
        }
    }

    async function handleAccountDeletion() {
        const res = await fetchWithAuth(`${API_URL}/users/me`, { method: "DELETE" });
        if (!res.ok) throw new Error("Konto löschen fehlgeschlagen");
        logout();
        router.push("/");
    }

    return (
        <div className="min-h-screen bg-white">
            {/* Navbar */}
            <header className="border-b bg-white sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <ChefHat className="w-8 h-8" />
                        <span className="text-xl">Lazy Cook</span>
                    </div>
                    <nav className="hidden md:flex items-center gap-6">
                        <a href="/recipeFinder" className="text-gray-700 hover:text-black">RecipeFinder</a>
                    </nav>
                    <Button
                        className="bg-red-600 text-white hover:bg-red-700 text-sm font-medium"
                        onClick={() => setShowConfirm(true)}
                    >
                        Konto löschen
                    </Button>
                </div>
            </header>

            {/* Inhalt */}
            <div className="max-w-7xl mx-auto px-6 py-8 grid md:grid-cols-2 gap-6">

                {/* Profil-Anzeige */}
                <div className="border rounded-lg p-6">
                    <h3 className="font-semibold mb-3">Profil</h3>
                    <p className="text-sm text-gray-600">E-Mail: {user.email}</p>
                    <p className="text-sm text-gray-600">Name: {user.name}</p>
                </div>

                {/* E-Mail ändern */}
                <div className="border rounded-lg p-6 flex flex-col gap-3">
                    <h3 className="font-semibold">E-Mail ändern</h3>
                    <input
                        type="email"
                        placeholder="Neue E-Mail-Adresse"
                        value={newEmail}
                        onChange={(e) => setNewEmail(e.target.value)}
                        className="border rounded-lg px-3 py-2 text-sm w-full"
                    />
                    <Button
                        onClick={handleEmailChange}
                        className="bg-black text-white hover:bg-gray-800 text-sm"
                    >
                        E-Mail speichern
                    </Button>
                    {emailMsg && <p className="text-sm">{emailMsg}</p>}
                </div>

                {/* Passwort ändern */}
                <div className="border rounded-lg p-6 flex flex-col gap-3">
                    <h3 className="font-semibold">Passwort ändern</h3>
                    <input
                        type="password"
                        placeholder="Aktuelles Passwort"
                        value={currentPassword}
                        onChange={(e) => setCurrentPassword(e.target.value)}
                        className="border rounded-lg px-3 py-2 text-sm w-full"
                    />
                    <input
                        type="password"
                        placeholder="Neues Passwort"
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                        className="border rounded-lg px-3 py-2 text-sm w-full"
                    />
                    <Button
                        onClick={handlePasswordChange}
                        className="bg-black text-white hover:bg-gray-800 text-sm"
                    >
                        Passwort speichern
                    </Button>
                    {passwordMsg && <p className="text-sm">{passwordMsg}</p>}
                </div>

            </div>

            {/* Bestätigungs-Modal */}
            {showConfirm && (
                <div
                    className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
                    onClick={() => setShowConfirm(false)}
                >
                    <div
                        className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-sm mx-4 flex flex-col gap-4"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <h2 className="text-lg font-semibold text-gray-900">Konto löschen</h2>
                        <p className="text-sm text-gray-600">
                            Möchtest du dein Konto wirklich löschen? Diese Aktion kann nicht rückgängig gemacht werden.
                        </p>
                        <div className="flex gap-3 justify-end mt-2">
                            <Button
                                className="px-4 py-2 rounded-lg border bg-gray-50 border-gray-300 text-gray-700 hover:bg-gray-300 text-sm font-medium"
                                onClick={() => setShowConfirm(false)}
                            >
                                Abbrechen
                            </Button>
                            <Button
                                className="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700 text-sm font-medium"
                                onClick={handleAccountDeletion}
                            >
                                Konto löschen
                            </Button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
