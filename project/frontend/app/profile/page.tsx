"use client";

import {useEffect, useRef, useState} from "react";
import { useAuth, fetchWithAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import {ChefHat} from "lucide-react";
import { Button } from '../components/ui/button';
import ProfileDropdown from "@/app/components/profile_dropdown";
import Modal from "@/app/components/modal";
import ChangeEmail from "@/app/profile/changeEmailPopup";
import ChangePassword from "@/app/profile/changePasswordPopup";

import "../recipeFinder/style.css"

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3000";

export default function Profile() {
    const { user, loading, logout } = useAuth();
    const router = useRouter();
    const menuRef = useRef<HTMLDivElement>(null);

    const [showConfirm, setShowConfirm] = useState(false);

    const [showEmailModal, setShowEmailModal] = useState(false);
    const [showPasswordModal, setShowPasswordModal] = useState(false);

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

                    <ProfileDropdown>
                    </ProfileDropdown>

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
                        onClick={() => { setShowEmailModal(true) }}
                        className="bg-black text-white hover:bg-gray-800 text-sm w-full"
                    >
                        E-Mail ändern
                    </Button>
                    <Button
                        onClick={() => { setShowPasswordModal(true); }}
                        className="bg-black text-white hover:bg-gray-800 text-sm w-full"
                    >
                        Passwort ändern
                    </Button>
                </div>
                <Button
                    className="bg-red-600 text-white hover:bg-red-700 text-sm font-medium"
                    onClick={() => setShowConfirm (true)}
                >
                    Konto löschen
                </Button>

            </div>

            <Modal open={showConfirm} onCloseAction={() => setShowConfirm(false)}>
                <div>
                    <h2 className="text-lg font-semibold text-gray-900">
                        Konto wirklich löschen?
                    </h2>
                    <p className="flex gap-3 justify-end">
                        <Button className="bg-red-600 text-white hover:bg-red-700 text-sm font-medium"
                                onClick={handleAccountDeletion}>
                            Bestätigen
                        </Button>
                        <Button className="bg-gray-600 text-white hover:bg-gray-700 text-sm font-medium"
                                onClick={() => setShowConfirm(false)}>
                            Abbrechen
                        </Button>
                    </p>

                </div>
            </Modal>

            <Modal open={showEmailModal} onCloseAction={() => setShowEmailModal(false)}>
                <ChangeEmail></ChangeEmail>
            </Modal>

            <Modal open={showPasswordModal} onCloseAction={() => setShowPasswordModal(false)}>
                <ChangePassword modus="change"></ChangePassword>
            </Modal>
        </div>
    );
}
