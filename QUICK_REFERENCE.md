# Quick Reference Guide

## Project Commands

### Docker (Recommended for Development)

```bash
# Start all services
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild specific service
docker-compose build backend
docker-compose build frontend

# Access container shell
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Backend (Local Development)

```bash
# Setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload

# Database
python -c "from app.database import init_db; init_db()"
python -c "from app.database import drop_db; drop_db()"

# Tests
pytest tests/ -v
pytest tests/ --cov=app
```

### Frontend (Local Development)

```bash
# Setup
cd frontend
npm install

# Development
npm run dev          # Hot reload on port 3000

# Production
npm run build        # Build for production
npm run preview      # Preview production build

# Code quality
npm run lint         # Run ESLint
npm run type-check   # TypeScript check
npm run format       # Format with Prettier
```

## API Endpoints Quick Reference

### Auth

```
POST /api/auth/github/login           Get OAuth URL
POST /api/auth/github/callback        Handle OAuth callback
POST /api/auth/refresh                Refresh JWT token
GET  /api/auth/me                     Get current user
POST /api/auth/logout                 Logout
```

### Repositories

```
POST /api/repositories/sync           Sync from GitHub
GET  /api/repositories                List repositories
GET  /api/repositories/search         Search repositories
GET  /api/repositories/{id}           Get repository
DELETE /api/repositories/{id}         Delete repository
```

## Frontend Structure

```
src/
├── pages/          # Route components
├── components/     # Reusable components
├── redux/          # State management
├── services/       # API communication
├── hooks/          # Custom React hooks
└── theme/          # Theme configuration
```

## Backend Structure

```
app/
├── main.py         # FastAPI app
├── config.py       # Configuration
├── database.py     # Database setup
├── models.py       # SQLAlchemy models
├── schemas.py      # Pydantic schemas
├── auth/           # Authentication
├── github/         # GitHub integration
└── repositories/   # Repository logic
```

## Key Files

### Frontend

- `src/App.tsx` - Main app component
- `src/redux/store.ts` - Redux store
- `src/services/apiClient.ts` - API client
- `frontend/package.json` - Dependencies

### Backend

- `app/main.py` - FastAPI app
- `app/models.py` - Database models
- `app/config.py` - Configuration
- `backend/requirements.txt` - Dependencies

## Environment Setup

### Minimal .env for Development

```bash
# Backend
DATABASE_URL=postgresql://user:password@localhost:5432/repopulse_ai
SECRET_KEY=dev-secret-key-change-in-production
GITHUB_CLIENT_ID=your-client-id
GITHUB_CLIENT_SECRET=your-client-secret

# Frontend
VITE_API_BASE_URL=http://localhost:8000
VITE_GITHUB_CLIENT_ID=your-client-id
```

## Database

### Create Tables

```bash
docker-compose exec backend python -c "from app.database import init_db; init_db()"
```

### Reset Database

```bash
docker-compose exec backend python -c "from app.database import drop_db, init_db; drop_db(); init_db()"
```

### Connect to Database

```bash
docker-compose exec postgres psql -U user -d repopulse_ai
```

## Common Issues & Solutions

| Issue                     | Solution                                                                |
| ------------------------- | ----------------------------------------------------------------------- |
| Port 3000 already in use  | `lsof -i :3000` then `kill -9 <PID>`                                    |
| Port 8000 already in use  | `lsof -i :8000` then `kill -9 <PID>`                                    |
| Database connection error | Check `DATABASE_URL` in `.env`                                          |
| Modules not found         | `pip install -r requirements.txt` (backend) or `npm install` (frontend) |
| CORS errors               | Check `FRONTEND_URL` in backend config                                  |
| Authentication failing    | Check GitHub OAuth credentials                                          |

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes and commit
git add .
git commit -m "feat: describe your changes"

# Push to remote
git push origin feature/your-feature

# Create pull request on GitHub
```

## Testing Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads on http://localhost:3000
- [ ] Can access API docs on http://localhost:8000/docs
- [ ] GitHub OAuth login works
- [ ] Repository list displays
- [ ] Can sync repositories
- [ ] Can navigate between pages
- [ ] Redux state updates correctly

## Performance Tips

### Frontend

- Use React.lazy() for route splitting
- Use React.memo() for expensive components
- Optimize images
- Check bundle size: `npm run build`

### Backend

- Check slow queries: `DATABASE_URL=...?echo=true`
- Use indexing on frequent query columns
- Cache frequently accessed data
- Use connection pooling

## Debugging

### Frontend (Chrome DevTools)

- React DevTools extension
- Redux DevTools extension
- Network tab for API calls
- Console for errors

### Backend (FastAPI)

- Visit `/docs` for interactive API docs
- Check logs: `docker-compose logs backend`
- Use `print()` or logging in code
- Check database with `psql`

## Useful Commands

```bash
# Check service status
docker-compose ps

# View resource usage
docker stats

# Rebuild from scratch
docker-compose down -v && docker-compose up --build

# Run backend only
docker-compose up backend postgres redis

# Run frontend only
docker-compose up frontend

# Interact with database
docker-compose exec postgres psql -U user -d repopulse_ai

# View Redis data
docker-compose exec redis redis-cli KEYS '*'

# See full request/response logs
curl -v http://localhost:8000/health
```

## Code Style

### Python

```python
# Use type hints
def get_user(user_id: int) -> User:
    pass

# Use pydantic for validation
class UserCreate(BaseModel):
    email: str
    password: str

# Use async/await
async def fetch_repos(token: str) -> list[Repository]:
    pass
```

### TypeScript/React

```typescript
// Use interfaces
interface Repository {
  id: number;
  name: string;
}

// Use types in components
const MyComponent: React.FC<Props> = ({ prop }) => {
  return <div>{prop}</div>;
};

// Use proper naming
const handleButtonClick = () => {};
const isLoading = false;
```

## Documentation Resources

- API Docs: `/docs`
- Architecture: `docs/ARCHITECTURE.md`
- Setup Guide: `docs/SETUP.md`
- This File: `QUICK_REFERENCE.md`

## Next Steps

1. **Phase 2 (Analysis)**
   - Implement repository analysis
   - Add AI code review
   - Generate health reports

2. **Phase 3 (Deployment)**
   - Create deployment workflows
   - Integrate Azure
   - Integrate Vercel

3. **Phase 4 (Monitoring)**
   - Add deployment logs
   - Create status dashboard
   - Add real-time updates

4. **Phase 5 (Advanced)**
   - Implement rollback
   - Add recommendations
   - Create admin features

---

**Last Updated**: 2024-01-02
**Version**: 1.0.0
**Status**: Production Ready
