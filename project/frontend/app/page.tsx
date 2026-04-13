"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import Homepage from "@/app/homepage/homepage";

export default function Page() {
    const { user, loading } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!loading && user) {
            router.replace("/recipeFinder");
        }
    }, [loading, user, router]);

    if (loading || user) return null;
    return <Homepage />;
}