# Architecture Documentation

## System Overview

The Deployment Orchestration Platform is built with a microservices-ready architecture that separates concerns into distinct layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (Port 3000)                 │
│  Material UI, Redux Toolkit, TypeScript                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/WebSocket
                         │
┌────────────────────────┴────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                      │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              API Router Layer                         │   │
│  │  /auth  /repositories  /analysis  /deployment        │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────┴──────────────────────────────┐   │
│  │          Service Layer (Business Logic)              │   │
│  │  ┌───────────────────────────────────────────────┐  │   │
│  │  │ AuthService   RepositoriesService             │  │   │
│  │  │ AnalysisService  DeploymentService            │  │   │
│  │  │ GitHubService   AzureService  VercelService   │  │   │
│  │  └───────────────────────────────────────────────┘  │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────┴──────────────────────────────┐   │
│  │        Data Access Layer (SQLAlchemy ORM)           │   │
│  │              Models & Repositories                   │   │
│  └──────────────────────┬───────────────────────────────┘   │
└──────────────────────────┼────────────────────────────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
      ┌─────┴────┐  ┌──────┴────┐  ┌─────┴────┐
      │PostgreSQL│  │   Redis   │  │  GitHub  │
      │Port 5432 │  │Port 6379  │  │   API    │
      └──────────┘  └───────────┘  └──────────┘
```

## Core Components

### 1. Frontend (React + Material UI)

**Location**: `/frontend/src`

**Responsibilities**:

- User interface and interactions
- State management (Redux Toolkit)
- Client-side routing
- API communication

**Key Directories**:

```
src/
├── pages/          # Page components
├── components/     # Reusable UI components
├── redux/          # Redux store, slices
├── services/       # API client
├── hooks/          # Custom React hooks
└── theme/          # Material UI theme
```

### 2. Backend API (FastAPI)

**Location**: `/backend/app`

**Responsibilities**:

- HTTP API endpoints
- Business logic
- Database operations
- External integrations

**Core Modules**:

#### Auth Module (`/auth`)

- GitHub OAuth flow
- JWT token generation
- User authentication
- Token refresh logic

#### GitHub Module (`/github`)

- GitHub API integration
- Repository fetching
- Workflow management
- Webhook handling

#### Repositories Module (`/repositories`)

- Repository CRUD operations
- Repository search/filtering
- Sync with GitHub

#### Analysis Module (`/analysis`) - Phase 2

- Code quality analysis
- Technology stack detection
- Security scanning
- AI-powered recommendations

#### Deployment Module (`/deployment`) - Phase 3

- Deployment orchestration
- Workflow YAML generation
- Status tracking
- Deployment history

#### Azure Module (`/azure`)

- Azure App Service integration
- Credential management
- Deployment configuration

#### Vercel Module (`/vercel`)

- Vercel API integration
- Project management
- Deployment configuration

#### AI Agents Module (`/ai_agents`)

- OpenAI integration
- Code review analysis
- Recommendation generation

### 3. Database Layer (PostgreSQL)

**Schema Highlights**:

```sql
users                    -- Authenticated users
repositories            -- GitHub repos metadata
deployment_configurations -- Per-repo settings
environment_variables   -- Encrypted env vars
deployment_history      -- Deployment records
deployment_logs         -- Real-time logs
repository_health_reports -- AI analysis results
github_workflows        -- Generated workflows
```

**Key Relationships**:

```
User (1) ─── (N) Repositories
User (1) ─── (N) Deployments
Repository (1) ─── (N) DeploymentConfigurations
Repository (1) ─── (N) HealthReports
Deployment (1) ─── (N) DeploymentLogs
```

## Data Flow

### Authentication Flow

```
User → Login Button
     ↓
Frontend → GET /auth/github/login
           ↓ Redirect to GitHub OAuth
           ↓ User authorizes
User ← GET /auth/callback?code=xxx
       ↓ Send code to backend
Backend → Exchange code for GitHub token
          ↓ Fetch user data
          ↓ Create/Update user in DB
          ↓ Generate JWT tokens
Frontend ← JWT tokens + User data
           Store in localStorage
           Redirect to dashboard
```

### Repository Sync Flow

```
User → Sync Button
     ↓
Frontend → POST /repositories/sync
           ↓
Backend → Service Layer
          ↓ Get GitHub token from DB
          ↓ Call GitHub API for repos
          ↓ For each repo:
            - Check if exists
            - Create or update in DB
          ↓ Return sync status
