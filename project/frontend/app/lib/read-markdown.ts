import { readFileSync } from "node:fs";
import path from "node:path";
import { notFound } from "next/navigation";

export function readMarkdownFile(fileName: string) {
    try {
        return readFileSync(
            path.join(process.cwd(), "app", "homepage", "MarkdownFiles", fileName),
            "utf8"
        );
    } catch {
        notFound();
    }
}
