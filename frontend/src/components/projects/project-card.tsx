"use client";

import Link from "next/link";
import {
  ArrowUpRight,
  FileText,
  MoreVertical,
  Pencil,
  Trash2,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import type { Project } from "@/types/project";

interface ProjectCardProps {
  project: Project;
  onRename: (project: Project) => void;
  onDelete: (project: Project) => void;
}

export function ProjectCard({
  project,
  onRename,
  onDelete,
}: ProjectCardProps) {
  return (
    <Card className="group relative overflow-hidden border-border/70 bg-card transition-all duration-200 hover:-translate-y-0.5 hover:border-primary/40 hover:shadow-lg hover:shadow-black/20">
      <div className="absolute inset-x-0 top-0 h-px bg-linear-to-r from-transparent via-primary/60 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />

      <CardHeader className="flex flex-row items-start justify-between gap-4 pb-3">
        <Link
          href={`/projects/${project.id}`}
          className="group/title min-w-0"
        >
          <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-lg border border-primary/20 bg-primary/10">
            <FileText className="h-5 w-5 text-primary" />
          </div>

          <CardTitle className="truncate text-base font-medium transition-colors group-hover/title:text-primary">
            {project.name}
          </CardTitle>

          <p className="mt-1 text-xs text-muted-foreground">
            Created{" "}
            {new Date(project.created_at).toLocaleDateString()}
          </p>
        </Link>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              size="icon"
              className="shrink-0 text-muted-foreground hover:bg-muted hover:text-foreground"
              aria-label={`Actions for ${project.name}`}
            >
              <MoreVertical className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>

          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => onRename(project)}>
              <Pencil className="mr-2 h-4 w-4" />
              Rename
            </DropdownMenuItem>

            <DropdownMenuSeparator />

            <DropdownMenuItem
              className="text-destructive focus:text-destructive"
              onClick={() => onDelete(project)}
            >
              <Trash2 className="mr-2 h-4 w-4" />
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </CardHeader>

      <CardContent>
        <div className="flex flex-wrap gap-2">
          <Badge
            variant="secondary"
            className="border border-border/60 bg-secondary/60 text-secondary-foreground"
          >
            Chunk {project.chunk_size}
          </Badge>

          <Badge
            variant="secondary"
            className="border border-border/60 bg-secondary/60 text-secondary-foreground"
          >
            Top K {project.top_k}
          </Badge>
        </div>

        <Link
          href={`/projects/${project.id}`}
          className="mt-5 flex items-center gap-1 text-xs font-medium text-muted-foreground transition-colors hover:text-primary"
        >
          Open project
          <ArrowUpRight className="h-3.5 w-3.5" />
        </Link>
      </CardContent>
    </Card>
  );
}