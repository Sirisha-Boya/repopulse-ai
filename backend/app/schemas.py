"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ==================== Auth Schemas ====================
class GitHubUser(BaseModel):
    """GitHub user info from OAuth"""
    id: int
    login: str
    email: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]


class AuthTokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int = 3600


class UserResponse(BaseModel):
    """User response DTO"""
    id: int
    github_id: int
    github_username: str
    email: Optional[str]
    avatar_url: Optional[str]
    is_admin: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


# ==================== Repository Schemas ====================
class RepositoryCreate(BaseModel):
    """Create repository"""
    github_repo_id: int
    name: str
    full_name: str
    description: Optional[str]
    url: str
    default_branch: str
    language: Optional[str]
    is_private: bool


class RepositoryResponse(BaseModel):
    """Repository response DTO"""
    id: int
    name: str
    full_name: str
    description: Optional[str]
    url: str
    default_branch: str
    language: Optional[str]
    is_private: bool
    stars: int
    last_pushed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RepositoryListResponse(BaseModel):
    """List repositories response"""
    total: int
    repositories: List[RepositoryResponse]
    page: int
    page_size: int


# ==================== Analysis Schemas ====================
class TechStackDetection(BaseModel):
    """Detected technology stack"""
    framework: str
    version: Optional[str]
    confidence: float = Field(..., ge=0, le=1)


class PackageManagerDetection(BaseModel):
    """Detected package manager"""
    manager: str
    lockfile: str


class AnalysisResult(BaseModel):
    """Repository analysis result"""
    framework: str
    package_manager: str
    build_command: Optional[str]
    install_command: Optional[str]
    start_command: Optional[str]
    output_folder: Optional[str]
    detected_env_vars: List[str]
    has_dockerfile: bool
    docker_file_path: Optional[str]
    detected_databases: List[str]


# ==================== Health Report Schemas ====================
class CodeQualityIssue(BaseModel):
    """Code quality issue"""
    severity: str  # high, medium, low
    type: str  # large_file, deep_nesting, duplicate_code, etc.
    description: str
    location: Optional[str]
    suggestion: Optional[str]


class SecurityFinding(BaseModel):
    """Security finding"""
    severity: str  # high, medium, low
    type: str  # hardcoded_secret, exposed_api_key, etc.
    description: str
    location: Optional[str]
    remediation: Optional[str]


class Recommendation(BaseModel):
    """AI recommendation"""
    priority: str  # high, medium, low
    category: str  # architecture, performance, security, etc.
    title: str
    description: str
    estimated_effort: str  # low, medium, high
    implementation_steps: Optional[List[str]]


class RepositoryHealthReport(BaseModel):
    """Repository health report"""
    overall_score: int = Field(..., ge=0, le=100)
    code_quality_score: int = Field(..., ge=0, le=100)
    architecture_score: int = Field(..., ge=0, le=100)
    security_score: int = Field(..., ge=0, le=100)
    performance_score: int = Field(..., ge=0, le=100)
    files_scanned: int
    total_lines: int
    detected_frameworks: List[str]
    issues: Dict[str, List[CodeQualityIssue]]
    security_findings: List[SecurityFinding]
    recommendations: List[Recommendation]
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Environment Variables Schemas ====================
class EnvironmentVariableCreate(BaseModel):
    """Create environment variable"""
    key: str
    value: str
    is_secret: bool = False
    environment: Optional[str] = "production"


class EnvironmentVariableResponse(BaseModel):
    """Environment variable response (value masked for secrets)"""
    id: int
    key: str
    value: Optional[str] = None  # Null for secrets in list
    is_secret: bool
    environment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class EnvironmentVariableUpdate(BaseModel):
    """Update environment variable"""
    value: str
    environment: Optional[str] = None


# ==================== Deployment Configuration Schemas ====================
class DeploymentConfigCreate(BaseModel):
    """Create deployment configuration"""
    framework: str
    package_manager: str
    build_command: str
    output_folder: Optional[str]
    install_command: str
    deployment_target: str  # azure, vercel, both
    azure_app_service_name: Optional[str]
    azure_resource_group: Optional[str]
    vercel_project_id: Optional[str]
    vercel_team_id: Optional[str]


class DeploymentConfigResponse(BaseModel):
    """Deployment configuration response"""
    id: int
    repository_id: int
    framework: str
    package_manager: str
    build_command: str
    output_folder: Optional[str]
    deployment_target: str
    docker_enabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Deployment Schemas ====================
class DeploymentCreate(BaseModel):
    """Create deployment"""
    branch: Optional[str] = "main"
    environment: Optional[str] = "production"
    deployment_target: str  # azure, vercel


class DeploymentLogResponse(BaseModel):
    """Deployment log entry"""
    id: int
    stage: str
    log_level: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True


class DeploymentResponse(BaseModel):
    """Deployment response DTO"""
    id: int
    repository_id: int
    commit_id: str
    branch: str
    status: str
    deployment_target: str
    deployment_url: Optional[str]
    environment: Optional[str]
    duration_seconds: Optional[int]
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    logs: Optional[List[DeploymentLogResponse]] = []

    class Config:
        from_attributes = True


class DeploymentHistoryResponse(BaseModel):
    """Deployment history entry"""
    id: int
    repository_id: int
    commit_id: str
    branch: str
    status: str
    deployment_target: str
    deployment_url: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]


# ==================== GitHub Workflow Schemas ====================
class GitHubWorkflowResponse(BaseModel):
    """GitHub workflow response"""
    id: int
    workflow_name: str
    workflow_path: str
    triggered_by: str
    created_at: datetime


# ==================== Dashboard Schemas ====================
class DashboardStats(BaseModel):
    """Dashboard statistics"""
    total_repositories: int
    total_deployments: int
    successful_deployments: int
    failed_deployments: int
    active_deployments: int


class RecentActivity(BaseModel):
    """Recent activity item"""
    id: int
    repository_name: str
    action: str  # deployment, analysis, rollback
    status: str
    timestamp: datetime


class DeploymentTrend(BaseModel):
    """Deployment trend data"""
    date: str
    successful: int
    failed: int
    total: int


class DashboardResponse(BaseModel):
    """Complete dashboard response"""
    stats: DashboardStats
    recent_activities: List[RecentActivity]
    deployment_trends: List[DeploymentTrend]
    top_repositories: List[RepositoryResponse]


# ==================== Error Schemas ====================
class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str]
    request_id: Optional[str]


class ValidationErrorResponse(BaseModel):
    """Validation error response"""
    error: str
    errors: List[Dict[str, Any]]
