import { api } from "@/lib/api";
import type {
  CreateProjectRequest,
  Project,
  UpdateProjectRequest,
} from "@/types/project";

export class ProjectService {
  static async getProjects(): Promise<Project[]> {
    const response = await api.get<Project[]>("/projects");
    return response.data;
  }

  static async getProject(id: string): Promise<Project> {
    const response = await api.get<Project>(`/projects/${id}`);
    return response.data;
  }

  static async createProject(
    data: CreateProjectRequest,
  ): Promise<Project> {
    const response = await api.post<Project>("/projects", data);
    return response.data;
  }

  static async updateProject(
    id: string,
    data: UpdateProjectRequest,
  ): Promise<Project> {
    const response = await api.patch<Project>(
      `/projects/${id}`,
      data,
    );

    return response.data;
  }

  static async deleteProject(id: string): Promise<void> {
    await api.delete(`/projects/${id}`);
  }
}