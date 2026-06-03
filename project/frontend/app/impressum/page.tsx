import MarkdownRenderer from "@/app/components/markdown-renderer";
import { readMarkdownFile } from "@/app/lib/read-markdown";

export default function ImpressumPage() {
    const content = readMarkdownFile("Impressum.md");

    return (
        <main className="min-h-screen bg-white px-6 py-12">
            <div className="mx-auto max-w-4xl">
                <h1 className="text-3xl font-semibold mb-6">Impressum</h1>
                <MarkdownRenderer content={content} />
            </div>
        </main>
    );
}
