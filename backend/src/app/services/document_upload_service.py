from uuid import UUID, uuid4

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.core.storage import storage
from app.models.document import Document
from app.models.enums import DocumentStatus
from app.models.project import Project
from app.models.user import User
from app.schemas.document_upload import (
    DocumentUploadUrlRequest,
    DocumentUploadUrlResponse,
)
from app.schemas.document_confirm import DocumentConfirmResponse


class DocumentUploadService:

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
    def create_upload_url(
        session: Session,
        project_id: UUID,
        current_user: User,
        data: DocumentUploadUrlRequest,
    ) -> DocumentUploadUrlResponse:
        DocumentUploadService.get_owned_project(
            session=session,
            project_id=project_id,
            current_user=current_user,
        )

        document_id = uuid4()

        object_key = (
            f"raw/{project_id}/{document_id}/{data.filename}"
        )

        upload_url = storage.generate_upload_url(
            object_key=object_key,
            content_type=data.content_type,
        )

        document = Document(
            id=document_id,
            project_id=project_id,
            filename=data.filename,
            content_hash="",
            status=DocumentStatus.UPLOADING,
            chunk_count=0,
        )

        session.add(document)
        session.commit()

        return DocumentUploadUrlResponse(
            document_id=document_id,
            upload_url=upload_url,
            object_key=object_key,
        )

    @staticmethod
    def confirm_upload(
        session: Session,
        project_id: UUID,
        document_id: UUID,
        current_user: User,
    ) -> DocumentConfirmResponse:
        project = DocumentUploadService.get_owned_project(
            session=session,
            project_id=project_id,
            current_user=current_user,
        )

        document = session.exec(
            select(Document).where(
                Document.id == document_id,
                Document.project_id == project.id,
            )
        ).first()

        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )

        object_key = (
            f"raw/{project_id}/{document_id}/{document.filename}"
        )

        if not storage.object_exists(object_key):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded object was not found in storage",
            )

        content_hash = storage.calculate_sha256(object_key)

        duplicate = session.exec(
            select(Document)
            .join(Project, Project.id == Document.project_id)
            .where(
                Document.content_hash == content_hash,
                Project.user_id == current_user.id,
                Document.id != document.id,
            )
        ).first()

        if duplicate is not None:
            storage.delete_object(object_key)

            session.delete(document)
            session.commit()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A document with identical content already exists",
            )

        document.content_hash = content_hash
        document.status = DocumentStatus.QUEUED

        session.add(document)
        session.commit()
        session.refresh(document)

        return DocumentConfirmResponse(
            document_id=document.id,
            filename=document.filename,
            status=document.status.value,
            content_hash=document.content_hash,
            chunk_count=document.chunk_count,
        )