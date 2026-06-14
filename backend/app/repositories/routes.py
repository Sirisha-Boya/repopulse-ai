"""Repository routes"""
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth.dependencies import get_current_user
from app.repositories.service import get_repositories_service, RepositoriesService
from app.github.service import get_github_service, GitHubService
from app import schemas

router = APIRouter(prefix="/api/repositories", tags=["repositories"])


@router.post("/sync")
async def sync_repositories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    repositories_service: RepositoriesService = Depends(get_repositories_service),
    github_service: GitHubService = Depends(get_github_service)
):
    """Sync repositories from GitHub"""
    
    repos = await repositories_service.sync_user_repositories(
        current_user,
        github_service,
        db
    )
    
    return {
        "message": f"Synced {len(repos)} repositories",
        "count": len(repos)
    }


@router.get("/", response_model=schemas.RepositoryListResponse)
async def get_repositories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    repositories_service: RepositoriesService = Depends(get_repositories_service),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Get user repositories"""
    
    repos, total = await repositories_service.get_user_repositories(
        current_user,
        db,
        page,
        page_size
    )
    
    return schemas.RepositoryListResponse(
        total=total,
        repositories=[schemas.RepositoryResponse.from_orm(r) for r in repos],
        page=page,
        page_size=page_size
    )


@router.get("/search", response_model=schemas.RepositoryListResponse)
async def search_repositories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    repositories_service: RepositoriesService = Depends(get_repositories_service),
    q: str = Query(..., min_length=1, max_length=100),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Search repositories"""
    
    repos, total = repositories_service.search_repositories(
        current_user,
        db,
        q,
        page,
        page_size
    )
    
    return schemas.RepositoryListResponse(
        total=total,
        repositories=[schemas.RepositoryResponse.from_orm(r) for r in repos],
        page=page,
        page_size=page_size
    )


@router.get("/{repo_id}", response_model=schemas.RepositoryResponse)
async def get_repository(
    repo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    repositories_service: RepositoriesService = Depends(get_repositories_service)
):
    """Get repository details"""
    
    repo = repositories_service.get_repository_by_id(repo_id, current_user, db)
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found"
        )
    
    return schemas.RepositoryResponse.from_orm(repo)


@router.delete("/{repo_id}")
async def delete_repository(
    repo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    repositories_service: RepositoriesService = Depends(get_repositories_service)
):
    """Delete repository"""
    
    success = await repositories_service.delete_repository(repo_id, current_user, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found"
        )
    
    return {"message": "Repository deleted"}
