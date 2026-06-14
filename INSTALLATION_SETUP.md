# 🚀 Installation & Setup Guide

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+
- PostgreSQL 12+
- Docker and Docker Compose (optional, for containerized setup)
- GitHub Account with OAuth app setup

## Step 1: Clone Repository

```bash
git clone <repository-url>
cd repopulse-ai
```

## Step 2: Create GitHub OAuth App

### Go to GitHub Developer Settings

1. Navigate to: https://github.com/settings/developers
2. Click "Developer settings" in left sidebar
3. Click "OAuth Apps"
4. Click "New OAuth App"

### Fill in OAuth App Details

**Application name:**

```
Deployment Orchestration Platform
```

**Homepage URL:**

```
http://localhost:3000
```

**Application description:**

```
AI-powered deployment orchestration platform for GitHub repositories
```

**Authorization callback URL:** ⚠️ **CRITICAL**

```
http://localhost:3000/auth/callback
```

✅ **Click "Register application"**

### Copy Your Credentials

You'll see:

- **Client ID** - Copy this
- **Client Secret** - Copy this (keep it secret!)

## Step 3: Backend Setup

### Create Backend Environment File

```bash
cd backend
cp .env.example .env
```

### Edit `backend/.env`

```bash
# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/repopulse_ai

# FastAPI
SECRET_KEY=your-secret-key-change-in-production
ENVIRONMENT=development
DEBUG=True
API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# GitHub OAuth (from Step 2)
GITHUB_CLIENT_ID=<your-client-id>
GITHUB_CLIENT_SECRET=<your-client-secret>
GITHUB_REDIRECT_URI=http://localhost:3000/auth/callback
GITHUB_API_TOKEN=<optional-github-pat-token>

# Other services (optional for Phase 2)
OPENAI_API_KEY=<your-openai-key>
```

### Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Initialize Database

```bash
# Create alembic migration
alembic upgrade head
```

## Step 4: Frontend Setup

### Create Frontend Environment File

```bash
cd frontend
cp .env.example .env
```

### Edit `frontend/.env`

```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_GITHUB_CLIENT_ID=<your-github-client-id-from-step-2>
VITE_APP_NAME=Deployment Orchestration Platform
VITE_LOG_LEVEL=info
```

### Install Frontend Dependencies

```bash
npm install
```

## Step 5: Run Application

### Option A: Docker Compose (Recommended for Production)

```bash
# From project root
docker-compose up --build
```

Services will be available at:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432

### Option B: Local Development

**Terminal 1 - Backend:**

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

## Step 6: Verify Installation

### Check Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{ "status": "ok" }
```

### Check Frontend

Open http://localhost:3000 in browser

Expected: Login page with "Sign in with GitHub" button

## Step 7: Test OAuth Flow

1. Click **"Sign in with GitHub"** button
2. You should be redirected to GitHub authorization page
3. Click **"Authorize"**
4. You should be redirected back to: `http://localhost:3000/auth/callback`
5. Page shows "Authenticating with GitHub..."
6. After 2 seconds, redirects to Dashboard
7. Dashboard shows your GitHub repositories ✅

## Common Issues & Solutions

### Issue: "CORS error" in browser console

**Causes:**

- Backend not running
- Frontend not on http://localhost:3000
- CORS misconfigured

**Fix:**

```bash
# Ensure backend is running
curl http://localhost:8000/health

# Check frontend .env has correct API URL
cat frontend/.env

# Restart both services
```

### Issue: "Failed to exchange code for token"

**Causes:**

- GitHub Client ID/Secret incorrect
- Redirect URI doesn't match GitHub settings

**Fix:**

1. Verify GitHub OAuth app settings: https://github.com/settings/developers
2. Ensure "Authorization callback URL" is EXACTLY: `http://localhost:3000/auth/callback`
3. Copy Client ID and Secret again
4. Update `backend/.env` with new credentials
5. Restart backend

### Issue: "Still redirects to GitHub after auth"

**Causes:**

- Redirect URI in backend .env is wrong
- OAuth app callback URL not configured

**Fix:**

1. Edit `backend/.env`
2. Set: `GITHUB_REDIRECT_URI=http://localhost:3000/auth/callback`
3. Restart backend
4. Check GitHub app settings again

