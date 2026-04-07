# Database Design

<!-- 
  TEMPLATE INSTRUCTIONS (System Designer — VM-2):
  This document defines the database architecture for GateForge, covering PostgreSQL 
  and Redis. Fill in all [PLACEHOLDER] sections based on the data model in 
  architecture/data-model.md and the requirements in requirements/.
  Cross-reference: resilience-design.md for Database HA and failover.
  Cross-reference: monitoring-design.md for database metrics and alerting.
  Cross-reference: RESILIENCE-SECURITY-GUIDE.md for data security patterns.
-->

## Document Metadata

| Field          | Value                                      |
|----------------|--------------------------------------------|
| Document ID    | GF-DES-DB-001                              |
| Version        | [PLACEHOLDER — e.g., 1.0.0]               |
| Owner          | System Designer (VM-2)                     |
| Status         | [PLACEHOLDER — Draft / In Review / Approved] |
| Last Updated   | [PLACEHOLDER — YYYY-MM-DD]                |
| Approved By    | System Architect                           |
| Classification | Confidential                               |

---

## 1. PostgreSQL Configuration

<!-- 
  Document the PostgreSQL server configuration for each environment.
  Tuning parameters should be based on available resources and workload profile.
  Reference: https://pgtune.leopard.in.ua/ for initial tuning.
-->

### 1.1 Server Parameters

| Parameter                  | Dev              | UAT              | Production        | Notes                                    |
|----------------------------|------------------|------------------|-------------------|------------------------------------------|
| PostgreSQL version         | 16               | 16               | 16                | Match across all environments            |
| `max_connections`          | 50               | 100              | 200               | Via PgBouncer, not direct connections    |
| `shared_buffers`           | 256MB            | 1GB              | 4GB               | ~25% of available memory                 |
| `effective_cache_size`     | 768MB            | 3GB              | 12GB              | ~75% of available memory                 |
| `work_mem`                 | 4MB              | 8MB              | 16MB              | Per-operation memory                     |
| `maintenance_work_mem`     | 64MB             | 256MB            | 1GB               | For VACUUM, CREATE INDEX                 |
| `wal_level`                | minimal          | replica          | replica            | Required for streaming replication       |
| `max_wal_senders`          | 0                | 2                | 5                  | Replication slots                        |
| `checkpoint_completion_target` | 0.9          | 0.9              | 0.9                | Spread checkpoint I/O                    |
| `random_page_cost`         | 4.0              | 1.1              | 1.1                | 1.1 for SSD storage                      |
| `log_min_duration_statement` | 0 (log all)   | 500ms            | 1000ms             | Slow query logging threshold             |
| [PLACEHOLDER]              | [PLACEHOLDER]    | [PLACEHOLDER]    | [PLACEHOLDER]     | [PLACEHOLDER]                            |

### 1.2 Connection Pooling (PgBouncer)

| Parameter              | Value              | Notes                                    |
|------------------------|--------------------|------------------------------------------|
| Pool mode              | transaction        | Release connection after transaction     |
| Default pool size      | 20                 | Per database                             |
| Max client connections | 200                | Total client connections accepted        |
| Reserve pool size      | 5                  | Extra connections for burst traffic       |
| Reserve pool timeout   | 3s                 | Wait time before using reserve pool      |
| Server idle timeout    | 600s               | Close idle server connections             |
| Query timeout          | 30s                | Kill queries exceeding this              |
| [PLACEHOLDER]          | [PLACEHOLDER]      | [PLACEHOLDER]                            |

### 1.3 Replication Configuration

<!-- See resilience-design.md Section 6.1 for full HA topology diagram. -->

| Parameter                | Value                    | Notes                                    |
|--------------------------|--------------------------|------------------------------------------|
| Replication type         | Streaming (async)        | [PLACEHOLDER — adjust per durability needs] |
| Number of standbys       | 1                        | [PLACEHOLDER — scale based on read load] |
| Replication slot name    | `standby_slot_1`         | Prevents WAL removal before standby reads|
| Max replication lag (SLO)| < 1 minute               | Alert if exceeded                        |
| [PLACEHOLDER]            | [PLACEHOLDER]            | [PLACEHOLDER]                            |

