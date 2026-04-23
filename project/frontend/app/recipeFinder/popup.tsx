import { useState } from "react";
import "./style.css";

const EINHEITEN = ["Stück", "g", "kg", "ml", "l", "EL", "TL", "Prise"];

export interface IngredientInput {
    name: string;
    amount: number;
    unit: string;
}

interface Props {
    ingredients: IngredientInput[];
    onAdd: (ingredient: IngredientInput) => void;
    servings: number;
    onServingsChange: (s: number) => void;
}

export default function AddIngredientsPopup({ ingredients, onAdd}: Props) {
    const [ingredientName, setIngredientName] = useState("");
    const [ingredientAmount, setIngredientAmount] = useState("");
    const [ingredientUnit, setIngredientUnit] = useState("Stück");
    const [inputError, setInputError] = useState("");

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

    return (
        <div className="popup">
            <h2 className="popup__title">Zutaten Hinzufügen</h2>

            <div className="popup__fields">
                <input
                    type="text"
                    value={ingredientName}
                    onChange={e => setIngredientName(e.target.value)}
                    onKeyDown={e => e.key === "Enter" && handleAddIngredient()}
                    placeholder="z.B. Tomaten"
                    className="popup__input"
                />
                <input
                    type="number"
                    value={ingredientAmount}
                    onChange={e => setIngredientAmount(e.target.value)}
                    onKeyDown={e => e.key === "Enter" && handleAddIngredient()}
                    placeholder="Menge"
                    min={0}
                    className="popup__input popup__input--amount"
                />
                <select
                    value={ingredientUnit}
                    onChange={e => setIngredientUnit(e.target.value)}
                    className="popup__select"
                >
                    {EINHEITEN.map(e => <option key={e} value={e}>{e}</option>)}
                </select>
            </div>

            {inputError && <p className="popup__error">{inputError}</p>}

            <button onClick={handleAddIngredient} className="popup__btn">
                Hinzufügen
            </button>
        </div>
    );
}