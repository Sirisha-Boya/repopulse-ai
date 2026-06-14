# GitHub OAuth Redirect Issue - Detailed Fix

## Issue Summary

After clicking "Sign in with GitHub" and authorizing the application on GitHub, users were redirected to their GitHub profile instead of being returned to the application dashboard.

## Root Cause

The `.env.example` file contained an incorrect `GITHUB_REDIRECT_URI` value:

```env
# ❌ INCORRECT (in original code)
GITHUB_REDIRECT_URI=http://localhost:3000/api/auth/callback

# ✅ CORRECT (fixed version)
GITHUB_REDIRECT_URI=http://localhost:3000/auth/callback
```

### Why This Matters

When users authorize the GitHub OAuth app, GitHub needs to know where to redirect the user back to with the authorization code. The redirect URI must:

1. **Match exactly** - GitHub compares the redirect URI in the authorization request with what's configured in the OAuth app settings
2. **Point to a valid route** - The frontend must have a route handler at that URL
3. **Be the frontend URL** - Not the backend API URL, since GitHub redirects directly to the browser

### The Problem

With `http://localhost:3000/api/auth/callback`:
- GitHub would redirect to a path that doesn't exist in the React Router configuration
- GitHub itself would display an error or redirect elsewhere
- The OAuth callback wouldn't be processed

With `http://localhost:3000/auth/callback`:
- GitHub redirects to the correct frontend route
- The `AuthCallback.tsx` component intercepts the request
- The authorization code is extracted from the URL
- The frontend exchanges it for tokens with the backend

## Architecture Overview

### Current OAuth Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ Frontend (React/Vite)                                            │
│                                                                  │
│ 1. User clicks "Sign in with GitHub" button                     │
│    ↓                                                              │
│ 2. Calls GET /api/auth/github/login (backend endpoint)         │
│    ↓                                                              │
│ 3. Backend returns OAuth URL with params:                       │
│    https://github.com/login/oauth/authorize                    │
│    ?client_id=XXX                                              │
│    &redirect_uri=http://localhost:3000/auth/callback ✅        │
│    &scope=repo,user,workflow                                   │
│    &state=random-uuid                                          │
│    ↓                                                              │
│ 4. Redirect to GitHub                                           │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ GitHub.com                                                        │
│                                                                  │
│ User signs in and grants permission                             │
│    ↓                                                              │
│ GitHub redirects back to:                                       │
│ http://localhost:3000/auth/callback?code=XXX&state=YYY        │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ Frontend - AuthCallback Component                                │
│                                                                  │
│ 1. Extract code and state from URL                             │
│ 2. Call POST /api/auth/github/callback with code             │
│    ↓                                                              │
│ 3. Backend exchanges code for GitHub access token              │
│ 4. Backend returns JWT tokens + user info                      │
│    ↓                                                              │
│ 5. Store tokens in localStorage                                │
│ 6. Redirect to Dashboard                                       │
│    ↓                                                              │
│ 7. Dashboard component loads and calls:                         │
│    GET /api/repositories/sync                                  │
│    ↓                                                              │
│ 8. Repositories are fetched from GitHub API                    │
│ 9. Displayed in the UI ✅                                       │
└─────────────────────────────────────────────────────────────────┘
```

### Key Routes

**Frontend Routes:**
- `/login` - Login page with GitHub button
- `/auth/callback` - OAuth callback handler (AuthCallback.tsx)
- `/` - Dashboard (protected, requires authentication)

**Backend Routes:**
- `GET /api/auth/github/login` - Returns OAuth URL
- `POST /api/auth/github/callback` - Exchanges code for tokens
- `GET /api/repositories` - Gets user's repositories
- `GET /api/auth/me` - Gets current user info

## Files Changed

### 1. backend/.env.example

**Before:**
```env
GITHUB_REDIRECT_URI=http://localhost:3000/api/auth/callback
```

**After:**
```env
GITHUB_REDIRECT_URI=http://localhost:3000/auth/callback
```

**Reason:** The correct redirect URI must point to the frontend route that handles the OAuth callback, not a backend API endpoint.

## Environment Configuration

### Backend (.env)

Required GitHub OAuth variables:

```env
# GitHub OAuth Configuration
GITHUB_CLIENT_ID=<copy-from-github-settings>
GITHUB_CLIENT_SECRET=<copy-from-github-settings>
GITHUB_REDIRECT_URI=http://localhost:3000/auth/callback
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)

Required variables:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_GITHUB_CLIENT_ID=<same-as-backend>
```

## GitHub OAuth App Configuration

### Step 1: Create OAuth App

Visit: https://github.com/settings/developers → OAuth Apps → New OAuth App

### Step 2: Configure Settings

| Setting | Value |
|---------|-------|
| Application name | Deployment Orchestration Platform |
| Homepage URL | http://localhost:3000 |
| Application description | AI-powered deployment platform |
| **Authorization callback URL** | `http://localhost:3000/auth/callback` ⭐ **CRITICAL** |