### 1.4 Vacuum Configuration

| Parameter                      | Value      | Notes                                    |
|--------------------------------|------------|------------------------------------------|
| `autovacuum`                   | on         | Never disable in production              |
| `autovacuum_vacuum_threshold`  | 50         | Min rows before autovacuum triggers      |
| `autovacuum_vacuum_scale_factor` | 0.1      | 10% of table size                        |
| `autovacuum_analyze_threshold` | 50         | Min rows before autoanalyze triggers     |
| `autovacuum_analyze_scale_factor` | 0.05    | 5% of table size                         |
| `autovacuum_max_workers`       | 3          | Parallel autovacuum workers              |
| `autovacuum_naptime`           | 30s        | Time between autovacuum checks           |
| [PLACEHOLDER]                  | [PLACEHOLDER] | [PLACEHOLDER]                         |

## 2. Schema Design per Module

<!-- 
  Map each application module to its database tables. This should align with 
  architecture/data-model.md. Each module's tables should be owned by the module 
  and follow naming conventions: snake_case, plural table names.
-->

| Module           | Tables                                                   | Key Relationships                                             | Owner Service    |
|------------------|----------------------------------------------------------|---------------------------------------------------------------|------------------|
| Authentication   | `users`, `user_credentials`, `refresh_tokens`, `sessions`| `user_credentials.user_id → users.id`; `refresh_tokens.user_id → users.id` | Auth Service |
| Authorization    | `roles`, `permissions`, `role_permissions`, `user_roles`  | `role_permissions.role_id → roles.id`; `user_roles.user_id → users.id`       | Auth Service |
| [PLACEHOLDER — Core Module] | `[table_1]`, `[table_2]`, `[table_3]`       | [PLACEHOLDER — describe foreign key relationships]            | [PLACEHOLDER]    |
| [PLACEHOLDER — Module 2]    | `[table_1]`, `[table_2]`                    | [PLACEHOLDER]                                                 | [PLACEHOLDER]    |
| Audit            | `audit_logs`                                             | `audit_logs.user_id → users.id` (nullable for system events)  | API Gateway      |
| System           | `migrations`, `system_config`                             | None (standalone)                                             | All Services     |

### Naming Conventions

| Element          | Convention                    | Example                        |
|------------------|-------------------------------|--------------------------------|
| Table name       | `snake_case`, plural          | `user_credentials`             |
| Column name      | `snake_case`                  | `created_at`                   |
| Primary key      | `id` (UUID v4)                | `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` |
| Foreign key      | `<referenced_table_singular>_id` | `user_id`                  |
| Index name       | `idx_<table>_<columns>`       | `idx_users_email`              |
| Unique constraint| `uq_<table>_<columns>`        | `uq_users_email`               |
| Check constraint | `ck_<table>_<description>`    | `ck_users_email_format`        |
| Timestamps       | `created_at`, `updated_at`    | Auto-managed by ORM/trigger    |
| Soft delete      | `deleted_at` (nullable)       | `NULL` = active                |

## 3. Migration Strategy

<!-- 
  Define how database migrations are created, reviewed, and applied.
  Migrations must be reversible (up + down). Naming convention is critical 
  for ordering and traceability.
-->

### 3.1 Migration File Convention

- **Naming format**: `YYYYMMDDHHMMSS-description.ts`
  - Example: `20260401120000-create-users-table.ts`
  - Example: `20260401120100-add-email-index-to-users.ts`
- **Location**: `src/database/migrations/`
- **Tool**: [PLACEHOLDER — e.g., TypeORM, Prisma, Knex]
- **Each migration MUST have**:
  - `up()` method — applies the change
  - `down()` method — reverts the change exactly

### 3.2 Migration Workflow

| Step | Action                                    | Environment | Approval Required |
|------|-------------------------------------------|-------------|-------------------|
| 1    | Developer creates migration file          | Local       | No                |
| 2    | Migration runs in CI test database        | CI          | Automatic         |
| 3    | Migration reviewed in PR (SQL reviewed)   | —           | Yes (Architect)   |
| 4    | Migration applied to UAT                  | UAT         | Automatic on merge|
| 5    | Migration applied to Production           | Production  | Manual trigger     |
| 6    | Verify migration success, update this doc | All         | Yes               |

