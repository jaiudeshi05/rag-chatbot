"use client";

import { ThemeProvider } from "next-themes";
import { SWRConfig } from "swr";

import { swrConfig } from "@/lib/swr";

interface ProvidersProps {
  children: React.ReactNode;
}

export function Providers({
  children,
}: ProvidersProps) {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="dark"
      enableSystem={false}
    >
      <SWRConfig value={swrConfig}>
        {children}
      </SWRConfig>
    </ThemeProvider>
  );
}