import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { ComponentPropsWithoutRef } from "react";

type MarkdownRendererProps = {
    content: string;
};

const markdownComponents = {
    h1: (props: ComponentPropsWithoutRef<"h1">) => (
        <h1 className="mb-6 text-3xl font-semibold text-gray-900" {...props} />
    ),
    h2: (props: ComponentPropsWithoutRef<"h2">) => (
        <h2 className="mb-4 mt-8 text-2xl font-semibold text-gray-900" {...props} />
    ),
    h3: (props: ComponentPropsWithoutRef<"h3">) => (
        <h3 className="mb-3 mt-6 text-xl font-semibold text-gray-900" {...props} />
    ),
    p: (props: ComponentPropsWithoutRef<"p">) => (
        <p className="mb-4 leading-7 text-gray-700" {...props} />
    ),
    ul: (props: ComponentPropsWithoutRef<"ul">) => (
        <ul className="mb-4 ml-6 list-disc space-y-2 text-gray-700" {...props} />
    ),
    ol: (props: ComponentPropsWithoutRef<"ol">) => (
        <ol className="mb-4 ml-6 list-decimal space-y-2 text-gray-700" {...props} />
    ),
    li: (props: ComponentPropsWithoutRef<"li">) => (
        <li className="leading-7" {...props} />
    ),
    strong: (props: ComponentPropsWithoutRef<"strong">) => (
        <strong className="font-semibold text-gray-900" {...props} />
    ),
    a: (props: ComponentPropsWithoutRef<"a">) => (
        <a className="text-blue-600 underline underline-offset-2 hover:text-blue-700" {...props} />
    ),
    blockquote: (props: ComponentPropsWithoutRef<"blockquote">) => (
        <blockquote className="mb-4 border-l-4 border-gray-300 pl-4 italic text-gray-600" {...props} />
    ),
    hr: () => <hr className="my-8 border-gray-200" />,
    code: (props: ComponentPropsWithoutRef<"code">) => (
        <code className="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-sm text-gray-800" {...props} />
    ),
};

export default function MarkdownRenderer({ content }: MarkdownRendererProps) {
    return (
        <article className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <div className="max-w-none">
                <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
                    {content}
                </ReactMarkdown>
            </div>
        </article>
    );
}