### 3.3 Migration Safety Rules

- **No destructive changes without a migration plan**: Dropping columns/tables requires a 2-phase migration:
  1. Phase 1: Stop using the column in code, deploy
  2. Phase 2: Drop the column in a subsequent migration
- **No locking migrations on large tables**: Use `CREATE INDEX CONCURRENTLY`, `ALTER TABLE ... ADD COLUMN` (with default) to avoid locks
- **Always test down migration**: `npm run migration:revert` must work cleanly
- **Data migrations**: Separate from schema migrations; run as standalone scripts

## 4. Index Design

<!-- 
  Define indexes based on query patterns. Every index must justify its existence 
  with a measured or estimated performance improvement. Review quarterly.
-->

| Table              | Index Name                    | Columns                  | Type       | Estimated Improvement              | Status        |
|--------------------|-------------------------------|--------------------------|------------|-------------------------------------|---------------|
| `users`            | `idx_users_email`             | `email`                  | UNIQUE, B-tree | Login lookup: O(n) → O(log n) | [PLACEHOLDER] |
| `users`            | `idx_users_created_at`        | `created_at`             | B-tree     | User listing sort: 500ms → 10ms    | [PLACEHOLDER] |
| `refresh_tokens`   | `idx_refresh_tokens_hash`     | `token_hash`             | UNIQUE, B-tree | Token validation: O(n) → O(log n) | [PLACEHOLDER] |
| `refresh_tokens`   | `idx_refresh_tokens_user_family` | `user_id`, `family_id`| B-tree     | Family invalidation: 200ms → 5ms   | [PLACEHOLDER] |
| `audit_logs`       | `idx_audit_logs_user_created` | `user_id`, `created_at`  | B-tree     | Audit trail query: 2s → 50ms       | [PLACEHOLDER] |
| `audit_logs`       | `idx_audit_logs_action`       | `action`                 | B-tree     | Action filtering: 1s → 20ms        | [PLACEHOLDER] |
| [PLACEHOLDER]      | [PLACEHOLDER]                 | [PLACEHOLDER]            | [PLACEHOLDER] | [PLACEHOLDER]                   | [PLACEHOLDER] |

<!-- 
  Index review questions:
  - Is this index actually used? (check pg_stat_user_indexes)
  - Is the write overhead justified by read improvement?
  - Can multiple indexes be combined into a composite index?
  - Should we use a partial index for better performance?
-->

## 5. Query Performance Baselines

<!-- 
  Define target execution times for the most critical and frequent queries.
  Measure with EXPLAIN ANALYZE on representative data. Update baselines 
  after schema or data volume changes.
-->

| Query Description                  | Target Execution Time | Current (Measured) | Data Volume Assumption | Optimization Notes                     |
|------------------------------------|-----------------------|--------------------|------------------------|----------------------------------------|
| User login (by email)              | < 5ms                 | [PLACEHOLDER]      | 100K users             | Uses `idx_users_email`                 |
| Refresh token validation           | < 3ms                 | [PLACEHOLDER]      | 500K tokens            | Uses `idx_refresh_tokens_hash`         |
| Audit log query (by user, 30 days) | < 50ms                | [PLACEHOLDER]      | 10M audit rows         | Uses composite index + date filter     |
| List users (paginated, 50 per page)| < 20ms                | [PLACEHOLDER]      | 100K users             | Keyset pagination, not OFFSET          |
| [PLACEHOLDER]                      | [PLACEHOLDER]         | [PLACEHOLDER]      | [PLACEHOLDER]          | [PLACEHOLDER]                          |

### Query Optimization Guidelines

- Use `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` for query plans
- Prefer **keyset pagination** (`WHERE id > :last_id LIMIT 50`) over `OFFSET`
- Avoid `SELECT *` — select only needed columns
- Use CTEs sparingly — they are optimization fences in PostgreSQL < 12 (but materialization hints work in 16)
- Monitor via `pg_stat_statements` extension

