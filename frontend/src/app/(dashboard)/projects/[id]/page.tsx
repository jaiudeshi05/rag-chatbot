"use client";

import { useState } from "react";
import { FilePlus2, MessageSquarePlus } from "lucide-react";
import { useParams } from "next/navigation";

import { Button } from "@/components/ui/button";

import {
  EmptyState,
  ErrorState,
  LoadingState,
} from "@/components/common";

import {
  ProjectHeader,
  ProjectSection,
} from "@/components/projects";

import { useProject } from "@/hooks/use-projects";

export default function ProjectPage() {
  const params = useParams<{ id: string }>();
  const projectId = params.id;

  const {
    project,
    error,
    isLoading,
  } = useProject(projectId);

  const [isRenameOpen, setIsRenameOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);

  if (isLoading) {
    return <LoadingState message="Loading project..." />;
  }

  if (error || !project) {
    return (
      <ErrorState
        title="Unable to load project"
        description="The project could not be found or could not be loaded."
      />
    );
  }

  return (
    <main className="min-h-full p-6">
      <div className="mx-auto max-w-7xl">
        <ProjectHeader
          project={project}
          onRename={() => setIsRenameOpen(true)}
          onDelete={() => setIsDeleteOpen(true)}
        />

        <div className="mt-8 space-y-10">
          <ProjectSection
            title="Documents"
            description="Upload and manage the documents used by this knowledge base."
            action={
              <Button>
                <FilePlus2 className="mr-2 h-4 w-4" />
                Upload Document
              </Button>
            }
          >
            <EmptyState
              title="No documents yet"
              description="Upload a document to start building this project's knowledge base."
              action={
                <Button>
                  <FilePlus2 className="mr-2 h-4 w-4" />
                  Upload Document
                </Button>
              }
            />
          </ProjectSection>

          <ProjectSection
            title="Chats"
            description="Ask questions against the documents in this project."
            action={
              <Button>
                <MessageSquarePlus className="mr-2 h-4 w-4" />
                New Chat
              </Button>
            }
          >
            <EmptyState
              title="No chats yet"
              description="Start a chat to ask questions about your project documents."
              action={
                <Button>
                  <MessageSquarePlus className="mr-2 h-4 w-4" />
                  New Chat
                </Button>
              }
            />
          </ProjectSection>
        </div>
      </div>

      {isRenameOpen && (
        <div>
          {/* Rename dialog will be connected when project mutations
              are extracted into reusable project actions. */}
        </div>
      )}

      {isDeleteOpen && (
        <div>
          {/* Delete dialog will be connected when project mutations
              are extracted into reusable project actions. */}
        </div>
      )}
    </main>
  );
}