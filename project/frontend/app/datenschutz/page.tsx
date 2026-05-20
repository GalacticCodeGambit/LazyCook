import { readFileSync } from "node:fs";
import path from "node:path";
import { notFound } from "next/navigation";

function readMarkdownFile(fileName: string) {
    try {
        return readFileSync(
            path.join(process.cwd(), "app", "homepage", "MarkdownFiles", fileName),
            "utf8"
        );
    } catch {
        notFound();
    }
}

export default function DatenschutzPage() {
    const content = readMarkdownFile("Datenschutz.md");

    return (
        <main className="min-h-screen bg-white px-6 py-12">
            <div className="mx-auto max-w-4xl">
                <h1 className="text-3xl font-semibold mb-6">Datenschutzerklärung</h1>
                <p className="text-gray-600 mb-8">
                    Die vollständige Datenschutzerklärung wird hier aus der bestehenden Markdown-Datei angezeigt.
                </p>
                <article className="rounded-lg border border-gray-200 bg-gray-50 p-6">
                    <pre className="whitespace-pre-wrap break-words text-sm leading-6 text-gray-800">
                        {content}
                    </pre>
                </article>
            </div>
        </main>
    );
}

