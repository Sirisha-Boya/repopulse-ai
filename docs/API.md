# API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

All endpoints (except `/auth/github/login` and `/auth/github/callback`) require JWT authentication via the `Authorization` header:

```
Authorization: Bearer {access_token}
```

## Endpoints

### Authentication

#### Get GitHub Login URL

```
GET /auth/github/login

Response:
{
  "oauth_url": "https://github.com/login/oauth/authorize?...",
  "state": "uuid-string"
}
```

#### GitHub OAuth Callback

```
POST /auth/github/callback

Body:
{
  "code": "authorization-code-from-github"
}

Response:
{
  "access_token": "jwt-token",
  "refresh_token": "jwt-refresh-token",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "github_id": 12345,
    "github_username": "octocat",
    "email": "octocat@github.com",
    "avatar_url": "https://avatars.githubusercontent.com/u/1?",
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00Z",
    "last_login": "2024-01-02T00:00:00Z"
  }
}
```

#### Refresh Token

```
POST /auth/refresh

Body:
{
  "refresh_token": "jwt-refresh-token"
}

Response:
{
  "access_token": "new-jwt-token",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### Get Current User

```
GET /auth/me

Response:
{
  "id": 1,
  "github_id": 12345,
  "github_username": "octocat",
  "email": "octocat@github.com",
  "avatar_url": "https://avatars.githubusercontent.com/u/1?",
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-02T00:00:00Z"
}
```

#### Logout

```
POST /auth/logout

Response:
{
  "message": "Successfully logged out"
}
```

### Repositories

#### Sync Repositories from GitHub

```
POST /repositories/sync

Response:
{
  "message": "Synced 15 repositories",
  "count": 15
}
```

#### List User Repositories

```
GET /repositories?page=1&page_size=20

Response:
{
  "total": 42,
  "repositories": [
    {
      "id": 1,
      "name": "my-project",
      "full_name": "octocat/my-project",
      "description": "A sample project",
      "url": "https://github.com/octocat/my-project",
      "default_branch": "main",
      "language": "javascript",
      "is_private": false,
      "stars": 10,
      "last_pushed_at": "2024-01-02T00:00:00Z",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-02T00:00:00Z"
    }
  ],
  "page": 1,
  "page_size": 20
}
```

#### Search Repositories

```
GET /repositories/search?q=my-project&page=1&page_size=20

Response:
{
  "total": 1,
  "repositories": [...],
  "page": 1,
  "page_size": 20
}
```

#### Get Repository Details

```
GET /repositories/{repo_id}

Response:
{
  "id": 1,
  "name": "my-project",
  "full_name": "octocat/my-project",
  "description": "A sample project",
  "url": "https://github.com/octocat/my-project",
  "default_branch": "main",
  "language": "javascript",
  "is_private": false,
  "stars": 10,
  "last_pushed_at": "2024-01-02T00:00:00Z",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

#### Delete Repository

```
DELETE /repositories/{repo_id}

Response:
{
  "message": "Repository deleted"
}
```

## Error Responses

All errors follow this format:

```
{
  "error": "Error type",
  "detail": "Detailed error message",
  "request_id": "unique-request-id"
}
```

### Common Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

## Rate Limiting

- **Authenticated Requests**: 1000 requests/hour
- **Unauthenticated Requests**: 100 requests/hour

## Webhook Events

(Coming in Phase 3)

- `deployment.started`
- `deployment.completed`
- `deployment.failed`
- `deployment.rolled_back`

## Pagination

List endpoints support pagination:

```
?page=1&page_size=20
```

- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

## Filtering and Sorting

(Coming in Phase 2)

- `?sort=name` - Sort by field
- `?order=asc` - Sort order (asc/desc)
- `?filter[status]=active` - Filter by status

---

For interactive API documentation, visit: `/docs` (Swagger UI) or `/redoc` (ReDoc)
