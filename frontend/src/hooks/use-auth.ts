"use client";

import useSWR from "swr";

import { AuthService } from "@/services/auth.service";
import type { User } from "@/types/auth";

export function useAuth() {
  const {
    data,
    error,
    isLoading,
    mutate,
  } = useSWR<User>(
    "/auth/me",
    AuthService.getCurrentUser,
  );

  return {
    user: data,
    isLoading,
    isAuthenticated: !!data,
    error,
    refreshUser: mutate,
  };
}