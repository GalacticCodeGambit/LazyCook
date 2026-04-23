"use client";

import {useEffect, useRef, useState} from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import {ChefHat, LogOut} from "lucide-react";
import { User, UserCircle } from "lucide-react";
import "./style.css"

export default function RecipeFinder() {
    const { user, loading, logout } = useAuth();
    const router = useRouter();

    const [open, setOpen] = useState(false);
    const menuRef = useRef<HTMLDivElement>(null);

    // Nicht eingeloggt → zurück zur Startseite
    useEffect(() => {
        if (!loading && !user) {
            router.replace("/");
        }
    }, [loading, user, router]);

    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
                setOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <p className="text-gray-500">Laden…</p>
            </div>
        );
    }

    if (!user) return null;

    const handleProfil = () => {
        setOpen(false);
        console.log("Profil ansehen");
        router.push("/profile");
    };

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
                        <a href="#" className="text-gray-700 hover:text-black">RecipeFinder</a>
                        <a href="#" className="text-gray-700 hover:text-black">Favoriten</a>
                        <a href="#" className="text-gray-700 hover:text-black">Neues Rezept</a>
                    </nav>

                    <div className="flex items-center gap-3">
                        <div ref={menuRef} className="account-menu">
                            <button
                                onClick={() => setOpen(!open)}
                                className="account-menu__trigger"
                                aria-label="Account-Menü"
                                aria-expanded={open}
                            >
                                <User size={28} />
                            </button>

                            {open && (
                                <div className="account-menu__dropdown" role="menu">
                                    <button
                                        onClick={handleProfil}
                                        className="account-menu__item"
                                        role="menuitem"
                                    >
                                        <UserCircle size={18} />
                                        <span>Profil ansehen</span>
                                    </button>
                                    <button
                                        onClick={() => { logout(); router.replace("/"); }}
                                        className="account-menu__item"
                                        role="menuitem"
                                    >
                                        <LogOut size={18} />
                                        <span>Abmelden</span>
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </header>

            {/* Dashboard Content */}
            <main className="max-w-4xl mx-auto px-6 py-12">
                <h1 className="text-3xl font-semibold mb-2">Dashboard</h1>
                <p className="text-gray-600 mb-8">Willkommen zurück, {user.name}!</p>

                <div className="grid md:grid-cols-2 gap-6">
                    <div className="border rounded-lg p-6">
                        <h3 className="font-semibold mb-3">Favoriten</h3>
                        <p className="text-sm text-gray-600">Du hast noch keine Rezepte gespeichert.</p>
                    </div>
                </div>
            </main>
        </div>
    );
}