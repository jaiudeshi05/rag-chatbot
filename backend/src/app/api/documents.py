from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.api.deps import get_current_user
from app.core.database import get_session
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService

from app.schemas.document_upload import (
    DocumentUploadUrlRequest,
    DocumentUploadUrlResponse,
)
from app.services.document_upload_service import DocumentUploadService
from app.schemas.document_confirm import DocumentConfirmResponse

router = APIRouter(tags=["Documents"])


@router.get(
    "/projects/{project_id}/documents",
    response_model=list[DocumentResponse],
)
def list_documents(
    project_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return DocumentService.list_documents(
        session=session,
        project_id=project_id,
        current_user=current_user,
    )


@router.get(
    "/documents/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return DocumentService.get_document(
        session=session,
        document_id=document_id,
        current_user=current_user,
    )


@router.delete(
    "/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(
    document_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    DocumentService.delete_document(
        session=session,
        document_id=document_id,
        current_user=current_user,
    )

    return None

@router.post(
    "/projects/{project_id}/documents/upload-url",
    response_model=DocumentUploadUrlResponse,
)
def create_upload_url(
    project_id: UUID,
    data: DocumentUploadUrlRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return DocumentUploadService.create_upload_url(
        session=session,
        project_id=project_id,
        current_user=current_user,
        data=data,
    )

@router.post(
    "/projects/{project_id}/documents/{document_id}/confirm",
    response_model=DocumentConfirmResponse,
)
def confirm_document_upload(
    project_id: UUID,
    document_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return DocumentUploadService.confirm_upload(
        session=session,
        project_id=project_id,
        document_id=document_id,
        current_user=current_user,
    )