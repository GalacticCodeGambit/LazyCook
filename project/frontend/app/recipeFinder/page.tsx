"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { ChefHat } from "lucide-react";
import { Button } from "@/app/components/ui/button";

export default function RecipeFinder() {
    const { user, loading, logout } = useAuth();
    const router = useRouter();

    // Nicht eingeloggt → zurück zur Startseite
    useEffect(() => {
        if (!loading && !user) {
            router.replace("/");
        }
    }, [loading, user, router]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <p className="text-gray-500">Laden…</p>
            </div>
        );
    }

    if (!user) return null;

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
                        <a href="#" className="text-gray-700 hover:text-black">Datenschutz</a>
                        <a href="#" className="text-gray-700 hover:text-black">Impressum</a>
                    </nav>

                    <div className="flex items-center gap-3">
                        <span className="text-sm text-gray-600">Hallo, {user.name}</span>
                        <Button
                            variant="ghost"
                            className="text-sm"
                            onClick={() => { logout(); router.replace("/"); }}
                        >
                            Abmelden
                        </Button>
                    </div>
                </div>
            </header>

            {/* Dashboard Content */}
            <main className="max-w-4xl mx-auto px-6 py-12">
                <h1 className="text-3xl font-semibold mb-2">Dashboard</h1>
                <p className="text-gray-600 mb-8">Willkommen zurück, {user.name}!</p>

                <div className="grid md:grid-cols-2 gap-6">
                    <div className="border rounded-lg p-6">
                        <h3 className="font-semibold mb-3">Profil</h3>
                        <p className="text-sm text-gray-600">E-Mail: {user.email}</p>
                        <p className="text-sm text-gray-600">Name: {user.name}</p>
                    </div>

                    <div className="border rounded-lg p-6">
                        <h3 className="font-semibold mb-3">Favoriten</h3>
                        <p className="text-sm text-gray-600">Du hast noch keine Rezepte gespeichert.</p>
                    </div>
                </div>
            </main>
        </div>
    );
}