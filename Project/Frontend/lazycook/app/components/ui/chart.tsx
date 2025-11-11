"use client";

import React, { useId, useMemo, useContext, createContext } from "react";
import * as Recharts from "recharts";
import { cn } from "./utils"; // siehe oben

const THEMES = { light: "", dark: ".dark" };

const ChartContext = createContext(null);

function useChart() {
    const ctx = useContext(ChartContext);
    if (!ctx) throw new Error("useChart must be used within <ChartContainer />");
    return ctx;
}

export function ChartContainer({ id, className, children, config, ...props }) {
    const uniqueId = useId();
    const chartId = `chart-${id || uniqueId.replace(/:/g, "")}`;

    return (
        <ChartContext.Provider value={{ config }}>
            <div
                data-slot="chart"
                data-chart={chartId}
                className={cn("flex aspect-video justify-center text-xs", className)}
                {...props}
            >
                <ChartStyle id={chartId} config={config} />
                <Recharts.ResponsiveContainer>{children}</Recharts.ResponsiveContainer>
            </div>
        </ChartContext.Provider>
    );
}

function ChartStyle({ id, config }) {
    const colorConfig = Object.entries(config).filter(
        ([, conf]) => conf.theme || conf.color
    );
    if (!colorConfig.length) return null;

    return (
        <style
            dangerouslySetInnerHTML={{
                __html: Object.entries(THEMES)
                    .map(
                        ([theme, prefix]) => `${prefix} [data-chart=${id}] {
                            ${colorConfig
                            .map(([key, itemConfig]) => {
                                const color =
                                    itemConfig.theme?.[theme] || itemConfig.color;
                                return color ? `  --color-${key}: ${color};` : null;
                            })
                            .join("\n")}
}
`
                    )
                    .join("\n"),
            }}
        />
    );
}
