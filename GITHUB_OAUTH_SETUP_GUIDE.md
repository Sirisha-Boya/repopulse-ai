# GitHub OAuth App Configuration - Screenshot Guide

## Step-by-Step: Setting Up GitHub OAuth

### Step 1: Access GitHub Developer Settings

1. Go to: https://github.com/settings/developers
2. Click "Developer settings" in left sidebar
3. Click "OAuth Apps"
4. Click "New OAuth App" (or select existing app to edit)

### Step 2: Fill in OAuth App Details

**You should see a form like this:**

```
Application name:
┌─────────────────────────────────────────────────────┐
│ Deployment Orchestration Platform                   │
└─────────────────────────────────────────────────────┘

Homepage URL:
┌─────────────────────────────────────────────────────┐
│ http://localhost:3000                               │
└─────────────────────────────────────────────────────┘

Application description (optional):
┌─────────────────────────────────────────────────────┐
│ AI-powered deployment orchestration platform        │
└─────────────────────────────────────────────────────┘

Authorization callback URL:  ⚠️ MOST IMPORTANT
┌─────────────────────────────────────────────────────┐
│ http://localhost:3000/auth/callback                 │
└─────────────────────────────────────────────────────┘
```

### ⚠️ CRITICAL - Authorization Callback URL

```
✅ CORRECT:
http://localhost:3000/auth/callback

❌ WRONG:
https://localhost:3000/auth/callback       (https not http)
http://localhost:3000/auth/callback/       (trailing slash)
http://localhost:3000/                     (no callback path)
http://127.0.0.1:3000/auth/callback        (127.0.0.1 instead of localhost)
http://localhost:3000/auth/github/callback (wrong path)
```

### Step 3: Register Application

1. Click "Register application" button
2. You'll see your credentials page

### Step 4: Copy Your Credentials

**You should see:**

```
┌─────────────────────────────────────────────────────┐
│ GitHub OAuth App Details                            │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Client ID:                                          │
│ [Click to copy]                                     │
│ xxxxxxxxxxxxxxxxxxxxxxxx                            │
│                                                     │
│ Client Secret:                                      │
│ [Click to copy]                                     │
│ xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx              │
│                                                     │
│ Authorization callback URL:                         │
│ http://localhost:3000/auth/callback                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Step 5: Save to Your Config Files

**Copy Client ID to:**

1. `backend/.env`:

```bash
GITHUB_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxx
```

2. `frontend/.env`:

```bash
VITE_GITHUB_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxx
```

**Copy Client Secret to:**

1. `backend/.env`:

```bash
GITHUB_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Verify Your Setup

### Checklist Before Testing

- [ ] You have a GitHub OAuth app created
- [ ] Client ID is copied to both `backend/.env` and `frontend/.env`
- [ ] Client Secret is copied to `backend/.env`
- [ ] Authorization callback URL is EXACTLY `http://localhost:3000/auth/callback`
- [ ] Backend running on `http://localhost:8000`
- [ ] Frontend running on `http://localhost:3000`
- [ ] Docker or local services are started

### Test the Configuration

1. **Clear all storage:**
   - Open DevTools (F12)
   - Go to Application → Local Storage → Clear All
   - Go to Application → Cookies → Clear All
2. **Refresh page:** `Ctrl+Shift+R` (hard refresh)

3. **Test login flow:**
   - Click "Sign in with GitHub"
   - You should go to `github.com` (not stay on GitHub)
   - After authorizing, you should come back to `http://localhost:3000/auth/callback`
   - You should see "Authenticating..." message
   - After ~2 seconds, redirect to dashboard
   - Dashboard should show your repositories

---

## If Your Callback URL is Wrong

### How to Fix It

1. Go to your GitHub OAuth app: https://github.com/settings/developers
2. Click your app name
3. Scroll to "Authorization callback URL"
4. Clear the field
5. Enter EXACTLY: `http://localhost:3000/auth/callback`
6. Click "Update application"
7. Wait 30 seconds (GitHub caches settings)
8. Try login again

