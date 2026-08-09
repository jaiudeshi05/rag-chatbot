import { Loader2 } from "lucide-react";

interface LoadingStateProps {
  message?: string;
  className?: string;
}

export function LoadingState({
  message = "Loading...",
  className,
}: LoadingStateProps) {
  return (
    <div
      className={`flex min-h-40 flex-col items-center justify-center gap-3 ${className ?? ""}`}
    >
      <Loader2 className="h-6 w-6 animate-spin" />
      <p className="text-sm text-muted-foreground">{message}</p>
    </div>
  );
}