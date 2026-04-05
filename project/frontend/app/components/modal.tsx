"use client";

import { useEffect, type ReactNode } from "react";
import styles from "../homepage/page.module.css";

export default function Modal({ open, onCloseAction, children }: { open: boolean; onCloseAction: () => void; children: ReactNode }) {
    useEffect(() => {
        if (!open) return;
        const handler = (e: KeyboardEvent) => e.key === "Escape" && onCloseAction();
        window.addEventListener("keydown", handler);
        return () => window.removeEventListener("keydown", handler);
    }, [open, onCloseAction]);

    useEffect(() => {
        document.body.style.overflow = open ? "hidden" : "";
        return () => { document.body.style.overflow = ""; };
    }, [open]);

    if (!open) return null;

    return (
        <div className={styles.overlay}>
            <div className={styles.modal}>
                <button className={styles.modalClose} onClick={onCloseAction} aria-label="Schließen">
                    ✕
                </button>
                {children}
            </div>
        </div>
    );
}