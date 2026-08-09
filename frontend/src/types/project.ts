export interface Project {
  id: string;
  user_id: string;
  name: string;
  chunk_size: number;
  chunk_overlap: number;
  top_k: number;
  created_at: string;
  updated_at: string;
}

export interface CreateProjectRequest {
  name: string;
  chunk_size?: number;
  chunk_overlap?: number;
  top_k?: number;
}

export interface UpdateProjectRequest {
  name?: string;
  chunk_size?: number;
  chunk_overlap?: number;
  top_k?: number;
}