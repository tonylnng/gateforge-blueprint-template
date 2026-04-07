# Coding Standards — Quick Reference

<!-- AGENT INSTRUCTION: This is a compact quick-reference for coding standards.
     The full, detailed development guide is in DEVELOPMENT-GUIDE.md at the repository root.
     Developer agents (VM-3) should reference this for day-to-day conventions.
     The System Architect maintains this document. -->

| Field | Value |
|---|---|
| **Document ID** | DEV-STANDARDS-001 |
| **Version** | 0.1.0 |
| **Owner** | System Architect |
| **Status** | Draft |
| **Last Updated** | [PLACEHOLDER] |

> **Full guide:** See [DEVELOPMENT-GUIDE.md](../DEVELOPMENT-GUIDE.md) for detailed standards, patterns, and architectural decisions.

---

## 1. TypeScript Configuration Summary

<!-- AGENT INSTRUCTION: These are the key tsconfig settings. The full tsconfig.json is in the project root. -->

| Setting | Value | Rationale |
|---|---|---|
| `strict` | `true` | Enables all strict type-checking options |
| `target` | `ES2022` | Modern JS features, aligns with Node.js LTS |
| `module` | `NodeNext` | Native ESM support for NestJS backend |
| `moduleResolution` | `NodeNext` | Consistent with module setting |
| `esModuleInterop` | `true` | Allows default imports from CommonJS modules |
| `forceConsistentCasingInFileNames` | `true` | Prevents cross-platform casing bugs |
| `noUncheckedIndexedAccess` | `true` | Arrays/objects return `T | undefined` on index access |
| `exactOptionalPropertyTypes` | `true` | Distinguishes between `undefined` and missing |
| `noImplicitReturns` | `true` | All code paths must return a value |
| `noFallthroughCasesInSwitch` | `true` | Prevents accidental switch fallthrough |

---

## 2. Naming Conventions

| Element | Convention | Example |
|---|---|---|
| **Files (components)** | PascalCase | `UserProfile.tsx` |
| **Files (modules/services)** | kebab-case | `user-profile.service.ts` |
| **Files (tests)** | Same as source + `.spec` | `user-profile.service.spec.ts` |
| **Classes** | PascalCase | `UserProfileService` |
| **Interfaces** | PascalCase (no `I` prefix) | `UserProfile` |
| **Types** | PascalCase | `CreateUserDto` |
| **Enums** | PascalCase, members UPPER_SNAKE | `enum Role { ADMIN, USER }` |
| **Functions** | camelCase | `getUserProfile()` |
| **Variables** | camelCase | `const userName = ...` |
| **Constants** | UPPER_SNAKE_CASE | `const MAX_RETRY_COUNT = 3` |
| **Database tables** | snake_case, plural | `user_profiles` |
| **Database columns** | snake_case | `created_at` |
| **API endpoints** | kebab-case, plural nouns | `/api/v1/user-profiles` |
| **Environment variables** | UPPER_SNAKE_CASE | `DATABASE_URL` |
| **CSS classes (Tailwind)** | Utility-first | `className="flex items-center"` |
| **React hooks** | camelCase, `use` prefix | `useUserProfile()` |

---

## 3. File Structure Convention

<!-- AGENT INSTRUCTION: GateForge uses feature-based folder structure, not type-based. -->

```
src/
├── modules/
│   ├── auth/
│   │   ├── auth.module.ts
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── auth.service.spec.ts
│   │   ├── auth.guard.ts
│   │   ├── dto/
│   │   │   ├── login.dto.ts
│   │   │   └── register.dto.ts
│   │   ├── entities/
│   │   │   └── user.entity.ts
│   │   └── interfaces/
│   │       └── auth-payload.interface.ts
│   ├── user-profile/
│   │   ├── user-profile.module.ts
│   │   ├── user-profile.controller.ts
│   │   ├── user-profile.service.ts
│   │   └── ...
│   └── ...
├── common/
│   ├── decorators/
│   ├── filters/
│   ├── guards/
│   ├── interceptors/
│   ├── pipes/
│   └── utils/
├── config/
│   ├── app.config.ts
│   ├── database.config.ts
│   └── redis.config.ts
└── main.ts
```

---

## 4. Import Ordering Rules

<!-- AGENT INSTRUCTION: Enforce via ESLint `import/order` rule. -->

Imports must follow this order, separated by blank lines:

1. **Node.js built-in modules** — `fs`, `path`, `crypto`
2. **External packages** — `@nestjs/*`, `react`, `class-validator`
3. **Internal aliases** — `@/common/*`, `@/config/*`
4. **Relative imports** — `./dto/login.dto`, `../shared/utils`

