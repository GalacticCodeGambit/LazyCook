import MarkdownRenderer from "@/app/components/markdown-renderer";
import { readMarkdownFile } from "@/app/lib/read-markdown";

export default function DatenschutzPage() {
    const content = readMarkdownFile("Datenschutz.md");

    return (
        <main className="min-h-screen bg-white px-6 py-12">
            <div className="mx-auto max-w-4xl">
                <MarkdownRenderer content={content} />
            </div>
        </main>
    );
}
