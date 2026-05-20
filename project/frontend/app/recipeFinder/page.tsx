"use client";

import {useEffect, useRef, useState} from "react";
import { useRouter } from "next/navigation";
import {fetchWithAuth, useAuth} from "@/lib/auth";
import {ChefHat, X, Search, Plus} from "lucide-react";
import "./style.css"
import {Button} from "@/app/components/ui/button";
import Modal from "@/app/components/modal";
import AddIngredientsPopup from "@/app/recipeFinder/popup";
import ProfileDropdown from "@/app/components/profile_dropdown";

const EINHEITEN = ["Stück", "g", "kg", "ml", "l", "EL", "TL", "Prise"];

interface IngredientInput {
    name: string;
    amount: number;
    unit: string;
}

interface Suggestion {
    name: string;
    unit: string | null;
}

// Reine Helper-Funktion auf Modulebene – schließt keinen Component-State ein,
// damit useEffect/useCallback keine ändernden Closure-Variablen aufnehmen müssen.
async function loadTopIngredients(): Promise<Suggestion[] | null> {
    try {
        const res = await fetchWithAuth(`/ingredients/top?limit=5&_=${Date.now()}`, {
            cache: "no-store",
            headers: { "Cache-Control": "no-cache" },
        });
        if (!res.ok) return null;
        const data = await res.json();
        if (Array.isArray(data.ingredients)) {
            localStorage.setItem("ingredientSuggestions", JSON.stringify(data.ingredients));
            return data.ingredients as Suggestion[];
        }
        return null;
    } catch {
        return null;
    }
}

