"use client";

import { useMemo, useState } from "react";
import { FolderPlus, Search } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import {
  EmptyState,
  ErrorState,
  LoadingState,
} from "@/components/common";

import { ProjectCard } from "@/components/projects/project-card";

import { useProjects } from "@/hooks/use-projects";
import { useAuth } from "@/hooks/use-auth";

import type { Project } from "@/types/project";

export default function ProjectsPage() {
  const { user } = useAuth();

  const {
    projects,
    error,
    isLoading,
    createProject,
    updateProject,
    deleteProject,
  } = useProjects();

  const [search, setSearch] = useState("");
  const [isCreating, setIsCreating] = useState(false);
  const [editingProject, setEditingProject] =
    useState<Project | null>(null);
  const [deletingProject, setDeletingProject] =
    useState<Project | null>(null);

  const filteredProjects = useMemo(() => {
    const query = search.trim().toLowerCase();

    if (!query) {
      return projects;
    }

    return projects.filter((project) =>
      project.name.toLowerCase().includes(query),
    );
  }, [projects, search]);

  const handleCreate = async (name: string) => {
    await createProject({ name });
    setIsCreating(false);
  };

  const handleRename = async (name: string) => {
    if (!editingProject) return;

    await updateProject(editingProject.id, { name });
    setEditingProject(null);
  };

  const handleDelete = async () => {
    if (!deletingProject) return;

    await deleteProject(deletingProject.id);
    setDeletingProject(null);
  };

  if (isLoading) {
    return <LoadingState message="Loading projects..." />;
  }

  if (error) {
    return (
      <ErrorState
        title="Unable to load projects"
        description="Something went wrong while loading your projects."
      />
    );
  }

  return (
    <main className="min-h-full p-6">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 flex flex-col gap-6 border-b border-border/60 pb-8 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <div className="mb-3 inline-flex items-center rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
              Workspace
            </div>

            <h1 className="text-3xl font-semibold tracking-tight text-foreground">
              Projects
            </h1>

            <p className="mt-2 max-w-xl text-sm leading-6 text-muted-foreground">
              Organize your documents and build searchable knowledge bases.
            </p>
          </div>

          <Button
            onClick={() => setIsCreating(true)}
            className="shrink-0 shadow-md shadow-black/20"
          >
            <FolderPlus className="mr-2 h-4 w-4" />
            New Project
          </Button>
        </header>

        <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="relative w-full max-w-md">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />

            <Input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search projects..."
              className="h-10 border-border/70 bg-card pl-9 transition-colors focus-visible:border-primary/60"
            />
          </div>

          <p className="text-xs text-muted-foreground">
            {filteredProjects.length}{" "}
            {filteredProjects.length === 1 ? "project" : "projects"}
          </p>
        </div>

        {projects.length === 0 ? (
          <EmptyState
            title="No projects yet"
            description="Create your first project to start building a searchable knowledge base."
            action={
              <Button onClick={() => setIsCreating(true)}>
                <FolderPlus className="mr-2 h-4 w-4" />
                Create Project
              </Button>
            }
          />
        ) : filteredProjects.length === 0 ? (
          <EmptyState
            title="No matching projects"
            description={`No projects match "${search}". Try a different search term.`}
          />
        ) : (
          <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
            {filteredProjects.map((project) => (
              <ProjectCard
                key={project.id}
                project={project}
                onRename={setEditingProject}
                onDelete={setDeletingProject}
              />
            ))}
          </div>
        )}

        {isCreating && (
          <ProjectNameDialog
            title="Create Project"
            initialName=""
            submitLabel="Create"
            onSubmit={handleCreate}
            onClose={() => setIsCreating(false)}
          />
        )}

        {editingProject && (
          <ProjectNameDialog
            title="Rename Project"
            initialName={editingProject.name}
            submitLabel="Save"
            onSubmit={handleRename}
            onClose={() => setEditingProject(null)}
          />
        )}

        {deletingProject && (
          <DeleteProjectDialog
            projectName={deletingProject.name}
            onConfirm={handleDelete}
            onClose={() => setDeletingProject(null)}
          />
        )}
      </div>
    </main>
  );
}

interface ProjectNameDialogProps {
  title: string;
  initialName: string;
  submitLabel: string;
  onSubmit: (name: string) => Promise<void>;
  onClose: () => void;
}

function ProjectNameDialog({
  title,
  initialName,
  submitLabel,
  onSubmit,
  onClose,
}: ProjectNameDialogProps) {
  const [name, setName] = useState(initialName);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    const trimmedName = name.trim();

    if (!trimmedName || isSubmitting) return;

    setIsSubmitting(true);

    try {
      await onSubmit(trimmedName);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="w-full max-w-md rounded-xl border border-border bg-card p-6 shadow-xl">
        <h2 className="text-lg font-semibold">{title}</h2>

        <Input
          autoFocus
          value={name}
          onChange={(event) => setName(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              void handleSubmit();
            }

            if (event.key === "Escape") {
              onClose();
            }
          }}
          placeholder="Project name"
          className="mt-4"
        />

        <div className="mt-6 flex justify-end gap-2">
          <Button
            variant="ghost"
            onClick={onClose}
            disabled={isSubmitting}
          >
            Cancel
          </Button>

          <Button
            onClick={() => void handleSubmit()}
            disabled={!name.trim() || isSubmitting}
          >
            {isSubmitting ? "Saving..." : submitLabel}
          </Button>
        </div>
      </div>
    </div>
  );
}

interface DeleteProjectDialogProps {
  projectName: string;
  onConfirm: () => Promise<void>;
  onClose: () => void;
}

function DeleteProjectDialog({
  projectName,
  onConfirm,
  onClose,
}: DeleteProjectDialogProps) {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    if (isDeleting) return;

    setIsDeleting(true);

    try {
      await onConfirm();
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="w-full max-w-md rounded-xl border border-border bg-card p-6 shadow-xl">
        <h2 className="text-lg font-semibold">
          Delete project?
        </h2>

        <p className="mt-2 text-sm text-muted-foreground">
          This will permanently delete{" "}
          <span className="font-medium text-foreground">
            {projectName}
          </span>{" "}
          and its associated data.
        </p>

        <div className="mt-6 flex justify-end gap-2">
          <Button
            variant="ghost"
            onClick={onClose}
            disabled={isDeleting}
          >
            Cancel
          </Button>

          <Button
            variant="destructive"
            onClick={() => void handleDelete()}
            disabled={isDeleting}
          >
            {isDeleting ? "Deleting..." : "Delete"}
          </Button>
        </div>
      </div>
    </div>
  );
}