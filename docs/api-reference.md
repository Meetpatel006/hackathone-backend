# API Reference

This document provides detailed information about the Runtime Traitors Backend API endpoints.

## Base Information

- **Base URL**: `http://localhost:8000` (development)
- **API Version**: v1
- **Authentication**: JWT Bearer tokens
- **Content Type**: `application/json`
- **Date Format**: ISO 8601 (`YYYY-MM-DDTHH:mm:ssZ`)

## Authentication

All authenticated endpoints require a valid JWT token in the Authorization header:

```http
Authorization: Bearer <your-jwt-token>
```

### Authentication Flow

1. **Login** to get access token
2. **Use access token** for API requests
3. **Logout** to invalidate tokens

## Response Format

All API responses follow a consistent format:

### Success Response
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Operation completed successfully",
  "timestamp": "2025-01-01T12:00:00Z"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": ["This field is required"]
    }
  },
  "timestamp": "2025-01-01T12:00:00Z"
}
```

## Authentication Endpoints

The default role for a new user is 'user'. Administrator accounts are created directly in the database with the 'admin' role.

### POST /api/v1/auth/login

Authenticate user and receive tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "expires_in": 1800,
    "user": {
      "id": "user-id",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "user"
    }
  }
}
```

**Status Codes:**
- `200 OK` - Login successful
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Invalid credentials
- `429 Too Many Requests` - Rate limit exceeded

### POST /api/v1/auth/logout

Logout and invalidate tokens.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### POST /api/v1/auth/register

Register a new user account.

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "password": "securepassword123",
  "first_name": "Jane",
  "last_name": "Smith",
  "terms_accepted": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "new-user-id",
      "email": "newuser@example.com",
      "first_name": "Jane",
      "last_name": "Smith",
      "role": "user",
  
      "created_at": "2025-01-01T12:00:00Z"
    }
  },
  "message": "User registered successfully"
}
```

## User Management Endpoints

### GET /api/v1/users/me

Get current user profile.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "user-id",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",

    "created_at": "2025-01-01T12:00:00Z",
    "updated_at": "2025-01-01T12:00:00Z",
    "last_login": "2025-01-01T11:30:00Z"
  }
}
```

### PUT /api/v1/users/me

Update current user profile.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "user-id",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "updated_at": "2025-01-01T12:30:00Z"
  }
}
```

### DELETE /api/v1/users/me

Delete current user account.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "password": "current-password",
  "confirmation": "DELETE"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Account deleted successfully"
}
```

## Admin Endpoints

### GET /api/v1/admin/users

List users (Admin only).

**Headers:**
```http
Authorization: Bearer <admin-access-token>
```

**Query Parameters:**
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Items per page (default: 10, max: 100)
- `search` (string, optional): Search by name or email
- `role` (string, optional): Filter by role (`user`, `admin`)
- `status` (string, optional): Filter by status (`active`, `inactive`, `banned`)

**Example:**
```http
GET /api/v1/users?page=1&limit=20&search=john&role=user
```

**Response:**
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": "user-id",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "user",
        "status": "active",
        "created_at": "2025-01-01T12:00:00Z",
        "last_login": "2025-01-01T11:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "pages": 8,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

### GET /api/v1/admin/users/{user_id}

Get user by ID (Admin only).

**Headers:**
```http
Authorization: Bearer <admin-access-token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "user-id",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "status": "active",

    "created_at": "2025-01-01T12:00:00Z",
    "updated_at": "2025-01-01T12:00:00Z",
    "last_login": "2025-01-01T11:30:00Z"
  }
}
```

### PUT /api/v1/admin/users/{user_id}

Update user (Admin only).

**Headers:**
```http
Authorization: Bearer <admin-access-token>
```

**Request Body:**
```json
{
  "role": "admin",
  "status": "active"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "user-id",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "admin",
    "status": "active",
    "updated_at": "2025-01-01T12:30:00Z"
  }
}
```

### DELETE /api/v1/admin/users/{user_id}

Delete user (Admin only).

**Headers:**
```http
Authorization: Bearer <admin-access-token>
```

**Response:**
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

### GET /api/v1/admin/stats

Get system statistics (Admin only).

**Headers:**
```http
Authorization: Bearer <admin-access-token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "users": {
      "total": 1500,
      "active": 1200,
      "new_today": 25,
      "new_this_week": 150
    },
    "files": {
      "total": 5000,
      "total_size": "2.5 GB",
      "uploaded_today": 50,
      "uploaded_this_week": 300
    },
    "api": {
      "requests_today": 10000,
      "requests_this_week": 50000,
      "avg_response_time": 120,
      "error_rate": 0.5
    },
    "system": {
      "uptime": "15 days, 3 hours",
      "memory_usage": "75%",
      "cpu_usage": "45%",
      "disk_usage": "60%"
    }
  }
}
```

### GET /api/v1/admin/logs

Get system logs (Admin only).

**Headers:**
```http
Authorization: Bearer <admin-access-token>
```

