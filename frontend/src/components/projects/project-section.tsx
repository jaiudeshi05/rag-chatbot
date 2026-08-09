import type { ReactNode } from "react";

interface ProjectSectionProps {
  title: string;
  description: string;
  action?: ReactNode;
  children: ReactNode;
}

export function ProjectSection({
  title,
  description,
  action,
  children,
}: ProjectSectionProps) {
  return (
    <section>
      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold">{title}</h2>

          <p className="mt-1 text-sm text-muted-foreground">
            {description}
          </p>
        </div>

        {action}
      </div>

      {children}
    </section>
  );
}