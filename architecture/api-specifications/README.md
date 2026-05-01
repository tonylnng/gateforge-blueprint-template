# API Specifications Guide

> **First action for the Architect:** open [`../AGENTS.md`](../AGENTS.md) and complete the Pre-Flight Acknowledgement before adding or modifying any OpenAPI spec. Per [`/VERSIONING.md`](../../VERSIONING.md), every push triggers an auto-version-bump; OpenAPI breaking changes additionally require a new ADR (gate ARC-G3).

<!--
  PURPOSE: Define conventions, naming rules, and structure for all OpenAPI specification files
           in this directory. Includes a complete example skeleton and common shared schemas.
  OWNER: System Architect
  
  INSTRUCTIONS FOR THE ARCHITECT:
  1. Create one OpenAPI YAML file per NestJS service module.
  2. Follow the naming convention: <service-name>.openapi.yaml
  3. All specs must use OpenAPI 3.0.3 format.
  4. Use the common response schemas defined in this README.
  5. Every endpoint must include authentication requirements.
  6. Review requirements/functional-requirements.md Section 5.2 for the endpoint inventory.
-->

## Overview

This directory contains **OpenAPI 3.0 specification files** for every API service in the GateForge platform. Each file is a self-contained, machine-readable contract that defines endpoints, request/response schemas, authentication, and error handling for a single service.

**These specs serve as:**
- The contract between frontend and backend developers
- Input for automated API documentation (Swagger UI)
- Input for API client code generation
- Validation rules for request/response testing by QC Agents

---

## File Naming Convention

```
<service-name>.openapi.yaml
```

| Service | Filename | Description |
|---------|----------|-------------|
| Auth Service | `auth-service.openapi.yaml` | Registration, login, token management, password reset |
| [PLACEHOLDER] Service | `[placeholder]-service.openapi.yaml` | [PLACEHOLDER] |
| [PLACEHOLDER] Service | `[placeholder]-service.openapi.yaml` | [PLACEHOLDER] |

<!--
  Add one row per service. The service name must match the NestJS module name in kebab-case.
-->

---

## API Versioning Rules

| Rule | Detail |
|------|--------|
| **Versioning scheme** | URL path prefix: `/v1/`, `/v2/`, etc. |
| **Current version** | `/v1/` |
| **When to bump version** | Breaking changes only: removing fields, changing field types, removing endpoints, changing response structure. |
| **Non-breaking changes** | Adding new optional fields, adding new endpoints, adding new enum values. These do NOT require a version bump. |
| **Deprecation policy** | Deprecated versions are supported for a minimum of [PLACEHOLDER — e.g., 6 months] after the successor version is released. |
| **Deprecation signaling** | Deprecated endpoints return `Deprecation: true` header and `Sunset: <date>` header (RFC 8594). |
| **Base path** | `https://api.[PLACEHOLDER — domain.com]/v1/` |

---

## Authentication Header Requirements

All authenticated endpoints must include the following header:

```
Authorization: Bearer <access_token>
```

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes (on protected endpoints) | JWT access token in Bearer scheme |
| `X-Refresh-Token` | Yes (on `/v1/auth/refresh` only) | Refresh token for obtaining new access tokens |
| `X-Trace-Id` | Auto-injected by API Gateway | Distributed trace ID for request correlation |
| `Content-Type` | Yes (on request body) | `application/json` |
| `Accept` | Recommended | `application/json` |

### Authentication Scopes

| Scope | Description | Endpoints |
|-------|-------------|-----------|
| `public` | No authentication required | `POST /v1/auth/register`, `POST /v1/auth/login`, `POST /v1/auth/reset-password` |
| `user` | Valid access token with any role | All user-facing endpoints |
| `admin` | Valid access token with `admin` or `super_admin` role | `GET /v1/admin/*`, `PUT /v1/admin/*`, `DELETE /v1/admin/*` |
| `super_admin` | Valid access token with `super_admin` role only | System configuration endpoints |

---

## Common Response Schemas

<!--
  These schemas must be used consistently across ALL API specs.
  Reference them via $ref in each OpenAPI file.
-->

### Success Response

```yaml
# Standard success response wrapper
SuccessResponse:
  type: object
  required:
    - success
    - data
  properties:
    success:
      type: boolean
      example: true
    data:
      type: object
      description: "Response payload — varies per endpoint"
    meta:
      $ref: "#/components/schemas/PaginationMeta"
      description: "Present only on paginated list endpoints"
```

### Error Response