---

## GitHub Token Scopes

Your app needs these permissions. When you login, GitHub will ask for:

```
✅ public_repo  - Can read public repositories
✅ user         - Can read user profile
✅ workflow     - Can manage workflows for deployment
```

If you don't see these scopes requested, something is wrong with your app config.

---

## For Production

When deploying to production, change these:

**GitHub OAuth App Settings:**

```
Authorization callback URL:
❌ http://localhost:3000/auth/callback
✅ https://yourdomain.com/auth/callback
```

**backend/.env:**

```bash
GITHUB_REDIRECT_URI=https://yourdomain.com/auth/callback
FRONTEND_URL=https://yourdomain.com
```

**frontend/.env:**

```bash
VITE_API_BASE_URL=https://api.yourdomain.com
```

---

## Troubleshooting Visual Guide

### Scenario 1: Stays on GitHub after authorization

```
┌─ WRONG SETUP ─┐
│               │
│  GitHub OAuth │ ❌ Wrong callback URL in GitHub settings
│  Still shows  │ ❌ Redirect not pointing to app
│  GitHub page  │
│               │
└───────────────┘
   FIX: Update GitHub OAuth app callback URL to:
        http://localhost:3000/auth/callback
```

### Scenario 2: Error "Authorization failed"

```
┌─ WRONG SETUP ─┐
│               │
│  Error message│ ❌ Client ID/Secret mismatch
│  on page      │ ❌ Wrong environment variables
│  "Auth failed"│ ❌ Outdated credentials
│               │
└───────────────┘
   FIX: 1. Regenerate Client Secret in GitHub
        2. Copy to backend/.env
        3. Restart backend
```

### Scenario 3: Cannot reach callback URL

```
┌─ WRONG SETUP ─┐
│               │
│  Error page   │ ❌ Frontend not running
│  "Cannot GET" │ ❌ Port 3000 not accessible
│               │ ❌ React Router missing route
│               │
└───────────────┘
   FIX: 1. Check frontend is running: http://localhost:3000
        2. Check /auth/callback route exists in App.tsx
        3. Check Docker: docker-compose ps
```

---

## Quick Reference

| Setting                    | Value                               |
| -------------------------- | ----------------------------------- |
| **Application Name**       | Deployment Orchestration Platform   |
| **Homepage URL**           | http://localhost:3000               |
| **Callback URL**           | http://localhost:3000/auth/callback |
| **Client ID Location**     | backend/.env, frontend/.env         |
| **Client Secret Location** | backend/.env only                   |
| **Scope**                  | repo, user, workflow                |

---

## Common Mistakes

❌ **Mistake 1:** Using `https://` for localhost

```
WRONG: https://localhost:3000/auth/callback
RIGHT: http://localhost:3000/auth/callback
```

❌ **Mistake 2:** Trailing slash

```
WRONG: http://localhost:3000/auth/callback/
RIGHT: http://localhost:3000/auth/callback
```

❌ **Mistake 3:** Wrong port

```
WRONG: http://localhost:8000/auth/callback (backend port)
RIGHT: http://localhost:3000/auth/callback (frontend port)
```

❌ **Mistake 4:** Wrong path

```
WRONG: http://localhost:3000/callback
RIGHT: http://localhost:3000/auth/callback
```

---

## Success Indicators

After proper setup, you should see:

✅ **On Login Page:**

- "Sign in with GitHub" button works
- Redirects to `github.com` authorization

✅ **On GitHub Authorization:**

- Shows app name "Deployment Orchestration Platform"
- Shows required scopes
- "Authorize" button available

✅ **After Authorization:**

- Redirected back to `http://localhost:3000/auth/callback`
- "Authenticating..." message shows
- After 2 seconds, redirected to dashboard
- Dashboard shows your repositories from GitHub

---

**You're all set! Your OAuth configuration is now correct.** ✨

**Next:** Return to the application and test the login flow.
