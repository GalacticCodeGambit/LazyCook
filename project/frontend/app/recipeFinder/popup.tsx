import { useRef, useState } from "react";
import "./style.css";

const EINHEITEN = ["Stück", "g", "kg", "ml", "l", "EL", "TL", "Prise"];

export interface IngredientInput {
    name: string;
    amount: number;
    unit: string;
}

export interface Suggestion {
    name: string;
    unit: string | null;
}

interface Props {
    ingredients: IngredientInput[];
    onAdd: (ingredient: IngredientInput) => void;
    servings: number;
    onServingsChange: (s: number) => void;
    suggestions?: Suggestion[];
}

export default function AddIngredientsPopup({ ingredients, onAdd, suggestions = [] }: Props) {
    const [ingredientName, setIngredientName] = useState("");
    const [ingredientAmount, setIngredientAmount] = useState("");
    const [ingredientUnit, setIngredientUnit] = useState("Stück");
    const [inputError, setInputError] = useState("");
    const amountInputRef = useRef<HTMLInputElement>(null);

    const handleAddIngredient = () => {
        const trimmedName = ingredientName.trim();
        const amountNum = parseFloat(ingredientAmount);

        if (!trimmedName) { setInputError("Bitte eine Zutat eingeben."); return; }
        if (!ingredientAmount || isNaN(amountNum) || amountNum <= 0) { setInputError("Bitte eine gültige Menge eingeben."); return; }
        if (ingredients.some(z => z.name.toLowerCase() === trimmedName.toLowerCase())) {
            setInputError("Diese Zutat wurde bereits hinzugefügt.");
            return;
        }

        onAdd({ name: trimmedName, amount: amountNum, unit: ingredientUnit });
        setIngredientName("");
        setIngredientAmount("");
        setIngredientUnit("Stück");
        setInputError("");
    };

    const handleSuggestionClick = (s: Suggestion) => {
        setIngredientName(s.name);
        if (s.unit && EINHEITEN.includes(s.unit)) {
            setIngredientUnit(s.unit);
        }
        setInputError("");
        // Fokus aufs Mengen-Feld – User muss nur noch die Menge tippen
        setTimeout(() => amountInputRef.current?.focus(), 0);
    };

    // Vorschläge bleiben sichtbar – bereits hinzugefügte werden disabled markiert,
    // damit das Popup seine Größe behält.
    const isAlreadyAdded = (s: Suggestion) =>
        ingredients.some(z => z.name.toLowerCase() === s.name.toLowerCase());

    return (
        <div className="popup">
            <h2 className="popup-title">Zutaten Hinzufügen</h2>

            <div className="popup-fields">
                <input
                    type="text"
                    value={ingredientName}
                    onChange={e => setIngredientName(e.target.value)}
                    onKeyDown={e => e.key === "Enter" && handleAddIngredient()}
                    placeholder="z.B. Tomaten"
                    className="popup-input"
                />
                <input
                    ref={amountInputRef}
                    type="number"
                    value={ingredientAmount}
                    onChange={e => setIngredientAmount(e.target.value)}
                    onKeyDown={e => e.key === "Enter" && handleAddIngredient()}
                    placeholder="Menge"
                    min={0}
                    className="popup-input popup-input-amount"
                />
                <select
                    value={ingredientUnit}
                    onChange={e => setIngredientUnit(e.target.value)}
                    className="popup-select"
                >
                    {EINHEITEN.map(e => <option key={e} value={e}>{e}</option>)}
                </select>
            </div>

            {suggestions.length > 0 && (
                <div className="popup-suggestions">
                    <p className="popup-suggestions-label">Häufig verwendet</p>
                    <div className="popup-suggestions-list">
                        {suggestions.map(s => {
                            const added = isAlreadyAdded(s);
                            return (
                                <button
                                    key={s.name}
                                    type="button"
                                    disabled={added}
                                    onClick={() => !added && handleSuggestionClick(s)}
                                    className={`popup-suggestion-badge${added ? " popup-suggestion-badge-added" : ""}`}
                                    title={added ? "Bereits hinzugefügt" : (s.unit ? `${s.name} (${s.unit})` : s.name)}
                                >
                                    {s.name}
                                </button>
                            );
                        })}
                    </div>
                </div>
            )}

            {inputError && <p className="popup-error">{inputError}</p>}

            <button onClick={handleAddIngredient} className="popup-btn">
                Hinzufügen
            </button>
        </div>
    );
}