```yaml
# Standard error response
ErrorResponse:
  type: object
  required:
    - success
    - error
  properties:
    success:
      type: boolean
      example: false
    error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: "Machine-readable error code"
          example: "VALIDATION_ERROR"
        message:
          type: string
          description: "Human-readable error message"
          example: "Email address is already registered."
        details:
          type: array
          description: "Field-level validation errors (optional)"
          items:
            type: object
            properties:
              field:
                type: string
                example: "email"
              message:
                type: string
                example: "Must be a valid email address"
        traceId:
          type: string
          description: "Request trace ID for debugging"
          example: "abc123-def456-ghi789"
```

### Pagination Meta

```yaml
PaginationMeta:
  type: object
  required:
    - page
    - limit
    - total
    - totalPages
  properties:
    page:
      type: integer
      description: "Current page number (1-based)"
      example: 1
    limit:
      type: integer
      description: "Items per page"
      example: 20
    total:
      type: integer
      description: "Total number of items"
      example: 150
    totalPages:
      type: integer
      description: "Total number of pages"
      example: 8
```

### Common Error Codes

| HTTP Status | Error Code | Description | When to Use |
|------------|-----------|-------------|-------------|
| 400 | `VALIDATION_ERROR` | Request body or query params failed validation | Missing required fields, wrong types, constraint violations |
| 401 | `UNAUTHORIZED` | Missing or invalid authentication token | No `Authorization` header, expired token, malformed token |
| 403 | `FORBIDDEN` | Valid token but insufficient permissions | User role does not have access to the resource |
| 404 | `NOT_FOUND` | Requested resource does not exist | Entity ID not found in database |
| 409 | `CONFLICT` | Request conflicts with current state | Duplicate email registration, version conflict |
| 422 | `UNPROCESSABLE_ENTITY` | Request is syntactically valid but semantically wrong | Business rule violation |
| 429 | `RATE_LIMITED` | Too many requests | Rate limit exceeded (see NFR-SEC-007) |
| 500 | `INTERNAL_ERROR` | Unexpected server error | Unhandled exception (never expose stack traces) |

---

## Example OpenAPI Skeleton

<!--
  This is a complete, working example for the Auth Service.
  Use this as the starting template for every new service spec file.
  Copy this to auth-service.openapi.yaml and fill in the remaining endpoints.
-->

