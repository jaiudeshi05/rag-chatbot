from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    @staticmethod
    def create_project(
        session: Session,
        current_user: User,
        data: ProjectCreate,
    ) -> Project:
        project = Project(
            user_id=current_user.id,
            name=data.name,
            chunk_size=data.chunk_size,
            chunk_overlap=data.chunk_overlap,
            top_k=data.top_k,
        )

        session.add(project)
        session.commit()
        session.refresh(project)

        return project

    @staticmethod
    def get_projects(
        session: Session,
        current_user: User,
    ) -> list[Project]:
        statement = (
            select(Project)
            .where(Project.user_id == current_user.id)
            .order_by(Project.created_at.desc())
        )

        return list(session.exec(statement).all())

    @staticmethod
    def get_project(
        session: Session,
        current_user: User,
        project_id: UUID,
    ) -> Project:
        statement = select(Project).where(
            Project.id == project_id,
            Project.user_id == current_user.id,
        )

        project = session.exec(statement).first()

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        return project

    @staticmethod
    def update_project(
        session: Session,
        current_user: User,
        project_id: UUID,
        data: ProjectUpdate,
    ) -> Project:
        project = ProjectService.get_project(
            session=session,
            current_user=current_user,
            project_id=project_id,
        )

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(project, field, value)

        session.add(project)
        session.commit()
        session.refresh(project)

        return project

    @staticmethod
    def delete_project(
        session: Session,
        current_user: User,
        project_id: UUID,
    ) -> None:
        project = ProjectService.get_project(
            session=session,
            current_user=current_user,
            project_id=project_id,
        )

        session.delete(project)
        session.commit()