### Issue: "Database connection error"

**Causes:**

- PostgreSQL not running
- Connection string wrong

**Fix:**

```bash
# Start PostgreSQL (if Docker)
docker-compose up postgres

# Or verify PostgreSQL is running locally
psql -U user -d repopulse_ai -c "SELECT 1"

# Check DATABASE_URL in backend/.env
```

### Issue: "npm install fails"

**Causes:**

- Node version too old
- Corrupted node_modules

**Fix:**

```bash
# Update Node to 18+
node --version

# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Environment Variables Reference

### Backend (.env)

| Variable             | Example                                            | Required        |
| -------------------- | -------------------------------------------------- | --------------- |
| DATABASE_URL         | postgresql://user:pass@localhost:5432/repopulse_ai | ✅              |
| SECRET_KEY           | your-secret-key-here                               | ✅              |
| GITHUB_CLIENT_ID     | abc123xyz                                          | ✅              |
| GITHUB_CLIENT_SECRET | ghu_xxx                                            | ✅              |
| GITHUB_REDIRECT_URI  | http://localhost:3000/auth/callback                | ✅              |
| FRONTEND_URL         | http://localhost:3000                              | ✅              |
| OPENAI_API_KEY       | sk-xxx                                             | For Phase 2     |
| ENVIRONMENT          | development                                        | ✅              |
| DEBUG                | True                                               | For development |

### Frontend (.env)

| Variable              | Example               | Required |
| --------------------- | --------------------- | -------- |
| VITE_API_BASE_URL     | http://localhost:8000 | ✅       |
| VITE_GITHUB_CLIENT_ID | abc123xyz             | ✅       |

## Database Setup

### Create PostgreSQL Database

```sql
CREATE DATABASE repopulse_ai;
CREATE USER user WITH PASSWORD 'password';
ALTER ROLE user SET client_encoding TO 'utf8';
ALTER ROLE user SET default_transaction_isolation TO 'read committed';
ALTER ROLE user SET default_transaction_deferrable TO off;
ALTER ROLE user SET default_transaction_read_only TO off;
ALTER ROLE user SET statement_timeout TO 0;
GRANT ALL PRIVILEGES ON DATABASE repopulse_ai TO user;
```

### Run Migrations

```bash
cd backend
alembic upgrade head
```

## Production Deployment

### Update Environment Variables

Before deploying to production:

**Backend `.env`:**

```bash
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<generate-strong-secret>
GITHUB_REDIRECT_URI=https://yourdomain.com/auth/callback
FRONTEND_URL=https://yourdomain.com
DATABASE_URL=postgresql://user:pass@db-host:5432/repopulse_ai
```

**Frontend `.env`:**

```bash
VITE_API_BASE_URL=https://api.yourdomain.com
```

**GitHub OAuth App:**

- Update "Authorization callback URL" to: `https://yourdomain.com/auth/callback`

### Build for Production

```bash
# Backend
cd backend
# Use Docker or gunicorn

# Frontend
cd frontend
npm run build
# Deploy dist/ folder
```

## Troubleshooting

### View Backend Logs

```bash
# Docker
docker-compose logs backend -f

# Local
# Check console output where uvicorn is running
```

### View Frontend Logs

```bash
# Browser console (F12)
# Network tab to see API calls
```

### Reset Everything

```bash
# Stop services
docker-compose down -v

# Remove node modules and cache
rm -rf frontend/node_modules frontend/dist

# Restart
docker-compose up --build
```

## Next Steps

1. ✅ Complete this setup
2. ✅ Test OAuth login flow
3. 📊 Explore Dashboard
4. 🔍 Analyze a repository
5. 🚀 Deploy to Vercel/Azure (Phase 2)

## Support

For issues:

1. Check logs: `docker-compose logs -f`
2. Verify environment variables: `cat backend/.env`
3. Clear browser cache: Ctrl+Shift+Delete
4. Check GitHub OAuth settings: https://github.com/settings/developers
5. See TROUBLESHOOTING.md for detailed debugging

---

**Installation Complete!** 🎉

Your deployment platform is ready to use.
