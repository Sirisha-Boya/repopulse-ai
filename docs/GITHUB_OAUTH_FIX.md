# 🔧 GitHub OAuth Setup - Complete Fix Guide

## The Problem

After GitHub login, the app redirects to GitHub instead of your application. This is a **GitHub OAuth configuration issue**.

## Solution: Verify Your GitHub App Settings

### Step 1: Check GitHub OAuth App Configuration

1. Go to: **https://github.com/settings/developers**
2. Click on your OAuth app or create a new one if needed
3. **VERIFY these settings exactly:**

   ```
   Application name:     Deployment Orchestration Platform
   Homepage URL:         http://localhost:3000
   Authorization callback URL:  http://localhost:3000/auth/callback
   ```

   ⚠️ **IMPORTANT**: The callback URL must be EXACTLY `http://localhost:3000/auth/callback`
   - No trailing slash
   - Must use http:// (not https:// for localhost)
   - Must match exactly in frontend .env

4. Copy your credentials:
   - `Client ID`
   - `Client Secret`

### Step 2: Update Backend .env

Edit `backend/.env`:

```bash
GITHUB_CLIENT_ID=your-client-id-here
GITHUB_CLIENT_SECRET=your-client-secret-here
GITHUB_REDIRECT_URI=http://localhost:3000/auth/callback
```

### Step 3: Update Frontend .env

Edit `frontend/.env`:

```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_GITHUB_CLIENT_ID=your-client-id-here
```

### Step 4: Important - Update Frontend Routes

Make sure your React Router includes the callback route. Check `src/App.tsx`:

```typescript
<Routes>
  <Route path="/login" element={<LoginPage />} />
  <Route path="/auth/callback" element={<AuthCallback />} />  // ← Must exist!
  {/* ... other routes ... */}
</Routes>
```

### Step 5: Restart Everything

```bash
# Stop current services
docker-compose down

# Rebuild and start
docker-compose up --build
```

Or if running locally:

```bash
# Backend terminal
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend terminal
cd frontend
npm install
npm run dev
```

## Expected Flow After Fix

1. ✅ User clicks "Sign in with GitHub" on login page
2. ✅ Redirects to GitHub authorization page (`github.com/login/oauth/authorize?...`)
3. ✅ User authorizes app
4. ✅ GitHub redirects back to `http://localhost:3000/auth/callback?code=xxx`
5. ✅ `AuthCallback.tsx` extracts the code from URL
6. ✅ Sends code to backend API `/api/auth/github/callback`
7. ✅ Backend exchanges code for GitHub token
8. ✅ Backend returns JWT tokens + user data
9. ✅ Frontend stores tokens and redirects to dashboard
10. ✅ Repository list shows your GitHub repositories ✨

## Testing the Fix

### 1. Test Backend Endpoint

```bash
# Get OAuth URL
curl http://localhost:8000/api/auth/github/login

# Should return:
# {
#   "oauth_url": "https://github.com/login/oauth/authorize?...",
#   "state": "uuid-string"
# }
```

### 2. Test Frontend

1. Visit `http://localhost:3000/login`
2. Click "Sign in with GitHub"
3. You should be redirected to `github.com` login
4. After authorizing, you should return to `http://localhost:3000/auth/callback`
5. You should see "Authenticating..." message
6. After ~2 seconds, you should see the dashboard with repositories

### 3. Check Browser Console

Open DevTools (F12) and check Console tab for any errors:

- Look for messages like "OAuth Callback - Code: xxxx"
- Look for any fetch errors
- Check Network tab for API calls

## Troubleshooting

### Issue: Still redirecting to GitHub after authorization

**Solution:**

1. Verify `Authorization callback URL` in GitHub settings is EXACTLY `http://localhost:3000/auth/callback`
2. Clear browser cache/cookies: `Ctrl+Shift+Delete`
3. Delete local storage: Open DevTools > Application > Local Storage > Clear all

### Issue: "Failed to exchange code for token"

**Solution:**

1. Verify Client ID and Secret match GitHub app settings
2. Check backend logs: `docker-compose logs backend`
3. Ensure GitHub API is accessible: `curl https://api.github.com`

### Issue: CORS errors in console

**Solution:**

1. Verify `FRONTEND_URL` in backend config
2. Ensure CORS middleware is enabled in `app/main.py`
3. Check that API requests go to `http://localhost:8000`

### Issue: Repositories not showing after login

**Solution:**

1. Click "Sync from GitHub" button on dashboard
2. Check browser console for errors
3. Check backend logs for API errors
4. Verify GitHub token has correct permissions: `repo`, `user`, `workflow`

## API Endpoints Used

### 1. Get OAuth URL

```
GET /api/auth/github/login
Response: { "oauth_url": "..." }
```

### 2. Exchange Code for Token

```
POST /api/auth/github/callback
Body: { "code": "github-authorization-code" }
Response: {
  "access_token": "jwt-token",
  "refresh_token": "jwt-refresh",
  "user": { ... }
}
```

### 3. Sync Repositories

```
POST /api/repositories/sync
Headers: { Authorization: "Bearer <access_token>" }
Response: { "message": "Synced X repositories", "count": X }
```

### 4. List Repositories

```
GET /api/repositories?page=1&page_size=20
Headers: { Authorization: "Bearer <access_token>" }
Response: {
  "total": X,
  "repositories": [ ... ],
  "page": 1,
  "page_size": 20
}
```

## Full OAuth Debug Checklist

- [ ] GitHub OAuth app exists at github.com/settings/developers
- [ ] `Authorization callback URL` = `http://localhost:3000/auth/callback`
- [ ] `Client ID` copied to `backend/.env` and `frontend/.env`
- [ ] `Client Secret` copied to `backend/.env`
- [ ] `GITHUB_REDIRECT_URI=http://localhost:3000/auth/callback` in `backend/.env`
- [ ] React Router has `/auth/callback` route
- [ ] Backend running on `http://localhost:8000`
- [ ] Frontend running on `http://localhost:3000`
- [ ] Browser cache cleared
- [ ] Docker services restarted (`docker-compose down && docker-compose up --build`)
- [ ] Backend logs show no errors
- [ ] Frontend console shows "OAuth Callback - Code: ..."
- [ ] Network tab shows successful POST to `/api/auth/github/callback`

## After Successful Login

### Dashboard Shows:

- ✅ Your GitHub username
- ✅ Total repositories count
- ✅ Recent repositories list
- ✅ "Sync from GitHub" button (to fetch latest)

### Repositories Page Shows:

- ✅ All your repositories in a table
- ✅ Repository name, description, language
- ✅ Default branch, stars, last updated date
- ✅ Search functionality

### What Happens Next:

1. Click on a repository to see details
2. Click "Analyze" to scan repository (Phase 2)
3. Click "Publish" to create deployment (Phase 3)

## Need More Help?

1. Check **docs/API.md** for full API reference
2. Check **docs/SETUP.md** for detailed setup
3. Review backend logs: `docker-compose logs backend -f`
4. Review frontend logs: Check browser Console tab

---

**If you've followed these steps and it still doesn't work, please share:**

1. Backend logs output
2. Browser console errors
3. Network tab screenshot showing the redirect
4. Your GitHub OAuth app settings (Client ID)
