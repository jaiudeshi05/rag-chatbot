import { api } from "@/lib/api";
import type { User } from "@/types/auth";

export class AuthService {
  static async getCurrentUser(): Promise<User> {
    const response = await api.get<User>("/auth/me");
    return response.data;
  }

  static async logout(): Promise<void> {
    await api.post("/auth/logout");
  }

  static getGoogleLoginUrl(): string {
    return `${process.env.NEXT_PUBLIC_API_URL}/auth/login`;
  }
}