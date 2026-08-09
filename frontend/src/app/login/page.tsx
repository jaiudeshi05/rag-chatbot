"use client";

import { Button } from "@/components/ui/button";
import { AuthService } from "@/services/auth.service";

export default function LoginPage() {
  const handleLogin = () => {
    window.location.href = AuthService.getGoogleLoginUrl();
  };

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-6 rounded-lg border p-8">
        <div className="space-y-2 text-center">
          <h1 className="text-3xl font-bold">RAG Chatbot</h1>
          <p className="text-muted-foreground">
            Chat with your documents
          </p>
        </div>

        <Button
          className="w-full"
          onClick={handleLogin}
        >
          Continue with Google
        </Button>
      </div>
    </div>
  );
}