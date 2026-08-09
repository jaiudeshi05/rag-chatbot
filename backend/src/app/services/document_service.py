from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.document import Document
from app.models.project import Project
from app.models.user import User


class DocumentService:

    @staticmethod
    def get_owned_project(
        session: Session,
        project_id: UUID,
        current_user: User,
    ) -> Project:
        project = session.exec(
            select(Project).where(
                Project.id == project_id,
                Project.user_id == current_user.id,
            )
        ).first()

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        return project

    @staticmethod
    def list_documents(
        session: Session,
        project_id: UUID,
        current_user: User,
    ) -> list[Document]:
        DocumentService.get_owned_project(
            session=session,
            project_id=project_id,
            current_user=current_user,
        )

        statement = (
            select(Document)
            .where(Document.project_id == project_id)
            .order_by(Document.created_at.desc())
        )

        return list(session.exec(statement).all())

    @staticmethod
    def get_document(
        session: Session,
        document_id: UUID,
        current_user: User,
    ) -> Document:
        statement = (
            select(Document)
            .join(Project, Project.id == Document.project_id)
            .where(
                Document.id == document_id,
                Project.user_id == current_user.id,
            )
        )

        document = session.exec(statement).first()

        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )

        return document

    @staticmethod
    def delete_document(
        session: Session,
        document_id: UUID,
        current_user: User,
    ) -> None:
        document = DocumentService.get_document(
            session=session,
            document_id=document_id,
            current_user=current_user,
        )

        session.delete(document)
        session.commit()