import {useEffect, useRef, useState} from "react";
import { useRouter } from "next/navigation";
import {useAuth} from "@/lib/auth";
import {LogOut, User, UserCircle} from "lucide-react";

export default function ProfileDropdown() {
    const menuRef = useRef<HTMLDivElement>(null);
    const { user, loading, logout } = useAuth();
    const router = useRouter();
    const [open, setOpen] = useState(false);


    const handleLogout = () => {
        logout();
        router.replace("/");
    }
    const handleProfil = () => {
        setOpen(false);
        console.log("Profil ansehen");
        router.push("/profile");
    };


    return (
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
    );
}