## 6. Partitioning Strategy

<!-- 
  Define when and how to partition tables. Not all tables need partitioning.
  Apply only when data volume justifies the complexity.
-->

### When to Partition

| Criterion                    | Threshold                 | Action                                    |
|------------------------------|---------------------------|-------------------------------------------|
| Table row count              | > 10 million rows         | Evaluate range partitioning by date       |
| Query scan time              | > 500ms on indexed query  | Evaluate partitioning to reduce scan scope|
| Data retention requirements  | > 1 year of time-series   | Partition by month, drop old partitions   |
| [PLACEHOLDER]                | [PLACEHOLDER]             | [PLACEHOLDER]                             |

### Partitioning Plan

| Table          | Partition Strategy | Partition Key    | Partition Interval | Retention       | Status        |
|----------------|--------------------|-----------------|--------------------|-----------------|---------------|
| `audit_logs`   | Range (by date)    | `created_at`    | Monthly            | 12 months       | [PLACEHOLDER] |
| [PLACEHOLDER]  | [PLACEHOLDER]      | [PLACEHOLDER]   | [PLACEHOLDER]      | [PLACEHOLDER]   | [PLACEHOLDER] |

<!-- 
  Partitioning notes:
  - Create partitions in advance (at least 3 months ahead)
  - Automate partition creation via pg_partman or CronJob
  - Test that queries use partition pruning (check EXPLAIN output)
-->

## 7. Backup and Recovery

<!-- 
  Define backup strategy, schedule, and recovery procedures.
  Cross-reference: resilience-design.md Section 7 for RPO/RTO targets.
-->

### 7.1 Backup Strategy

| Backup Type        | Tool               | Schedule          | Retention          | Storage Location        |
|--------------------|--------------------|-------------------|--------------------|-------------------------|
| Full base backup   | `pg_basebackup`    | Daily at 02:00 UTC| 7 daily, 4 weekly  | `backup-pvc` + off-site |
| WAL archiving      | `archive_command`  | Continuous        | 7 days             | WAL archive volume      |
| Logical backup     | `pg_dump`          | Weekly (Sunday)   | 4 weekly           | Off-site storage        |
| Redis RDB snapshot | `redis-cli BGSAVE` | Every 6 hours     | 7 days             | `backup-pvc`            |
| Redis AOF          | Continuous         | Always-on         | N/A (rewrite at 100%) | Redis data volume    |
| [PLACEHOLDER]      | [PLACEHOLDER]      | [PLACEHOLDER]     | [PLACEHOLDER]      | [PLACEHOLDER]           |

### 7.2 PITR (Point-in-Time Recovery) Procedure

```
# 1. Stop the PostgreSQL primary
kubectl scale statefulset postgresql --replicas=0 -n gateforge-data

# 2. Restore base backup
pg_basebackup -D /var/lib/postgresql/data -Ft -z -P

# 3. Configure recovery target
cat > /var/lib/postgresql/data/recovery.signal <<EOF
# recovery.signal presence triggers recovery mode
EOF

cat >> /var/lib/postgresql/data/postgresql.conf <<EOF
restore_command = 'cp /wal-archive/%f %p'
recovery_target_time = 'YYYY-MM-DD HH:MM:SS UTC'  # Target point in time
recovery_target_action = 'promote'
EOF

# 4. Start PostgreSQL (enters recovery mode)
kubectl scale statefulset postgresql --replicas=1 -n gateforge-data

# 5. Verify data integrity
psql -c "SELECT count(*) FROM users;"  # Verify expected row counts

# 6. Rebuild standby from recovered primary
# [PLACEHOLDER — standby rebuild steps]
```

<!-- Test PITR procedure quarterly in UAT. Document results in the change log. -->

### 7.3 Backup Verification

| Verification Step             | Frequency  | Method                                          | Owner           |
|-------------------------------|------------|--------------------------------------------------|-----------------|
| Restore test (full backup)    | Monthly    | Restore to test instance, verify data integrity  | System Designer |
| WAL replay test               | Monthly    | PITR to random point, verify consistency         | System Designer |
| Backup file integrity         | Daily      | Checksum verification of backup files            | Automated       |
| Off-site backup accessibility | Weekly     | Download and verify off-site backup              | Automated       |
| [PLACEHOLDER]                 | [PLACEHOLDER] | [PLACEHOLDER]                                | [PLACEHOLDER]   |