Frontend ← Success response
           Refresh repository list
```

### Deployment Flow (Phase 3)

```
User → Publish Button
     ↓
Frontend → POST /deployment/publish
           ↓
Backend → Analysis Phase
          ↓ Clone repo
          ↓ Detect tech stack
          ↓ Scan for env vars
          ↓ Workflow Generation Phase
            - Generate Actions YAML
            - Create deployment config
          ↓ Commit & Push Phase
            - Commit workflow file
            - Push to GitHub
          ↓ Trigger Phase
            - Trigger GitHub Actions
          ↓ Monitor Phase
            - Poll for workflow status
            - Stream logs
Frontend ← Real-time status updates
           Display logs/progress
           Show deployment URL
```

## Service Layer Architecture

Each service follows a consistent pattern:

```python
class XyzService:
    def __init__(self):
        """Initialize with dependencies"""
        pass

    async def operation(self, data):
        """Perform business logic"""
        # Validation
        # Database operations
        # External API calls
        # Return result or raise exception
        pass

def get_xyz_service() -> XyzService:
    """Dependency injection"""
    return XyzService()
```

## API Endpoint Naming Convention

```
GET    /api/{resource}              # List
GET    /api/{resource}/{id}         # Get
POST   /api/{resource}              # Create
PUT    /api/{resource}/{id}         # Replace
PATCH  /api/{resource}/{id}         # Partial update
DELETE /api/{resource}/{id}         # Delete
POST   /api/{resource}/{id}/action  # Custom action
```

## Error Handling

Consistent error response format:

```json
{
  "error": "ErrorType",
  "detail": "Human-readable message",
  "request_id": "unique-id"
}
```

**Error Classes**:

- `ValidationError` (422)
- `UnauthorizedError` (401)
- `ForbiddenError` (403)
- `NotFoundError` (404)
- `ConflictError` (409)
- `ServerError` (500)

## Security Considerations

1. **Authentication**
   - GitHub OAuth 2.0 for login
   - JWT for API authentication
   - Refresh tokens for long sessions

2. **Encryption**
   - GitHub tokens encrypted at rest
   - Environment variables encrypted
   - Deployment secrets handled securely

3. **CORS**
   - Limited to frontend origin
   - Credentials required for cookies

4. **Rate Limiting**
   - Per-user rate limits
   - Per-endpoint rate limits
   - DDoS protection

5. **Input Validation**
   - Pydantic schemas
   - Type checking
   - Sanitization

## Performance Optimization

1. **Database**
   - Connection pooling
   - Query optimization
   - Indexing on frequent queries
   - Pagination for large datasets

2. **Caching**
   - Redis for session data
   - Repository metadata caching
   - API response caching

3. **Frontend**
   - Code splitting (Vite)
   - Lazy loading routes
   - Memoization (React.memo)
   - Virtual scrolling for large lists

4. **API**
   - Async/await for I/O operations
   - Background tasks for long operations
   - Streaming for large responses

## Deployment Targets

### Azure App Service

**Supported**:

- Node.js applications
- Python applications
- .NET applications
- Docker containers

**Configuration**:

```json
{
  "subscription_id": "xxx",
  "resource_group": "xxx",
  "app_service_name": "xxx",
  "runtime_stack": "NODE|14-lts"
}
```

### Vercel

**Supported**:

- Next.js
- React
- Node.js APIs
- Static sites

**Configuration**:

```json
{
  "project_id": "xxx",
  "team_id": "xxx",
  "environment": "production|preview"
}
```

## Scalability

### Horizontal Scaling

1. **Frontend**
   - Serve static files from CDN
   - Load balancing with multiple instances

2. **Backend**
   - Stateless API servers
   - Load balancer distribution
   - Database connection pooling

3. **Database**
   - Read replicas
   - Sharding by user_id
   - Archive old deployments

### Vertical Scaling

1. Increase server resources
2. Optimize database queries
3. Implement caching layer

## Monitoring & Logging

1. **Application Logs**
   - Structured logging (JSON)
   - Log levels (DEBUG, INFO, WARNING, ERROR)
   - Request IDs for tracing

2. **Metrics**
   - API response times
   - Database query times
   - Deployment success rates
   - Error rates

3. **Alerting**
   - High error rates
   - Deployment failures
   - Database connection issues

---

For more details, see related documentation in `/docs`
