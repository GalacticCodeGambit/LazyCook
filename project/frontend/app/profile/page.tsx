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

    const [showEmailModal, setShowEmailModal] = useState(false);
    const [showPasswordModal, setShowPasswordModal] = useState(false);

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
            <div className="max-w-7xl mx-auto px-6 py-8 flex flex-col items-center gap-6">

                {/* Profil-Anzeige */}
                <div className="border rounded-lg p-6 w-full max-w-sm">
                    <h3 className="font-semibold mb-3">Profil</h3>
                    <p className="text-sm text-gray-600">E-Mail: {user.email}</p>
                    <p className="text-sm text-gray-600">Name: {user.name}</p>
                </div>

                {/* Buttons */}
                <div className="border rounded-lg p-6 flex flex-col gap-3 w-full max-w-sm">
                    <h3 className="font-semibold">Einstellungen</h3>
                    <Button
                        onClick={() => { setShowEmailModal(true); setEmailMsg(""); }}
                        className="bg-black text-white hover:bg-gray-800 text-sm w-full"
                    >
                        E-Mail ändern
                    </Button>
                    <Button
                        onClick={() => { setShowPasswordModal(true); setPasswordMsg(""); }}
                        className="bg-black text-white hover:bg-gray-800 text-sm w-full"
                    >
                        Passwort ändern
                    </Button>
                </div>

            </div>

            {/* E-Mail Modal */}
            {showEmailModal && (
                <div
                    className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
                    onClick={() => setShowEmailModal(false)}
                >
                    <div
                        className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-sm mx-4 flex flex-col gap-4"
                        onClick={(e) => e.stopPropagation()}
                    >
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
                                className="px-4 py-2 rounded-lg border bg-gray-50 border-gray-300 text-gray-700 hover:bg-gray-300 text-sm font-medium"
                                onClick={() => setShowEmailModal(false)}
                            >
                                Abbrechen
                            </Button>
                            <Button
                                className="px-4 py-2 rounded-lg bg-black text-white hover:bg-gray-800 text-sm font-medium"
                                onClick={handleEmailChange}
                            >
                                Speichern
                            </Button>
                        </div>
                    </div>
                </div>
            )}

            {/* Passwort Modal */}
            {showPasswordModal && (
                <div
                    className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
                    onClick={() => setShowPasswordModal(false)}
                >
                    <div
                        className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-sm mx-4 flex flex-col gap-4"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <h2 className="text-lg font-semibold text-gray-900">Passwort ändern</h2>
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
                        {passwordMsg && <p className="text-sm">{passwordMsg}</p>}
                        <div className="flex gap-3 justify-end">
                            <Button
                                className="px-4 py-2 rounded-lg border bg-gray-50 border-gray-300 text-gray-700 hover:bg-gray-300 text-sm font-medium"
                                onClick={() => setShowPasswordModal(false)}
                            >
                                Abbrechen
                            </Button>
                            <Button
                                className="px-4 py-2 rounded-lg bg-black text-white hover:bg-gray-800 text-sm font-medium"
                                onClick={handlePasswordChange}
                            >
                                Speichern
                            </Button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