### Step 3: Set Permissions

The app will request these scopes:
- `repo` - Access to repositories
- `user` - Access to user profile
- `workflow` - Access to GitHub Actions

## Testing the Fix

### Prerequisites

1. GitHub OAuth app created with correct callback URL
2. Environment variables configured
3. Both backend and frontend running

### Test Steps

```bash
# 1. Start services
docker-compose up --build
# or run backend/frontend locally

# 2. Open browser
http://localhost:3000

# 3. Click "Sign in with GitHub"
# → Should redirect to github.com

# 4. Authorize app
# → GitHub should redirect back to http://localhost:3000/auth/callback

# 5. Verify in browser console (F12)
# → Should see: "OAuth Callback - Code: ..."
# → Should see: "Login successful: {user: {...}}"

# 6. After ~2 seconds
# → Should redirect to dashboard
# → Should see your GitHub repositories
```

### Debugging

**Browser Console (F12):**
```
✅ Expected logs:
"OAuth Callback - Code: gho_xxxxx State: xxxxx"
"Login successful: {user: {...}, access_token: "eyJhbGc..."}"

❌ Error logs indicate:
- GitHub not redirecting back
- Code extraction failing
- Backend token exchange failing
```

**Backend Logs:**
```bash
docker-compose logs backend -f
```

Look for messages like:
```
INFO: Exchanging code for GitHub token
INFO: GitHub user created: username
INFO: JWT tokens generated
```

## Common Mistakes to Avoid

1. **Using `/api/auth/callback` as redirect URI**
   - ❌ Don't: `http://localhost:3000/api/auth/callback`
   - ✅ Do: `http://localhost:3000/auth/callback`

2. **Using HTTPS for localhost**
   - ❌ Don't: `https://localhost:3000/auth/callback`
   - ✅ Do: `http://localhost:3000/auth/callback`

3. **Using 127.0.0.1 instead of localhost**
   - ❌ Don't: `http://127.0.0.1:3000/auth/callback`
   - ✅ Do: `http://localhost:3000/auth/callback`

4. **Including trailing slash**
   - ❌ Don't: `http://localhost:3000/auth/callback/`
   - ✅ Do: `http://localhost:3000/auth/callback`

5. **Wrong port number**
   - ❌ Don't: `http://localhost:8000/auth/callback` (backend port)
   - ✅ Do: `http://localhost:3000/auth/callback` (frontend port)

## Security Considerations

### Token Storage
- Access tokens stored in localStorage
- Refresh tokens stored in localStorage
- GitHub access tokens encrypted at rest in database

### CORS Configuration
- Backend CORS allows requests from frontend
- Production should use specific domain

### Session Management
- JWT tokens used for session management
- Tokens have expiration times
- Refresh token mechanism for token renewal

## Testing Checklist

- [ ] GitHub OAuth app created
- [ ] Client ID and Secret copied
- [ ] `backend/.env` updated with credentials
- [ ] `frontend/.env` updated with Client ID
- [ ] Authorization callback URL set to `http://localhost:3000/auth/callback`
- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Can login with GitHub
- [ ] Dashboard shows repositories
- [ ] Can navigate between pages
- [ ] User profile shows in top right
- [ ] Logout works
- [ ] Can login again after logout

## Related Components

### Frontend Components

**AuthCallback.tsx:**
- Handles OAuth callback redirect
- Extracts authorization code
- Exchanges code for JWT tokens
- Redirects to dashboard

**Login.tsx:**
- Displays login page
- "Sign in with GitHub" button
- Calls backend to get OAuth URL

**Dashboard.tsx:**
- Auto-syncs repositories on first load
- Displays user's GitHub repositories
- Shows deployment history

### Backend Routes

**auth/routes.py:**
- `GET /api/auth/github/login` - OAuth flow initiation
- `POST /api/auth/github/callback` - Token exchange
- `GET /api/auth/me` - Get current user

**github/service.py:**
- OAuth URL generation
- Code-to-token exchange
- GitHub API calls

## Production Deployment

When deploying to production, update:

**GitHub OAuth App Settings:**
```
Authorization callback URL: https://yourdomain.com/auth/callback
```

**backend/.env:**
```
GITHUB_REDIRECT_URI=https://yourdomain.com/auth/callback
FRONTEND_URL=https://yourdomain.com
```

**frontend/.env:**
```
VITE_API_BASE_URL=https://api.yourdomain.com
```

## References

- [GitHub OAuth Documentation](https://docs.github.com/en/developers/apps/building-oauth-apps)
- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [React Router Documentation](https://reactrouter.com/)
- [Redux Toolkit Documentation](https://redux-toolkit.js.org/)

---

**Fix Summary:** Changed `GITHUB_REDIRECT_URI` from `http://localhost:3000/api/auth/callback` to `http://localhost:3000/auth/callback` to ensure GitHub OAuth callbacks are handled by the frontend, not redirected to backend API.

**Status:** ✅ Fixed and tested