**Query Parameters:**
- `level` (string, optional): Log level (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- `start_date` (string, optional): Start date (ISO format)
- `end_date` (string, optional): End date (ISO format)
- `page` (int, optional): Page number
- `limit` (int, optional): Items per page

**Response:**
```json
{
  "success": true,
  "data": {
    "logs": [
      {
        "id": "log-id",
        "level": "ERROR",
        "message": "Database connection failed",
        "timestamp": "2025-01-01T12:00:00Z",
        "source": "database",
        "details": {
          "error": "Connection timeout",
          "duration": 5000
        }
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 50,
      "total": 1000,
      "pages": 20
    }
  }
}
```

## File Upload Endpoints

### POST /api/v1/uploads

Upload a file.

**Headers:**
```http
Authorization: Bearer <access-token>
Content-Type: multipart/form-data
```

**Request Body:**
```
file: (binary file data)
folder: (optional) string - destination folder
```

**Response:**
```json
{
  "success": true,
  "data": {
    "file_id": "file-uuid",
    "filename": "document.pdf",
    "original_filename": "my-document.pdf",
    "url": "https://storage.azure.com/uploads/file-uuid",
    "size": 1048576,
    "content_type": "application/pdf",
    "folder": "documents",
    "uploaded_by": "user-id",
    "created_at": "2025-01-01T12:00:00Z"
  }
}
```

**File Constraints:**
- Maximum file size: 50MB
- Allowed types: Images (jpg, png, gif), Documents (pdf, doc, docx), Archives (zip, tar)
- Virus scanning enabled
- Automatic file type detection

### GET /api/v1/uploads

List user's uploaded files.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Items per page (default: 10)
- `folder` (string, optional): Filter by folder
- `content_type` (string, optional): Filter by content type

**Response:**
```json
{
  "success": true,
  "data": {
    "files": [
      {
        "file_id": "file-uuid",
        "filename": "document.pdf",
        "url": "https://storage.azure.com/uploads/file-uuid",
        "size": 1048576,
        "content_type": "application/pdf",
        "created_at": "2025-01-01T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 25,
      "pages": 3,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

### GET /api/v1/uploads/{file_id}

Get file information.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "file_id": "file-uuid",
    "filename": "document.pdf",
    "original_filename": "my-document.pdf",
    "url": "http://localhost:8000/api/v1/uploads/file-uuid/download",
    "size": 1048576,
    "content_type": "application/pdf",
    "folder": "documents",
    "uploaded_by": "user-id",
    "created_at": "2025-01-01T12:00:00Z",
    "metadata": {
      "pages": 10,
      "author": "John Doe"
    }
  }
}
```

### GET /api/v1/uploads/{file_id}/download

Download file.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
- Status: `200 OK`
- Headers: 
  - `Content-Type`: File's content type
  - `Content-Disposition`: `attachment; filename="filename.ext"`
  - `Content-Length`: File size
- Body: File binary data

### DELETE /api/v1/uploads/{file_id}

Delete file.

**Headers:**
```http
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "success": true,
  "message": "File deleted successfully"
}
```

## Health Check Endpoints

### GET /health

Application health check.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-01T12:00:00Z",
  "version": "1.0.0",
  "uptime": "15 days, 3 hours"
}
```

### GET /health/db

Database health check.

**Response:**
```json
{
  "status": "healthy",
  "database": {
    "connected": true,
    "response_time": 25,
    "connections": {
      "active": 5,
      "max": 100
    }
  }
}
```


### GET /health/storage

Storage health check.

**Response:**
```json
{
  "status": "healthy",
  "storage": {
    "connected": true,
    "response_time": 150,
    "available_space": "500 GB",
    "used_space": "250 GB"
  }
}
```

## Error Codes

### Authentication Errors
- `INVALID_CREDENTIALS` - Wrong email or password
- `TOKEN_EXPIRED` - JWT token has expired
- `TOKEN_INVALID` - JWT token is malformed or invalid
- `INSUFFICIENT_PERMISSIONS` - User lacks required permissions
- `ACCOUNT_DISABLED` - User account is disabled or banned

### Validation Errors
- `VALIDATION_ERROR` - Request data validation failed
- `MISSING_FIELD` - Required field is missing
- `INVALID_FORMAT` - Field format is invalid
- `VALUE_TOO_LONG` - Field value exceeds maximum length
- `VALUE_TOO_SHORT` - Field value is below minimum length

### Resource Errors
- `RESOURCE_NOT_FOUND` - Requested resource doesn't exist
- `RESOURCE_ALREADY_EXISTS` - Resource with same identifier exists
- `RESOURCE_LOCKED` - Resource is locked and cannot be modified
- `RESOURCE_DELETED` - Resource has been deleted

### System Errors
- `INTERNAL_SERVER_ERROR` - Unexpected server error
- `SERVICE_UNAVAILABLE` - Service is temporarily unavailable
- `DATABASE_ERROR` - Database operation failed
- `STORAGE_ERROR` - File storage operation failed
- `RATE_LIMIT_EXCEEDED` - Too many requests

### File Upload Errors
- `FILE_TOO_LARGE` - File size exceeds limit
- `INVALID_FILE_TYPE` - File type not allowed
- `STORAGE_QUOTA_EXCEEDED` - User storage quota exceeded

## Rate Limiting

API endpoints are rate limited to prevent abuse:

### Limits
- **Authentication endpoints**: 5 requests per minute
- **General API endpoints**: 60 requests per minute
- **File upload endpoints**: 10 requests per minute
- **Admin endpoints**: 100 requests per minute

### Headers
Rate limit information is included in response headers:

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640995200
```

### Rate Limit Exceeded Response
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "retry_after": 60
  }
}
```

## Pagination

List endpoints support pagination with the following parameters:

### Query Parameters
- `page` (int): Page number (starts from 1)
- `limit` (int): Items per page (max 100)

### Response Format
```json
{
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 100,
      "pages": 10,
      "has_next": true,
      "has_prev": false,
      "next_page": 2,
      "prev_page": null
    }
  }
}
```

---

This API reference provides comprehensive documentation for all available endpoints. For additional information or support, please refer to the main README or contact the development team.
