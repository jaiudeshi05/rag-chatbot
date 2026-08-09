"use client";

import useSWR from "swr";

import { ProjectService } from "@/services/project.service";
import type {
  CreateProjectRequest,
  Project,
  UpdateProjectRequest,
} from "@/types/project";

const PROJECTS_KEY = "/projects";

export function useProjects() {
  const {
    data,
    error,
    isLoading,
    mutate,
  } = useSWR<Project[]>(
    PROJECTS_KEY,
    ProjectService.getProjects,
  );

  const createProject = async (
    project: CreateProjectRequest,
  ) => {
    const created = await ProjectService.createProject(project);

    await mutate();

    return created;
  };

  const updateProject = async (
    id: string,
    project: UpdateProjectRequest,
  ) => {
    const updated = await ProjectService.updateProject(id, project);

    await mutate();

    return updated;
  };

  const deleteProject = async (id: string) => {
    await ProjectService.deleteProject(id);

    await mutate();
  };

  return {
    projects: data ?? [],
    error,
    isLoading,
    createProject,
    updateProject,
    deleteProject,
    refreshProjects: mutate,
  };
}

export function useProject(id: string) {
  const {
    data,
    error,
    isLoading,
    mutate,
  } = useSWR<Project>(
    id ? `/projects/${id}` : null,
    () => ProjectService.getProject(id),
  );

  return {
    project: data,
    error,
    isLoading,
    refreshProject: mutate,
  };
}