## 8. Redis Schema

<!-- 
  Document every Redis key pattern. Redis is used for caching, sessions, and 
  ephemeral data — NOT as a primary data store. Every key must have a TTL.
-->

| Key Pattern                          | Data Type | TTL          | Purpose                                  | Module          |
|--------------------------------------|-----------|--------------|------------------------------------------|-----------------|
| `session:{userId}:{deviceId}`        | Hash      | 7 days       | User session data (refresh token family) | Auth Service    |
| `cache:user:{userId}`               | JSON (String) | 15 min   | Cached user profile                      | API Gateway     |
| `ratelimit:{ip}:{endpoint}`          | String (counter) | 1 min  | Rate limiting counter per IP/endpoint    | API Gateway     |
| `lock:{resource}:{id}`              | String    | 30s          | Distributed lock for critical sections   | Worker          |
| `queue:jobs:{priority}`              | List      | No TTL       | Job queue (processed and removed)        | Worker          |
| `blacklist:token:{jti}`             | String    | 15 min       | Blacklisted JWT tokens (logout)          | Auth Service    |
| `config:feature_flags`              | Hash      | 5 min        | Feature flag cache                       | API Gateway     |
| [PLACEHOLDER]                        | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER]                       | [PLACEHOLDER]   |

### Redis Key Naming Conventions

- **Delimiter**: `:` (colon)
- **Format**: `{category}:{entity}:{identifier}`
- **All keys MUST have a TTL** (except job queues, which are consumed)
- **No binary keys** — use string keys only for debuggability
- **Max key length**: 256 bytes

## 9. Data Integrity Constraints

<!-- 
  Define the database-level constraints that enforce data integrity.
  These are the last line of defense — application-level validation comes first.
-->

### 9.1 Foreign Key Constraints

| Parent Table     | Child Table          | FK Column      | On Delete     | On Update    |
|------------------|----------------------|----------------|---------------|--------------|
| `users`          | `user_credentials`   | `user_id`      | CASCADE       | CASCADE      |
| `users`          | `refresh_tokens`     | `user_id`      | CASCADE       | CASCADE      |
| `users`          | `user_roles`         | `user_id`      | CASCADE       | CASCADE      |
| `roles`          | `user_roles`         | `role_id`      | RESTRICT      | CASCADE      |
| `roles`          | `role_permissions`   | `role_id`      | CASCADE       | CASCADE      |
| `permissions`    | `role_permissions`   | `permission_id`| CASCADE       | CASCADE      |
| [PLACEHOLDER]    | [PLACEHOLDER]        | [PLACEHOLDER]  | [PLACEHOLDER] | [PLACEHOLDER]|

### 9.2 Check Constraints

| Table            | Constraint Name              | Expression                                        | Purpose                          |
|------------------|------------------------------|---------------------------------------------------|----------------------------------|
| `users`          | `ck_users_email_format`      | `email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'` | Valid email format |
| `users`          | `ck_users_status_valid`      | `status IN ('active', 'inactive', 'suspended')`   | Enum enforcement                 |
| `audit_logs`     | `ck_audit_action_valid`      | `action IN ('create', 'read', 'update', 'delete')`| Valid audit actions              |
| [PLACEHOLDER]    | [PLACEHOLDER]                | [PLACEHOLDER]                                     | [PLACEHOLDER]                    |

### 9.3 Unique Constraints

| Table              | Constraint Name               | Columns                      | Notes                            |
|--------------------|-------------------------------|------------------------------|----------------------------------|
| `users`            | `uq_users_email`              | `email`                      | One account per email            |
| `user_roles`       | `uq_user_roles_user_role`     | `user_id`, `role_id`         | No duplicate role assignments    |
| `role_permissions`  | `uq_role_perms_role_perm`    | `role_id`, `permission_id`   | No duplicate permissions         |
| [PLACEHOLDER]      | [PLACEHOLDER]                 | [PLACEHOLDER]                | [PLACEHOLDER]                    |

