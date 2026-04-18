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

    if (!user) return null;

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

            <div className="grid md:grid-cols-2 gap-6">
                <div className="border rounded-lg p-6">
                    <h3 className="font-semibold mb-3">Profil</h3>
                    <p className="text-sm text-gray-600">E-Mail: {user.email}</p>
                    <p className="text-sm text-gray-600">Name: {user.name}</p>
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