"""GitHub repositories service"""
from typing import Optional, List
import logging
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_

from app.models import Repository, User, RepositoryLanguage
from app.github.service import GitHubService
from app import schemas
from app.auth.utils import decrypt_token

logger = logging.getLogger(__name__)


class RepositoriesService:
    """Service for managing repositories"""
    
    async def sync_user_repositories(
        self,
        user: User,
        github_service: GitHubService,
        db: Session
    ) -> List[Repository]:
        """Sync user's repositories from GitHub"""
        
        # Decrypt GitHub token
        github_token = decrypt_token(user.github_token)
        
        # Fetch repositories from GitHub
        repos = await github_service.get_user_repos(github_token)
        if not repos:
            logger.warning(f"Failed to fetch repos for user {user.github_username}")
            return []
        
        synced = []
        for repo in repos:
            # Check if repository already exists
            existing = db.query(Repository).filter(
                Repository.github_repo_id == repo["id"],
                Repository.owner_id == user.id
            ).first()
            
            # Determine language enum
            language = None
            if repo.get("language"):
                try:
                    language = RepositoryLanguage[repo["language"].upper()]
                except (KeyError, AttributeError):
                    language = RepositoryLanguage.OTHER
            
            if existing:
                # Update existing repository
                existing.name = repo["name"]
                existing.full_name = repo["full_name"]
                existing.description = repo.get("description")
                existing.url = repo["html_url"]
                existing.default_branch = repo.get("default_branch", "main")
                existing.language = language
                existing.is_private = repo["private"]
                existing.stars = repo.get("stargazers_count", 0)
                existing.last_pushed_at = repo.get("pushed_at")
                db.commit()
                synced.append(existing)
            else:
                # Create new repository
                new_repo = Repository(
                    owner_id=user.id,
                    github_repo_id=repo["id"],
                    name=repo["name"],
                    full_name=repo["full_name"],
                    description=repo.get("description"),
                    url=repo["html_url"],
                    default_branch=repo.get("default_branch", "main"),
                    language=language,
                    is_private=repo["private"],
                    stars=repo.get("stargazers_count", 0),
                    last_pushed_at=repo.get("pushed_at")
                )
                db.add(new_repo)
                db.commit()
                db.refresh(new_repo)
                synced.append(new_repo)
                logger.info(f"Created new repository: {new_repo.full_name}")
        
        return synced
    
    async def get_user_repositories(
        self,
        user: User,
        db: Session,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[Repository], int]:
        """Get user's repositories from database"""
        
        query = db.query(Repository).filter(Repository.owner_id == user.id)
        total = query.count()
        
        # Order by last updated
        repositories = query.order_by(
            desc(Repository.last_pushed_at)
        ).offset((page - 1) * page_size).limit(page_size).all()
        
        return repositories, total
    
    def get_repository_by_id(
        self,
        repo_id: int,
        user: User,
        db: Session
    ) -> Optional[Repository]:
        """Get single repository"""
        return db.query(Repository).filter(
            Repository.id == repo_id,
            Repository.owner_id == user.id
        ).first()
    
    def search_repositories(
        self,
        user: User,
        db: Session,
        query: str,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[Repository], int]:
        """Search user repositories"""
        
        search_query = db.query(Repository).filter(
            Repository.owner_id == user.id,
            or_(
                Repository.name.ilike(f"%{query}%"),
                Repository.description.ilike(f"%{query}%"),
                Repository.full_name.ilike(f"%{query}%")
            )
        )
        
        total = search_query.count()
        
        repositories = search_query.order_by(
            desc(Repository.last_pushed_at)
        ).offset((page - 1) * page_size).limit(page_size).all()
        
        return repositories, total
    
    async def delete_repository(
        self,
        repo_id: int,
        user: User,
        db: Session
    ) -> bool:
        """Delete repository (local record only)"""
        
        repo = self.get_repository_by_id(repo_id, user, db)
        if not repo:
            return False
        
        db.delete(repo)
        db.commit()
        logger.info(f"Deleted repository: {repo.full_name}")
        return True


def get_repositories_service() -> RepositoriesService:
    """Get repositories service instance"""
    return RepositoriesService()
