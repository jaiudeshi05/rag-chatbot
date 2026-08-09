"use client";

import { Menu } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { UserMenu } from "@/components/layout/user-menu";

export function Header() {
  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b bg-background px-4 md:px-6">
      <div className="flex items-center gap-3">
        <Button
          variant="ghost"
          size="icon"
          className="md:hidden"
          aria-label="Open navigation"
        >
          <Menu className="size-5" />
        </Button>

        <Separator
          orientation="vertical"
          className="hidden h-6 md:block"
        />

        <div>
          <h1 className="text-sm font-semibold">
            Workspace
          </h1>
        </div>
      </div>

      <UserMenu />
    </header>
  );
}