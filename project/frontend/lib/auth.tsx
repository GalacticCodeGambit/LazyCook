"use client";

import {
    createContext,
    useContext,
    useState,
    useEffect,
    useCallback,
    useRef,
    type ReactNode,
} from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3000";

// ── Typen ─────────────────────────────────────────────────────
export interface User {
    email: string;
    name: string;
}

interface AuthContextType {
    user: User | null;
    loading: boolean;
    login: (email: string, password: string) => Promise<void>;
    register: (email: string, name: string, password: string) => Promise<void>;
    logout: () => void;
}

// ── Token-Verwaltung ──────────────────────────────────────────
// Access Token → sessionStorage (lebt nur im Tab, kurzlebig)
// Refresh Token → localStorage (überlebt Browser-Neustart, 7 Tage gültig)

function getAccessToken(): string | null {
    return sessionStorage.getItem("access_token");
}

function getRefreshToken(): string | null {
    return localStorage.getItem("refresh_token");
}

function saveTokens(accessToken: string, refreshToken: string) {
    sessionStorage.setItem("access_token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);
}

function clearTokens() {
    sessionStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
}

// ── API-Aufrufe ───────────────────────────────────────────────
async function apiLogin(email: string, password: string): Promise<{ access_token: string; refresh_token: string }> {
    const body = new URLSearchParams({ username: email, password });
    const res = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body,
    });
    if (!res.ok) throw new Error("Login fehlgeschlagen");
    return res.json();
}

async function apiRegister(email: string, name: string, password: string): Promise<void> {
    const res = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, name, password }),
    });
    if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? "Registrierung fehlgeschlagen");
    }
}

async function apiRefreshTokens(refreshToken: string): Promise<{ access_token: string; refresh_token: string }> {
    const res = await fetch(`${API_URL}/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: refreshToken }),
    });
    if (!res.ok) throw new Error("Token-Erneuerung fehlgeschlagen");
    return res.json();
}

async function apiLogout(refreshToken: string): Promise<void> {
    await fetch(`${API_URL}/auth/logout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: refreshToken }),
    }).catch(() => {}); // Fehler ignorieren – Token wird lokal sowieso gelöscht
}

async function apiGetMe(accessToken: string): Promise<User> {
    const res = await fetch(`${API_URL}/users/me`, {
        headers: { Authorization: `Bearer ${accessToken}` },
    });
    if (!res.ok) throw new Error("Nicht autorisiert");
    return res.json();
}

// ── Authentifizierter Fetch mit automatischer Token-Erneuerung ──
async function fetchWithAuth(url: string, options: RequestInit = {}): Promise<Response> {
    const accessToken = getAccessToken();
    if (!accessToken) throw new Error("Nicht eingeloggt");

    // Erster Versuch mit aktuellem Access Token
    let res = await fetch(url, {
        ...options,
        headers: {
            ...options.headers,
            Authorization: `Bearer ${accessToken}`,
        },
    });

    // Bei 401: Access Token erneuern und erneut versuchen
    if (res.status === 401) {
        const refreshToken = getRefreshToken();
        if (!refreshToken) throw new Error("Nicht eingeloggt");

        try {
            const tokens = await apiRefreshTokens(refreshToken);
            saveTokens(tokens.access_token, tokens.refresh_token);

            // Erneuter Versuch mit neuem Access Token
            res = await fetch(url, {
                ...options,
                headers: {
                    ...options.headers,
                    Authorization: `Bearer ${tokens.access_token}`,
                },
            });
        } catch {
            // Refresh fehlgeschlagen → komplett ausloggen
            clearTokens();
            throw new Error("Session abgelaufen");
        }
    }

    return res;
}

// ── Context ───────────────────────────────────────────────────
const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    // Beim Laden: Token prüfen und ggf. erneuern
    useEffect(() => {
        const accessToken = getAccessToken();
        const refreshToken = getRefreshToken();

        if (accessToken) {
            // Versuche mit Access Token
            apiGetMe(accessToken)
                .then(setUser)
                .catch(async () => {
                    // Access Token abgelaufen → mit Refresh Token erneuern
                    if (refreshToken) {
                        try {
                            const tokens = await apiRefreshTokens(refreshToken);
                            saveTokens(tokens.access_token, tokens.refresh_token);
                            const me = await apiGetMe(tokens.access_token);
                            setUser(me);
                        } catch {
                            clearTokens();
                        }
                    } else {
                        clearTokens();
                    }
                })
                .finally(() => setLoading(false));
        } else if (refreshToken) {
            // Kein Access Token aber Refresh Token vorhanden → erneuern
            apiRefreshTokens(refreshToken)
                .then(async (tokens) => {
                    saveTokens(tokens.access_token, tokens.refresh_token);
                    const me = await apiGetMe(tokens.access_token);
                    setUser(me);
                })
                .catch(() => clearTokens())
                .finally(() => setLoading(false));
        } else {
            setLoading(false);
        }
    }, []);

    const login = useCallback(async (email: string, password: string) => {
        const tokens = await apiLogin(email, password);
        saveTokens(tokens.access_token, tokens.refresh_token);
        const me = await apiGetMe(tokens.access_token);
        setUser(me);
    }, []);

    const register = useCallback(async (email: string, name: string, password: string) => {
        await apiRegister(email, name, password);
        await login(email, password);
    }, [login]);

    const logout = useCallback(() => {
        const refreshToken = getRefreshToken();
        if (refreshToken) {
            apiLogout(refreshToken); // Serverseitig löschen (fire & forget)
        }
        clearTokens();
        setUser(null);
    }, []);

    return (
        <AuthContext.Provider value={{ user, loading, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth(): AuthContextType {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth muss innerhalb von AuthProvider verwendet werden");
    return ctx;
}

// Export für geschützte API-Aufrufe in anderen Komponenten
export { fetchWithAuth };