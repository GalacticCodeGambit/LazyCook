import styles from "../homepage/page.module.css";

export default function Field({ label, type = "text", value, onChange, placeholder, onKeyDown, onBlur, state = "default" }: {
    label: string; type?: string; value: string;
    onChange: (v: string) => void; placeholder?: string;
    onKeyDown?: (e: React.KeyboardEvent) => void;
    onBlur?: () => void;
    state?: "default" | "error" | "success";
}) {
    const inputClass =
        state === "error" ? styles.inputError :
            state === "success" ? styles.inputSuccess :
                styles.input;

    return (
        <div className={styles.fieldGroup}>
            <label className={styles.label}>{label}</label>
            <input
                className={inputClass}
                type={type}
                value={value}
                onChange={(e) => onChange(e.target.value)}
                placeholder={placeholder}
                onKeyDown={onKeyDown}
                onBlur={onBlur}
            />
        </div>
    );
}