```typescript
// 1. Node built-ins
import { randomUUID } from 'crypto';

// 2. External packages
import { Injectable, HttpException, HttpStatus } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

// 3. Internal aliases
import { AppLogger } from '@/common/logger';
import { RedisService } from '@/config/redis.config';

// 4. Relative imports
import { CreateUserDto } from './dto/create-user.dto';
import { User } from './entities/user.entity';
```

---

## 5. Error Handling Standards

<!-- AGENT INSTRUCTION: Summary rules. Full patterns in DEVELOPMENT-GUIDE.md. -->

| Rule | Description |
|---|---|
| Never swallow errors | Always log or rethrow. No empty `catch {}` blocks. |
| Use typed exceptions | Throw `HttpException` with appropriate status code (NestJS). Use custom exception classes for domain errors. |
| Validate inputs at boundary | Use `class-validator` + `ValidationPipe` on all DTOs. |
| Centralized error filter | Global exception filter catches unhandled errors, logs them, returns standard error response. |
| Return standard error shape | `{ statusCode, message, error, timestamp, path }` |
| No stack traces in production | Stack traces only in development. Production returns sanitized messages. |
| Async errors | Always use `try/catch` in `async` functions. Never leave unhandled promise rejections. |

---

## 6. Git Conventions

### Branch Naming

| Type | Pattern | Example |
|---|---|---|
| Feature | `feature/<module>/<short-description>` | `feature/auth/social-login` |
| Bugfix | `fix/<module>/<short-description>` | `fix/auth/token-refresh-race` |
| Hotfix | `hotfix/v<X.Y.Z>` | `hotfix/v1.0.1` |
| Release | `release/v<X.Y.Z>` | `release/v1.0.0` |
| Chore | `chore/<description>` | `chore/update-dependencies` |

### Commit Message Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

| Type | When to Use |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, white-space (no logic change) |
| `refactor` | Code restructuring (no behavior change) |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `chore` | Build, CI, tooling changes |

### PR Checklist

| # | Item |
|---|---|
| 1 | PR title follows commit format: `<type>(<scope>): <subject>` |
| 2 | Linked to backlog item / issue |
| 3 | All CI checks passing |
| 4 | Self-review completed |
| 5 | Module documentation updated (if applicable) |
| 6 | No `console.log` or debug statements left in code |

---

## 7. Code Review Checklist

<!-- AGENT INSTRUCTION: Reviewers must verify all items. Mark pass/fail for each. -->

| # | Category | Check |
|---|---|---|
| 1 | **Correctness** | Does the code do what it's supposed to do? |
| 2 | **Correctness** | Are edge cases handled (null, empty, boundary values)? |
| 3 | **Correctness** | Are error conditions handled appropriately? |
| 4 | **Security** | No hardcoded secrets, API keys, or credentials |
| 5 | **Security** | Input validation present on all external inputs |
| 6 | **Security** | SQL injection / NoSQL injection prevention verified |
| 7 | **Security** | Authentication and authorization checks in place |
| 8 | **Performance** | No N+1 queries or unbounded data fetches |
| 9 | **Performance** | Database queries use appropriate indexes |
| 10 | **Performance** | Large data sets use pagination |
| 11 | **Style** | Naming conventions followed (Section 2) |
| 12 | **Style** | Import ordering rules followed (Section 4) |
| 13 | **Tests** | Unit tests cover new/changed logic |
| 14 | **Tests** | Tests are meaningful (not just testing mocks) |
| 15 | **Tests** | Edge cases covered in tests |
| 16 | **Documentation** | Module docs updated if API or schema changed |
| 17 | **Documentation** | Complex logic has inline comments explaining *why* |
| 18 | **Dependencies** | No unnecessary new dependencies added |

---

## 8. Logging Standards Summary

<!-- AGENT INSTRUCTION: Use the structured logger (AppLogger). Never use console.log directly. -->

### Log Levels

| Level | When to Use | Example |
|---|---|---|
| `error` | Unrecoverable errors, failed operations | DB connection failure, unhandled exception |
| `warn` | Recoverable issues, degraded behavior | Cache miss fallback, retry attempt, deprecated API usage |
| `info` | Significant business events | User login, order placed, deployment started |
| `debug` | Detailed technical information | Query parameters, request/response payloads (non-sensitive) |
| `verbose` | Very detailed tracing | Method entry/exit, loop iterations |

### What to Log

- Request ID (correlation ID) in every log entry
- User ID (if authenticated) — never log full tokens
- Operation name and result (success/failure)
- Duration for operations > 100ms
- External service calls (URL, status, duration)

### What NOT to Log

- Passwords, tokens, API keys, or secrets
- Full credit card numbers or PII beyond what's necessary
- Request/response bodies containing sensitive user data
- Stack traces in production (log to error tracking service instead)
- High-frequency events that would cause log flooding (use sampling)