## 10. Rollback Strategy

<!-- REQUIRED: All design documents must include a rollback strategy. -->

| Change Type              | Rollback Method                                      | Verification                              | RTO       |
|--------------------------|------------------------------------------------------|-------------------------------------------|-----------|
| Schema migration (DDL)   | Run `down()` migration                               | Verify schema matches previous version    | < 10 min  |
| Data migration (DML)     | Run compensating data script (must be pre-written)   | Row count and data spot-check             | < 30 min  |
| Index creation           | `DROP INDEX` (concurrent if needed)                  | Verify query plans unchanged              | < 5 min   |
| Configuration change     | Revert `postgresql.conf` + `pg_reload_conf()`        | Verify `pg_settings` reflects old values  | < 2 min   |
| Redis schema change      | Deploy previous app version (key handling)           | Verify cache hit rates normal             | < 5 min   |
| Partition change         | Reattach/detach partition as needed                   | Verify queries use correct partitions     | < 15 min  |
| [PLACEHOLDER]            | [PLACEHOLDER]                                        | [PLACEHOLDER]                             | [PLACEHOLDER] |

## 11. Security Assessment

<!-- REQUIRED: All design documents must include a security assessment section. -->

| Area                       | Risk Level | Controls                                              | Status        |
|----------------------------|------------|-------------------------------------------------------|---------------|
| SQL injection              | Critical   | Parameterized queries via ORM, no raw SQL in app code  | [PLACEHOLDER] |
| Connection security        | High       | TLS for all DB connections, network policies           | [PLACEHOLDER] |
| Credential storage         | Critical   | Sealed Secrets, rotated every 90 days                  | [PLACEHOLDER] |
| Backup encryption          | High       | Encrypted at rest, encrypted in transit                | [PLACEHOLDER] |
| Access control             | High       | Separate DB users per service, least privilege         | [PLACEHOLDER] |
| Audit trail                | Medium     | All mutations logged in `audit_logs` table              | [PLACEHOLDER] |
| [PLACEHOLDER]              | [PLACEHOLDER] | [PLACEHOLDER]                                      | [PLACEHOLDER] |

<!-- Cross-reference: See security-design.md for STRIDE analysis of database components. -->

## 12. Database Change Log

<!-- 
  Log every database change. Add a row BEFORE applying any change.
  This is the audit trail for schema evolution.
-->

| Date       | Migration ID               | Description                              | Impact                            | Rollback                                |
|------------|----------------------------|------------------------------------------|-----------------------------------|-----------------------------------------|
| YYYY-MM-DD | 20260401120000             | [Example] Create users table              | New table, no data impact         | Down migration drops table              |
| YYYY-MM-DD | 20260401120100             | [Example] Add email index                 | Brief lock on users table (< 1s) | `DROP INDEX idx_users_email`            |
| YYYY-MM-DD | 20260402090000             | [Example] Add audit_logs partitioning     | Requires table rewrite (planned downtime) | Revert to non-partitioned table |
| [PLACEHOLDER] | [PLACEHOLDER]          | [PLACEHOLDER]                             | [PLACEHOLDER]                     | [PLACEHOLDER]                           |

---

<!-- 
  REVIEW CHECKLIST (System Architect):
  [ ] PostgreSQL configuration tuned for target hardware
  [ ] Connection pooling configured (PgBouncer)
  [ ] Schema design follows naming conventions
  [ ] Migration strategy includes up/down and safety rules
  [ ] Indexes justified with performance data
  [ ] Query performance baselines established
  [ ] Partitioning strategy defined (or explicitly deferred)
  [ ] Backup and PITR procedures tested
  [ ] Redis schema documented with TTLs for all keys
  [ ] Data integrity constraints defined at database level
  [ ] Rollback strategy documented for all change types
  [ ] Security assessment completed
  [ ] Change log initialized
  Cross-reference: resilience-design.md for HA topology
  Cross-reference: RESILIENCE-SECURITY-GUIDE.md for data security
-->