```yaml
openapi: 3.0.3
info:
  title: Auth Service API
  description: |
    Authentication and authorization service for the GateForge platform.
    Handles user registration, login, token management, and password reset.
  version: 1.0.0
  contact:
    name: System Architect
    email: "[PLACEHOLDER — architect email]"

servers:
  - url: https://api.[PLACEHOLDER — domain.com]/v1
    description: Production
  - url: https://api.staging.[PLACEHOLDER — domain.com]/v1
    description: Staging
  - url: http://localhost:3000/v1
    description: Local development

tags:
  - name: Authentication
    description: Registration, login, and token operations
  - name: Password Management
    description: Password reset and change operations

paths:
  /auth/register:
    post:
      tags:
        - Authentication
      summary: Register a new user
      description: |
        Creates a new user account with `pending_verification` status.
        Sends a verification email to the provided address.
        
        **Source:** FR-AUTH-001
      operationId: registerUser
      security: []  # Public endpoint
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  format: email
                  maxLength: 320
                  example: "user@example.com"
                password:
                  type: string
                  format: password
                  minLength: 8
                  maxLength: 128
                  description: "Must contain ≥1 uppercase, ≥1 number, ≥1 special character"
                  example: "SecureP@ss1"
      responses:
        "201":
          description: User created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  data:
                    type: object
                    properties:
                      userId:
                        type: string
                        format: uuid
                        example: "550e8400-e29b-41d4-a716-446655440000"
                      message:
                        type: string
                        example: "Registration successful. Please check your email for verification."
        "400":
          description: Validation error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
              example:
                success: false
                error:
                  code: "VALIDATION_ERROR"
                  message: "Invalid request body"
                  details:
                    - field: "password"
                      message: "Must contain at least one uppercase letter"
        "409":
          description: Email already registered
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
              example:
                success: false
                error:
                  code: "CONFLICT"
                  message: "An account with this email address already exists."

  /auth/login:
    post:
      tags:
        - Authentication
      summary: Authenticate a user
      description: |
        Validates credentials and returns JWT access token + refresh token.
        
        **Source:** FR-AUTH-001
      operationId: loginUser
      security: []  # Public endpoint
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  format: email
                  example: "user@example.com"
                password:
                  type: string
                  format: password
                  example: "SecureP@ss1"
      responses:
        "200":
          description: Login successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  data:
                    type: object
                    properties:
                      accessToken:
                        type: string
                        description: "JWT access token (expires in 15 min)"
                        example: "eyJhbGciOiJIUzI1NiIs..."
                      refreshToken:
                        type: string
                        description: "Refresh token (expires in 7 days)"
                        example: "dGhpcyBpcyBhIHJlZnJl..."
                      expiresIn:
                        type: integer
                        description: "Access token TTL in seconds"
                        example: 900
        "401":
          description: Invalid credentials
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
        "429":
          description: Rate limit exceeded
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"

  /auth/refresh:
    post:
      tags:
        - Authentication
      summary: Refresh access token
      description: |
        Exchanges a valid refresh token for a new access token.
        Implements refresh token rotation — the old refresh token is invalidated.
      operationId: refreshToken
      security: []  # Uses refresh token, not access token
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - refreshToken
              properties:
                refreshToken:
                  type: string
                  example: "dGhpcyBpcyBhIHJlZnJl..."
      responses:
        "200":
          description: Token refreshed
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  data:
                    type: object
                    properties:
                      accessToken:
                        type: string
                      refreshToken:
                        type: string
                        description: "New refresh token (old one is now invalid)"
                      expiresIn:
                        type: integer
                        example: 900
        "401":
          description: Invalid or expired refresh token

  /auth/reset-password:
    post:
      tags:
        - Password Management
      summary: Request password reset
      description: |
        Sends a password reset email with a single-use, time-limited token.
        Always returns 200 regardless of whether the email exists (prevents enumeration).
        
        **Source:** FR-AUTH-003
      operationId: requestPasswordReset
      security: []  # Public endpoint
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
              properties:
                email:
                  type: string
                  format: email
                  example: "user@example.com"
      responses:
        "200":
          description: Reset email sent (or silently ignored if email not found)
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  data:
                    type: object
                    properties:
                      message:
                        type: string
                        example: "If an account exists with this email, a reset link has been sent."

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: "JWT access token obtained from /auth/login"

  schemas:
    ErrorResponse:
      type: object
      required:
        - success
        - error
      properties:
        success:
          type: boolean
          example: false
        error:
          type: object
          required:
            - code
            - message
          properties:
            code:
              type: string
              example: "VALIDATION_ERROR"
            message:
              type: string
              example: "Invalid request body"
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                  message:
                    type: string
            traceId:
              type: string
              example: "abc123-def456"

    PaginationMeta:
      type: object
      properties:
        page:
          type: integer
          example: 1
        limit:
          type: integer
          example: 20
        total:
          type: integer
          example: 150
        totalPages:
          type: integer
          example: 8

security:
  - BearerAuth: []
```

---

## Creating a New API Spec File

### Step-by-Step

1. **Copy the skeleton** above into a new file: `<service-name>.openapi.yaml`.
2. **Update `info`** — title, description, version.
3. **Update `servers`** — adjust URLs if the service has a different base path.
4. **Define `tags`** — one tag per logical group of endpoints.
5. **Add `paths`** — one path per endpoint from `requirements/functional-requirements.md` Section 5.2.
6. **Define `components/schemas`** — request/response models derived from `architecture/data-model.md`.
7. **Set `security`** — use `security: []` for public endpoints; default `BearerAuth` for protected.
8. **Add examples** — every request and response must have realistic example values.
9. **Link to requirements** — include `**Source:** FR-XXX-NNN` in each endpoint description.

### Validation Checklist

- [ ] File name follows `<service-name>.openapi.yaml` convention
- [ ] OpenAPI version is `3.0.3`
- [ ] All endpoints have `operationId`
- [ ] All request bodies have `required` fields listed
- [ ] All responses include both success and error cases
- [ ] Error responses use the standard `ErrorResponse` schema
- [ ] Paginated responses include `PaginationMeta`
- [ ] Authentication requirements are explicit per endpoint
- [ ] Examples are realistic and consistent with data model
- [ ] Every endpoint references its source FR in the description

---

## Directory Structure

```
api-specifications/
├── README.md                          # This file — conventions and example skeleton
├── auth-service.openapi.yaml          # Auth Service: registration, login, tokens, password
├── [placeholder]-service.openapi.yaml # [PLACEHOLDER — next service]
└── [placeholder]-service.openapi.yaml # [PLACEHOLDER — next service]
```

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | YYYY-MM-DD | System Architect | Initial guide and auth service skeleton created |
| | | | |
