"""
GitHub OAuth and API integration
"""
import httpx
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)


class GitHubService:
    """GitHub OAuth and API service"""
    
    def __init__(self):
        self.client_id = settings.GITHUB_CLIENT_ID
        self.client_secret = settings.GITHUB_CLIENT_SECRET
        self.redirect_uri = settings.GITHUB_REDIRECT_URI
        self.api_base = settings.GITHUB_API_BASE_URL
        self.api_token = settings.GITHUB_API_TOKEN
    
    def get_oauth_url(self, state: str) -> str:
        """Generate GitHub OAuth authorization URL"""
        return (
            f"https://github.com/login/oauth/authorize?"
            f"client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&scope=repo,user,workflow"
            f"&state={state}"
        )
    
    async def exchange_code_for_token(self, code: str) -> Optional[dict]:
        """Exchange authorization code for access token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://github.com/login/oauth/access_token",
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "code": code,
                        "redirect_uri": self.redirect_uri,
                    },
                    headers={"Accept": "application/json"}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"GitHub OAuth error: {e}")
            return None
    
    async def get_user(self, access_token: str) -> Optional[dict]:
        """Get authenticated GitHub user"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base}/user",
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"GitHub get_user error: {e}")
            return None
    
    async def get_user_repos(self, access_token: str, page: int = 1, per_page: int = 30) -> Optional[list]:
        """Get user repositories"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base}/user/repos",
                    params={"page": page, "per_page": per_page, "sort": "updated"},
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"GitHub get_user_repos error: {e}")
            return None
    
    async def get_repo_content(self, owner: str, repo: str, path: str = "", access_token: str = None) -> Optional[dict]:
        """Get repository contents"""
        token = access_token or self.api_token
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base}/repos/{owner}/{repo}/contents/{path}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"GitHub get_repo_content error: {e}")
            return None
    
    async def create_workflow(
        self,
        owner: str,
        repo: str,
        path: str,
        content: str,
        commit_message: str,
        access_token: str
    ) -> bool:
        """Create or update GitHub workflow file"""
        try:
            # First, get the current file SHA if it exists (for update)
            sha = None
            try:
                file_info = await self.get_repo_content(owner, repo, path, access_token)
                if file_info and "sha" in file_info:
                    sha = file_info["sha"]
            except:
                pass  # File doesn't exist yet
            
            import base64
            encoded_content = base64.b64encode(content.encode()).decode()
            
            async with httpx.AsyncClient() as client:
                payload = {
                    "message": commit_message,
                    "content": encoded_content,
                    "branch": "main"
                }
                if sha:
                    payload["sha"] = sha
                
                response = await client.put(
                    f"{self.api_base}/repos/{owner}/{repo}/contents/{path}",
                    json=payload,
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                response.raise_for_status()
                return True
        except httpx.HTTPError as e:
            logger.error(f"GitHub create_workflow error: {e}")
            return False
    
    async def trigger_workflow(
        self,
        owner: str,
        repo: str,
        workflow_id: str,
        ref: str,
        access_token: str
    ) -> bool:
        """Trigger a GitHub Actions workflow"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches",
                    json={"ref": ref},
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                # GitHub returns 204 for success
                return response.status_code in [200, 204]
        except httpx.HTTPError as e:
            logger.error(f"GitHub trigger_workflow error: {e}")
            return False
    
    async def create_repository_secret(
        self,
        owner: str,
        repo: str,
        secret_name: str,
        secret_value: str,
        access_token: str
    ) -> bool:
        """Create or update a repository secret for GitHub Actions"""
        try:
            # Note: In real implementation, we'd need to encrypt with repo's public key
            # For now, we'll use a simplified approach
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{self.api_base}/repos/{owner}/{repo}/actions/secrets/{secret_name}",
                    json={"encrypted_value": secret_value},
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                return response.status_code in [200, 201, 204]
        except httpx.HTTPError as e:
            logger.error(f"GitHub create_repository_secret error: {e}")
            return False


def get_github_service() -> GitHubService:
    """Get GitHub service instance"""
    return GitHubService()
