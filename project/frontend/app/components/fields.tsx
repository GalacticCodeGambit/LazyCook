import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import styles from "../homepage/page.module.css";

export default function Field({ label, type = "text", value, onChange, placeholder, onKeyDown, onBlur, state = "default" }: {
    label: string; type?: string; value: string;
    onChange: (v: string) => void; placeholder?: string;
    onKeyDown?: (e: React.KeyboardEvent) => void;
    onBlur?: () => void;
    state?: "default" | "error" | "success";
}) {
    const [showPassword, setShowPassword] = useState(false);
    const isPassword = type === "password";
    const effectiveType = isPassword && showPassword ? "text" : type;

    const inputClass =
        state === "error" ? styles.inputError :
            state === "success" ? styles.inputSuccess :
                styles.input;

    return (
        <div className={styles.fieldGroup}>
            <label className={styles.label}>{label}</label>
            <div style={{ position: "relative" }}>
                <input
                    className={inputClass}
                    type={effectiveType}
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    placeholder={placeholder}
                    onKeyDown={onKeyDown}
                    onBlur={onBlur}
                    style={isPassword ? { paddingRight: 38 } : undefined}
                />
                {isPassword && (
                    <button
                        type="button"
                        onClick={() => setShowPassword((s) => !s)}
                        aria-label={showPassword ? "Passwort verbergen" : "Passwort anzeigen"}
                        tabIndex={-1}
                        style={{
                            position: "absolute",
                            right: 8,
                            top: "50%",
                            transform: "translateY(-50%)",
                            background: "none",
                            border: "none",
                            cursor: "pointer",
                            padding: 4,
                            display: "flex",
                            alignItems: "center",
                            color: "#666",
                        }}
                    >
                        {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                )}
            </div>
        </div>
    );
}