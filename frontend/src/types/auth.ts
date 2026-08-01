export interface User {
  id: string;
  email: string;
  name: string;
  picture_url?: string | null;
}

export interface AuthResponse {
  user: User;
}