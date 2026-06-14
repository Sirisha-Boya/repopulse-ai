# 🚀 QUICK FIX - GitHub OAuth Redirect Issue

## The Problem (What You're Experiencing)

- ❌ After clicking "Sign in with GitHub"
- ❌ You authorize the app on GitHub
- ❌ You get redirected back to GitHub instead of your dashboard
- ❌ You see your GitHub repository instead of the app dashboard

## The Root Cause

Your GitHub OAuth app's **"Authorization callback URL"** is incorrectly set or doesn't match your environment.

## The Solution (3 Simple Steps)

### STEP 1: Fix GitHub App Settings

1. Go to: **https://github.com/settings/developers**
2. Select your OAuth app (or create new one)
3. **IMPORTANT**: Set "Authorization callback URL" to:
   ```
   http://localhost:3000/auth/callback
   ```
   ⚠️ MUST be exactly like this (no trailing slash, http not https)
4. Save changes
5. Copy **Client ID** and **Client Secret**

### STEP 2: Update Configuration Files

**Edit `backend/.env`:**

```bash
GITHUB_CLIENT_ID=your-client-id-from-github
GITHUB_CLIENT_SECRET=your-client-secret-from-github
GITHUB_REDIRECT_URI=http://localhost:3000/auth/callback
```

**Edit `frontend/.env`:**

```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_GITHUB_CLIENT_ID=same-client-id-as-above
```

### STEP 3: Restart the Application

```bash
# Option A: Docker Compose (Recommended)
docker-compose down
docker-compose up --build

# Option B: Local Development
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Verify the Fix

### ✅ Test the Flow

1. Open `http://localhost:3000` in browser
2. Click **"Sign in with GitHub"**
3. You should see: `github.com/login/oauth/authorize?...`
4. Click **"Authorize"**
5. You should be redirected back to: `http://localhost:3000/auth/callback`
6. Page shows: "Authenticating..."
7. Wait 2 seconds...
8. You should see the **Dashboard** with your repositories! 🎉

### ✅ Check Browser Console (F12)

You should see messages like:

```
OAuth Callback - Code: gho_xxxxx State: xxxxx
Login successful: {user: {...}, access_token: "eyJhbGc..."}
```

### ✅ Check Repositories Show

After login, your dashboard should show:

- ✅ Your GitHub username
- ✅ Total repository count
- ✅ List of 5 recent repositories with:
  - Repository name
  - Description
  - Programming language
  - Star count

## If It Still Doesn't Work

### Debug Checklist

1. **Clear Browser Cache**
   - Press `Ctrl+Shift+Delete`
   - Clear "All time" cookies and cache
   - Refresh page

2. **Check GitHub Settings Again**
   - Go to https://github.com/settings/developers
   - Click your app
   - Verify "Authorization callback URL" is EXACTLY `http://localhost:3000/auth/callback`

3. **Check Backend Logs**

   ```bash
   docker-compose logs backend -f
   ```

   Look for errors related to GitHub or OAuth

4. **Check Frontend Console**
   - Open DevTools (F12)
   - Go to Console tab
   - Look for any red errors
   - Check Network tab - look for requests to `/api/auth/github/callback`

5. **Verify Ports Are Open**

   ```bash
   # Should see all services running
   docker-compose ps

   # Should return response
   curl http://localhost:8000/health
   ```

## Common Issues & Fixes

### Issue: "Still redirects to GitHub after auth"

**Fix:**

- Verify redirect URL in GitHub settings (no trailing slash!)
- Clear browser cache completely
- Restart docker: `docker-compose restart`

### Issue: "CORS error in console"

**Fix:**

- Make sure backend `.env` has: `FRONTEND_URL=http://localhost:3000`
- Restart backend

### Issue: "Failed to exchange code for token"

**Fix:**

- Verify Client ID and Secret in `.env` match GitHub settings
- Check backend logs for detailed error

### Issue: "Repositories don't show"

**Fix:**

- You should see "Syncing..." message automatically
- If not, click "Sync Again" button
- Check browser console for errors

## The Complete Flow (What Should Happen)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1. User clicks "Sign in with GitHub"                      │
│     ↓                                                        │
│  2. Frontend calls GET /api/auth/github/login              │
│     ↓                                                        │
│  3. Frontend redirects to github.com/login/oauth/...       │
│     ↓                                                        │
│  4. User signs in and authorizes app on GitHub             │
│     ↓                                                        │
│  5. GitHub redirects back to:                              │
│     http://localhost:3000/auth/callback?code=xxxxx        │
│     ↓                                                        │
│  6. AuthCallback.tsx extracts code from URL                │
│     ↓                                                        │
│  7. Frontend calls POST /api/auth/github/callback          │
│     with the code                                           │
│     ↓                                                        │
│  8. Backend exchanges code for GitHub token                │
│     ↓                                                        │
│  9. Backend returns JWT + user data to frontend            │
│     ↓                                                        │
│  10. Frontend stores JWT in localStorage                    │
│      ↓                                                       │
│  11. Frontend redirects to Dashboard                        │
│      ↓                                                       │
│  12. Dashboard auto-syncs repositories                      │
│      ↓                                                       │
│  13. Repositories display on Dashboard  ✅ SUCCESS!        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## What You Can Do After Login

1. **View Repositories** - Click "View All" to see all repos
2. **Search Repositories** - Type in search box to filter
3. **Sync Again** - Refresh from latest GitHub
4. **Next Steps** - Analyze and deploy (Phase 2 & 3)

## Quick Test Command

To verify everything is connected:

```bash
# Test backend health
curl http://localhost:8000/health

# Test OAuth endpoint
curl http://localhost:8000/api/auth/github/login

# You should get a response with oauth_url
```

## Still Having Issues?

Please run this and share the output:

```bash
# Check all services running
docker-compose ps

# Check backend logs
docker-compose logs backend --tail 50

# Check frontend is accessible
curl http://localhost:3000
```

---

**After you fix this, you'll have:**
✅ GitHub OAuth working perfectly  
✅ Repositories loading automatically  
✅ Dashboard showing your GitHub repos  
✅ Ready for Phase 2 (Analysis & Deployment)

**Let me know if it works now!** 🎉
