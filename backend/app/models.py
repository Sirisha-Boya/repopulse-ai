"""
Database Models for Deployment Orchestration Platform
"""
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class DeploymentStatus(str, Enum):
    """Deployment status enum"""
    PENDING = "pending"
    ANALYZING = "analyzing"
    ANALYZED = "analyzed"
    GENERATING = "generating"
    GENERATED = "generated"
    COMMITTING = "committing"
    PUSHING = "pushing"
    BUILDING = "building"
    DEPLOYING = "deploying"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class RepositoryLanguage(str, Enum):
    """Repository primary language"""
    JAVASCRIPT = "javascript"
    PYTHON = "python"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    RUBY = "ruby"
    PHP = "php"
    OTHER = "other"


class User(Base):
    """User model - GitHub authenticated users"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, index=True, nullable=False)
    github_username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    github_token = Column(Text, nullable=False)  # Encrypted in production
    jwt_token = Column(Text, nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    repositories = relationship("Repository", back_populates="owner")
    deployments = relationship("DeploymentHistory", back_populates="user")
    env_variables = relationship("EnvironmentVariable", back_populates="user")


class Repository(Base):
    """Repository model - GitHub repositories"""
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    github_repo_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    full_name = Column(String(500), index=True, nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(500), nullable=False)
    default_branch = Column(String(255), default="main")
    language = Column(SQLEnum(RepositoryLanguage), nullable=True)
    is_private = Column(Boolean, default=False)
    stars = Column(Integer, default=0)
    last_pushed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="repositories")
    configurations = relationship("DeploymentConfiguration", back_populates="repository", cascade="all, delete-orphan")
    health_reports = relationship("RepositoryHealthReport", back_populates="repository", cascade="all, delete-orphan")
    deployments = relationship("DeploymentHistory", back_populates="repository", cascade="all, delete-orphan")


class DeploymentConfiguration(Base):
    """Deployment configuration for each repository"""
    __tablename__ = "deployment_configurations"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    framework = Column(String(100), nullable=True)  # React, Next.js, FastAPI, etc.
    package_manager = Column(String(50), nullable=True)  # npm, pip, yarn, etc.
    build_command = Column(String(255), nullable=True)
    output_folder = Column(String(255), nullable=True)
    install_command = Column(String(255), nullable=True)
    start_command = Column(String(255), nullable=True)
    deployment_target = Column(String(50), nullable=True)  # azure, vercel, both
    azure_app_service_name = Column(String(255), nullable=True)
    azure_resource_group = Column(String(255), nullable=True)
    vercel_project_id = Column(String(255), nullable=True)
    vercel_team_id = Column(String(255), nullable=True)
    github_secrets = Column(JSON, nullable=True)  # Deployment secrets
    detected_env_vars = Column(JSON, nullable=True)  # Detected env variables
    dockerfile_path = Column(String(255), nullable=True)
    docker_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    repository = relationship("Repository", back_populates="configurations")


class RepositoryHealthReport(Base):
    """AI-generated repository health analysis"""
    __tablename__ = "repository_health_reports"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    overall_score = Column(Integer, nullable=False)  # 0-100
    code_quality_score = Column(Integer, nullable=False)
    architecture_score = Column(Integer, nullable=False)
    security_score = Column(Integer, nullable=False)
    performance_score = Column(Integer, nullable=False)
    
    # Detailed findings
    issues = Column(JSON, nullable=True)  # {high: [], medium: [], low: []}
    recommendations = Column(JSON, nullable=True)  # Array of recommendations
    code_analysis = Column(JSON, nullable=True)  # Detailed code analysis
    security_findings = Column(JSON, nullable=True)  # Security issues
    performance_findings = Column(JSON, nullable=True)  # Performance issues
    
    # Metadata
    files_scanned = Column(Integer, default=0)
    total_lines = Column(Integer, default=0)
    detected_frameworks = Column(JSON, nullable=True)
    dependencies = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    repository = relationship("Repository", back_populates="health_reports")


class EnvironmentVariable(Base):
    """Environment variables for deployments"""
    __tablename__ = "environment_variables"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=True)
    key = Column(String(255), nullable=False)
    value = Column(Text, nullable=False)  # Encrypted in production
    is_secret = Column(Boolean, default=False)
    environment = Column(String(50), nullable=True)  # production, staging, development
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="env_variables")


class DeploymentHistory(Base):
    """Deployment history and logs"""
    __tablename__ = "deployment_history"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    commit_id = Column(String(255), nullable=False)
    branch = Column(String(255), default="main")
    status = Column(SQLEnum(DeploymentStatus), default=DeploymentStatus.PENDING)
    deployment_target = Column(String(50), nullable=True)  # azure, vercel
    deployment_url = Column(String(500), nullable=True)
    environment = Column(String(50), nullable=True)  # production, staging
    duration_seconds = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    workflow_run_id = Column(String(255), nullable=True)  # GitHub Actions run ID
    previous_deployment_id = Column(Integer, ForeignKey("deployment_history.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    repository = relationship("Repository", back_populates="deployments")
    user = relationship("User", back_populates="deployments")
    logs = relationship("DeploymentLog", back_populates="deployment", cascade="all, delete-orphan")
    rollback_from = relationship(
        "DeploymentHistory",
        remote_side=[id],
        backref="rolled_back_to",
        foreign_keys=[previous_deployment_id]
    )


class DeploymentLog(Base):
    """Real-time deployment logs"""
    __tablename__ = "deployment_logs"

    id = Column(Integer, primary_key=True, index=True)
    deployment_id = Column(Integer, ForeignKey("deployment_history.id"), nullable=False)
    stage = Column(String(50), nullable=False)  # analyzing, generating, committing, etc.
    log_level = Column(String(20), default="info")  # info, warning, error
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    deployment = relationship("DeploymentHistory", back_populates="logs")


class GitHubWorkflow(Base):
    """Generated GitHub Actions workflows"""
    __tablename__ = "github_workflows"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    workflow_name = Column(String(255), nullable=False)
    workflow_path = Column(String(500), nullable=False)  # .github/workflows/deploy.yml
    workflow_content = Column(Text, nullable=False)  # YAML content
    triggered_by = Column(String(50), nullable=True)  # push, pull_request, workflow_dispatch
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
