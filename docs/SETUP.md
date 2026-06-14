# Setup Guide

## Initial Setup

### Step 1: Clone Repository

```bash
cd d:\projects\repopulse-ai
```

### Step 2: Configure Environment Variables

#### Backend (.env)

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and update:

```env
DATABASE_URL=postgresql://user:password@postgres:5432/repopulse_ai
SECRET_KEY=generate-a-random-key-using-openssl-rand-32

# GitHub OAuth (get from github.com/settings/developers)
GITHUB_CLIENT_ID=your-client-id
GITHUB_CLIENT_SECRET=your-client-secret
GITHUB_REDIRECT_URI=http://localhost:3000/auth/callback

# OpenAI (get from platform.openai.com)
OPENAI_API_KEY=your-openai-key

# Azure (optional, for real deployments)
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret

# Vercel (optional, for real deployments)
VERCEL_API_TOKEN=your-vercel-token
```

#### Frontend (.env)

```bash
cd ../frontend
cp .env.example .env
```

Edit `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_GITHUB_CLIENT_ID=same-as-backend
```

### Step 3: GitHub OAuth Setup

1. Go to https://github.com/settings/developers
2. Click "New OAuth App"
3. Fill in:
   - Application name: `Deployment Orchestration Platform`
   - Homepage URL: `http://localhost:3000`
   - Authorization callback URL: `http://localhost:3000/auth/callback`
4. Copy Client ID and Client Secret to `.env`

### Step 4: OpenAI Setup

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy to `OPENAI_API_KEY` in `.env`
4. Ensure you have GPT-4 access (may require paid account)

## Running with Docker Compose

### Prerequisites

- Docker Desktop installed
- Docker Compose installed

### Start Services

```bash
# From project root
docker-compose up --build

# Or in background
docker-compose up -d --build
```

### Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Stop Services

```bash
docker-compose down

# Remove volumes too
docker-compose down -v
```

## Local Development Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Initialize database
python -c "from app.database import init_db; init_db()"

# Run server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm run dev
```

Backend will run on http://localhost:8000
Frontend will run on http://localhost:3000

## Database Setup

### Initialize Database

```bash
# Using Docker
docker exec repopulse-backend python -c "from app.database import init_db; init_db()"

# Or locally
python backend/app/database.py
```

### Create Tables

Tables are created automatically on first run. To reset:

```bash
# WARNING: This will drop all tables
docker exec repopulse-backend python -c "from app.database import drop_db, init_db; drop_db(); init_db()"
```

### Database Migrations (Alembic)

Coming in Phase 3. For now, tables are created via SQLAlchemy ORM.

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## Build for Production

### Backend

```bash
# Build image
docker build -f backend/Dockerfile -t repopulse-backend:1.0.0 backend/

# Run
docker run -p 8000:8000 repopulse-backend:1.0.0
```

### Frontend

```bash
# Build
cd frontend
npm run build

# Build Docker image
docker build -f Dockerfile -t repopulse-frontend:1.0.0 .

# Run
docker run -p 3000:3000 repopulse-frontend:1.0.0
```

## Troubleshooting

### Issue: "Connection refused" when accessing http://localhost:3000

**Solution**:

```bash
# Check if frontend container is running
docker-compose ps

# Check frontend logs
docker-compose logs frontend

# Restart frontend
docker-compose restart frontend
```

### Issue: "Cannot connect to database"

**Solution**:

```bash
# Verify PostgreSQL is running
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Verify DATABASE_URL in .env
# Format: postgresql://user:password@host:port/database
```

### Issue: "GitHub OAuth not working"

**Solution**:

1. Verify credentials in `.env`
2. Check GitHub app settings at github.com/settings/developers
3. Ensure redirect URI matches exactly
4. Check backend logs: `docker-compose logs backend`

### Issue: Frontend not loading styles

**Solution**:

```bash
# Rebuild frontend
docker-compose down frontend
docker-compose build frontend
docker-compose up frontend -d

# Or locally
cd frontend
npm run dev
```

### Issue: API returns 401 Unauthorized

**Solution**:

1. Ensure you're logged in
2. Check access token in browser localStorage
3. Try logging out and logging back in
4. Check backend logs for JWT issues

## Performance Tuning

### Backend

```python
# In config.py
DATABASE_POOL_SIZE = 20
DATABASE_MAX_OVERFLOW = 40
```

### Frontend

```bash
# Optimize build
npm run build -- --minify

# Analyze bundle
npm install --save-dev webpack-bundle-analyzer
npm run build
```

## Next Steps

1. Review the [API Documentation](./API.md)
2. Explore [Architecture Documentation](./ARCHITECTURE.md)
3. Check [Contributing Guidelines](./CONTRIBUTING.md)
4. Run example flows

## Getting Help

1. Check logs: `docker-compose logs -f`
2. Review API docs: http://localhost:8000/docs
3. Check status: http://localhost:8000/health
4. Create an issue on GitHub

---

Need more help? See FAQ.md or contact support.
