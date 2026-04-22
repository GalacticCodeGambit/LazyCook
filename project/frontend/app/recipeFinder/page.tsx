"use client";

import {useEffect, useRef, useState} from "react";
import { useRouter } from "next/navigation";
import {fetchWithAuth, useAuth} from "@/lib/auth";
import {ChefHat, LogOut, X, User, UserCircle, Search, Plus} from "lucide-react";
import "./style.css"
import {Button} from "@/app/components/ui/button";
import Modal from "@/app/components/modal";
import AddIngredientsPopup from "@/app/recipeFinder/popup";

interface IngredientInput {
    name: string;
    amount: number;
    unit: string;
}

export default function RecipeFinder() {
    const { user, loading, logout } = useAuth();
    const router = useRouter();

    const [open, setOpen] = useState(false);
    const menuRef = useRef<HTMLDivElement>(null);

    const [ingredients, setIngredients] = useState<IngredientInput[]>(() => {
        try {
            const saved = localStorage.getItem("ingredients");
            return saved ? JSON.parse(saved) : [];
        } catch {
            return [];
        }
    });

    const [servings, setServings] = useState(1);

    const [searching, setSearching] = useState(false);
    const [results, setResults] = useState<any[] | null>(null);

    const [searchError, setSearchError] = useState("");

    const [modalOpen, setModalOpen] = useState(false);

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

    useEffect(() => {
        localStorage.setItem("ingredients", JSON.stringify(ingredients));
    }, [ingredients]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <p className="text-gray-500">Laden…</p>
            </div>
        );
    }

    if (!user) return null;

    const handleLogout = () => {
        logout();
        router.replace("/");
    }
    const handleProfil = () => {
        setOpen(false);
        console.log("Profil ansehen");
        router.push("/profile");
    };

    const handleAdd = (ingredient: IngredientInput) => {
        setIngredients(prev => [...prev, ingredient]);
    };

    const handleRemoveIngredient = (name: string) => {
        setIngredients(prev => prev.filter(z => z.name !== name));
    }

    const handleSearch = async () => {
        if (ingredients.length === 0) {
            setSearchError("Bitte mindestens eine Zutat hinzufügen.");
            return;
        }
        setSearchError("");
        setSearching(true);
        try {
            const res = await fetchWithAuth('/recipes/search', {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({zutaten: ingredients, servings}),
            });
            const data = await res.json();
            setResults(data.rezepte ?? []);
        } catch {
            setSearchError("Suche fehlgeschlagen.");
        } finally {
            setSearching(false);
        }
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
                        <a href="#" className="text-gray-700 hover:text-black">Favoriten</a>
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
                                        onClick={ handleLogout }
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

            <div className="finder-layout">
                {/* Sidebar */}
                <aside className="finder-sidebar">

                    {/* Zutaten hinzufügen */}
                    <div className="finder-sidebar__section">
                        <p className="finder-sidebar__title">Zutaten</p>
                        <div style={{ display: "flex", gap: 8 }}>
                            <Button onClick={() => setModalOpen(true)} className="finder-sidebar__add-btn">
                                <Plus size={15} />
                                Zutat hinzufügen
                            </Button>
                            <Button onClick={() => setIngredients([])} className="finder-sidebar__clear-btn">
                                Alle entfernen
                            </Button>
                        </div>


                        {ingredients.length > 0 ? (
                            <div className="finder-sidebar__ingredient-list">
                                {ingredients.map(i => (
                                    <div key={i.name} className="finder-sidebar__ingredient">
                                        <span className="finder-sidebar__ingredient-name">{i.name}</span>
                                        <span className="finder-sidebar__ingredient-amount">{i.amount} {i.unit}</span>
                                        <button onClick={() => handleRemoveIngredient(i.name)} className="finder-sidebar__ingredient-remove">
                                            <X size={14} />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="finder-sidebar__empty">Noch keine Zutaten.</p>
                        )}
                    </div>

                    {/* Personenanzahl */}
                    <div className="finder-sidebar__section">
                        <p className="finder-sidebar__title">Personen</p>
                        <div className="finder-sidebar__persons">
                            <button onClick={() => setServings(Math.max(1, servings - 1))} className="finder-sidebar__persons-btn">−</button>
                            <div>
                                <div className="finder-sidebar__persons-count">{servings}</div>
                                <div className="finder-sidebar__persons-label">Personen</div>
                            </div>
                            <button onClick={() => setServings(servings + 1)} className="finder-sidebar__persons-btn">+</button>
                        </div>
                    </div>

                    {/* Suche starten */}
                    <div className="finder-sidebar__section">
                        {searchError && <p style={{ color: '#b91c1c', fontSize: 13, fontFamily: 'system-ui', marginBottom: 8 }}>{searchError}</p>}
                        <button onClick={handleSearch} disabled={searching || ingredients.length === 0} className="finder-sidebar__search-btn">
                            <Search size={15} />
                            {searching ? "Suche läuft…" : "Rezepte suchen"}
                        </button>
                    </div>
                </aside>

                <Modal open={modalOpen} onCloseAction={() => setModalOpen(false)}>
                    <AddIngredientsPopup
                        ingredients={ingredients}
                        onAdd={handleAdd}
                        servings={servings}
                        onServingsChange={setServings}
                    />
                </Modal>
            </div>
        </div>
    );
}