export default function RecipeFinder() {
    const { user, loading } = useAuth();
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

    const [editingIngredient, setEditingIngredient] = useState<string | null>(null);
    const [editAmount, setEditAmount] = useState("");
    const [editUnit, setEditUnit] = useState("Stück");

    const [searchError, setSearchError] = useState("");

    const [modalOpen, setModalOpen] = useState(false);

    // Vorschläge: localStorage als sofortiger Initialwert (instant beim Öffnen),
    // im Hintergrund per useEffect aktualisiert.
    const [suggestions, setSuggestions] = useState<Suggestion[]>(() => {
        try {
            const saved = localStorage.getItem("ingredientSuggestions");
            return saved ? JSON.parse(saved) : [];
        } catch {
            return [];
        }
    });

    useEffect(() => {
        if (!loading && !user) {
            router.replace("/");
        }
    }, [loading, user, router]);

    // Initial nach dem Login laden (damit sie beim ersten Popup-Öffnen sofort da sind)
    useEffect(() => {
        if (!user) return;
        let cancelled = false;
        loadTopIngredients().then(result => {
            if (!cancelled && result) setSuggestions(result);
        });
        return () => { cancelled = true; };
    }, [user]);

    // Bei jedem Öffnen des Popups erneut laden – aktuelle Daten nach jeder Suche
    useEffect(() => {
        if (!modalOpen || !user) return;
        let cancelled = false;
        loadTopIngredients().then(result => {
            if (!cancelled && result) setSuggestions(result);
        });
        return () => { cancelled = true; };
    }, [modalOpen, user]);

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

    const handleAdd = (ingredient: IngredientInput) => {
        setIngredients(prev => [...prev, ingredient]);
    };

    const handleRemoveIngredient = (name: string) => {
        setIngredients(prev => prev.filter(z => z.name !== name));
    }

    const handleEditSave = (name: string) => {
        const amountNum = parseFloat(editAmount);
        if (!editAmount || isNaN(amountNum) || amountNum <= 0) return;
        setIngredients(prev => prev.map(i =>
            i.name === name ? { ...i, amount: amountNum, unit: editUnit } : i
        ));
        setEditingIngredient(null);
    };

    const handleEditStart = (i: IngredientInput) => {
        setEditingIngredient(i.name);
        setEditAmount(String(i.amount));
        setEditUnit(i.unit);
    };

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
            // Aktualisierte Top 5 direkt aus der Search-Response übernehmen –
            // beim nächsten Popup-Öffnen sind die Vorschläge sofort aktuell, ohne extra Roundtrip
            if (Array.isArray(data.topIngredients)) {
                setSuggestions(data.topIngredients);
                localStorage.setItem("ingredientSuggestions", JSON.stringify(data.topIngredients));
            }
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

                    <ProfileDropdown>
                    </ProfileDropdown>

                </div>
            </header>

            <div className="finder-layout">
                {/* Sidebar */}
                <aside className="finder-sidebar">

                    {/* Zutaten hinzufügen */}
                    <div className="finder-sidebar__section">
                        <p className="finder-sidebar__title">Zutaten</p>
                        <div style={{ display: "flex", gap: 8 }}>
                            <Button
                                onPointerDown={() => {
                                    loadTopIngredients().then(result => {
                                        if (result) setSuggestions(result);
                                    });
                                }}
                                onClick={() => setModalOpen(true)}
                                className="finder-sidebar-add-btn"
                            >
                                <Plus size={15} />
                                Zutat hinzufügen
                            </Button>
                            <Button onClick={() => setIngredients([])} className="finder-sidebar-clear-btn">
                                Alle entfernen
                            </Button>
                        </div>


                        {ingredients.length > 0 ? (
                            <div className="finder-sidebar-ingredient-list">
                                {ingredients.map(i => (
                                    <div key={i.name} className="finder-sidebar-ingredient">
                                        <span className="finder-sidebar-ingredient-name">{i.name}</span>

                                        {editingIngredient === i.name ? (
                                            // Bearbeitungsmodus
                                            <div className="finder-sidebar-ingredient-edit">
                                                <input
                                                    type="number"
                                                    value={editAmount}
                                                    onChange={e => setEditAmount(e.target.value)}
                                                    onKeyDown={e => e.key === "Enter" && handleEditSave(i.name)}
                                                    min={0}
                                                    className="finder-sidebar-edit-input"
                                                    autoFocus
                                                />
                                                <select
                                                    value={editUnit}
                                                    onChange={e => setEditUnit(e.target.value)}
                                                    className="finder-sidebar-edit-select"
                                                >
                                                    {EINHEITEN.map(e => <option key={e} value={e}>{e}</option>)}
                                                </select>
                                                <button onClick={() => handleEditSave(i.name)} className="finder-sidebar-edit-save">✓</button>
                                                <button onClick={() => setEditingIngredient(null)} className="finder-sidebar-edit-cancel">✕</button>
                                            </div>
                                        ) : (
                                            // Anzeigemodus — klickbar
                                            <div className="finder-sidebar-ingredient-right">
                                                <span
                                                    onClick={() => handleEditStart(i)}
                                                    className="finder-sidebar-ingredient-amount"
                                                    title="Klicken zum Bearbeiten"
                                                >
                                                    {i.amount} {i.unit}
                                                </span>
                                                <button onClick={() => handleRemoveIngredient(i.name)} className="finder-sidebar-ingredient-remove">
                                                    <X size={14} />
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="finder-sidebar-empty">Noch keine Zutaten.</p>
                        )}
                    </div>

                    {/* Personenanzahl */}
                    <div className="finder-sidebar-section">
                        <p className="finder-sidebar-title">Personen</p>
                        <div className="finder-sidebar-persons">
                            <button onClick={() => setServings(Math.max(1, servings - 1))} className="finder-sidebar-persons-btn">−</button>
                            <div>
                                <div className="finder-sidebar-persons-count">{servings}</div>
                                <div className="finder-sidebar-persons-label">Personen</div>
                            </div>
                            <button onClick={() => setServings(servings + 1)} className="finder-sidebar-persons-btn">+</button>
                        </div>
                    </div>

                    {/* Suche starten */}
                    <div className="finder-sidebar-section">
                        {searchError && <p style={{ color: '#b91c1c', fontSize: 13, fontFamily: 'system-ui', marginBottom: 8 }}>{searchError}</p>}
                        <button onClick={handleSearch} disabled={searching || ingredients.length === 0} className="finder-sidebar-search-btn">
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
                        suggestions={suggestions}
                    />
                </Modal>
            </div>
        </div>
    );
}