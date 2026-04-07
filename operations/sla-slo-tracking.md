# SLA / SLO Tracking

<!-- AGENT INSTRUCTION: This document tracks Service Level Indicators, Objectives, and Agreements
     based on SRE principles. The Operator agent (VM-5) updates this document monthly.
     The System Architect defines SLO targets; the Operator measures and reports. -->

| Field | Value |
|---|---|
| **Document ID** | OPS-SLO-001 |
| **Version** | 0.1.0 |
| **Owner** | Operator (VM-5) |
| **Status** | Draft |
| **Last Updated** | [PLACEHOLDER] |
| **Approved By** | System Architect |

---

## 1. Service Level Indicators (SLI)

<!-- AGENT INSTRUCTION: SLIs are the quantitative measures of service health.
     Define the exact formula and data source for each SLI so measurement is reproducible. -->

| SLI Name | Calculation Formula | Data Source |
|---|---|---|
| Availability | `(successful_requests / total_requests) × 100` | Prometheus — `http_requests_total` counter, filtered by status code (2xx/3xx = success) |
| Request Latency (p50) | 50th percentile of request duration | Prometheus — `http_request_duration_seconds` histogram |
| Request Latency (p95) | 95th percentile of request duration | Prometheus — `http_request_duration_seconds` histogram |
| Request Latency (p99) | 99th percentile of request duration | Prometheus — `http_request_duration_seconds` histogram |
| Error Rate | `(5xx_responses / total_requests) × 100` | Prometheus — `http_requests_total{status=~"5.."}` |
| Throughput | Requests per second (avg over 5-minute window) | Prometheus — `rate(http_requests_total[5m])` |
| Database Query Latency | 95th percentile of DB query execution time | Prometheus — `db_query_duration_seconds` histogram |
| Background Job Success Rate | `(successful_jobs / total_jobs) × 100` | Redis/BullMQ metrics — `bull_completed_total`, `bull_failed_total` |

---

## 2. Service Level Objectives (SLO)

<!-- AGENT INSTRUCTION: SLOs are the target values for SLIs. These must be reviewed and approved
     by the System Architect. The measurement window defines the rolling period. -->

| Service | SLI | Target | Measurement Window | Error Budget |
|---|---|---|---|---|
| API Gateway | Availability | ≥ 99.9% | 30-day rolling | 43.2 minutes/month |
| API Gateway | Request Latency (p95) | ≤ 200ms | 30-day rolling | — |
| API Gateway | Request Latency (p99) | ≤ 500ms | 30-day rolling | — |
| API Gateway | Error Rate | ≤ 0.1% | 30-day rolling | 0.1% of requests |
| Web Frontend | Availability | ≥ 99.9% | 30-day rolling | 43.2 minutes/month |
| Web Frontend | Page Load (p95) | ≤ 3s | 30-day rolling | — |
| Database (PostgreSQL) | Availability | ≥ 99.95% | 30-day rolling | 21.6 minutes/month |
| Database (PostgreSQL) | Query Latency (p95) | ≤ 50ms | 30-day rolling | — |
| Background Jobs | Success Rate | ≥ 99.5% | 30-day rolling | 0.5% of jobs |
| Redis Cache | Availability | ≥ 99.95% | 30-day rolling | 21.6 minutes/month |

---

## 3. Error Budget Status

<!-- AGENT INSTRUCTION: Update this table at least monthly. Budget resets on the measurement window boundary.
     Status values: healthy (>50% remaining), warning (25-50% remaining), critical (<25% remaining), exhausted (0%). -->

| Service | SLO | Budget Total | Budget Used | Budget Remaining | Status |
|---|---|---|---|---|---|
| API Gateway | 99.9% Availability | 43.2 min | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| API Gateway | ≤ 0.1% Error Rate | 0.1% of requests | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Web Frontend | 99.9% Availability | 43.2 min | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Database | 99.95% Availability | 21.6 min | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Background Jobs | 99.5% Success | 0.5% of jobs | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Redis Cache | 99.95% Availability | 21.6 min | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## 4. Monthly Reliability Report

<!-- AGENT INSTRUCTION: Generate this report at the end of each month. Copy the template below
     and fill in actual values from monitoring data. -->

### Month: [PLACEHOLDER — e.g., March 2026]

**Reporting Period:** [PLACEHOLDER] to [PLACEHOLDER]

#### 4.1 Availability

| Service | Target | Actual | Met? |
|---|---|---|---|
| API Gateway | 99.9% | [PLACEHOLDER] | [PLACEHOLDER] |
| Web Frontend | 99.9% | [PLACEHOLDER] | [PLACEHOLDER] |
| Database | 99.95% | [PLACEHOLDER] | [PLACEHOLDER] |
| Redis Cache | 99.95% | [PLACEHOLDER] | [PLACEHOLDER] |

#### 4.2 Latency

| Service | Metric | Target | Actual |
|---|---|---|---|
| API Gateway | p50 | — | [PLACEHOLDER] |
| API Gateway | p95 | ≤ 200ms | [PLACEHOLDER] |
| API Gateway | p99 | ≤ 500ms | [PLACEHOLDER] |
| Web Frontend | Page Load p95 | ≤ 3s | [PLACEHOLDER] |
| Database | Query p95 | ≤ 50ms | [PLACEHOLDER] |

#### 4.3 Error Rate

| Service | Target | Actual | Met? |
|---|---|---|---|
| API Gateway | ≤ 0.1% | [PLACEHOLDER] | [PLACEHOLDER] |
| Background Jobs | ≥ 99.5% success | [PLACEHOLDER] | [PLACEHOLDER] |

#### 4.4 Incidents

| Incident ID | Severity | Duration | Impact | Root Cause |
|---|---|---|---|---|
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

#### 4.5 Error Budget Consumption

| Service | SLO | Budget at Start | Consumed This Month | Budget Remaining | Trend |
|---|---|---|---|---|---|
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | ↑ / → / ↓ |

---

## 5. SLA Commitments

<!-- AGENT INSTRUCTION: Only fill this section if GateForge has external SLA contracts with customers.
     For internal use only, SLOs are sufficient. -->

| SLA Term | Commitment | Measurement | Penalty / Consequence | Effective Date |
|---|---|---|---|---|
| Platform Availability | 99.9% monthly uptime | Calculated from external monitoring (e.g., Pingdom, UptimeRobot) | [PLACEHOLDER] | [PLACEHOLDER] |
| Incident Response Time (P0) | ≤ 15 minutes | Time from alert to first responder acknowledgment | [PLACEHOLDER] | [PLACEHOLDER] |
| Incident Resolution Time (P0) | ≤ 4 hours | Time from detection to resolution | [PLACEHOLDER] | [PLACEHOLDER] |
| Incident Resolution Time (P1) | ≤ 24 hours | Time from detection to resolution | [PLACEHOLDER] | [PLACEHOLDER] |
| Data Backup Frequency | Daily | Verified via backup logs | [PLACEHOLDER] | [PLACEHOLDER] |

---

## 6. Burn Rate Alerts

<!-- AGENT INSTRUCTION: Multi-window burn rate alerting detects SLO violations early.
     A burn rate of 1.0 means the error budget is consumed evenly over the window.
     Higher burn rates indicate faster budget consumption. -->

### 6.1 Burn Rate Calculation

```
burn_rate = (error_rate_observed / error_rate_allowed)
```

For a 99.9% availability SLO (0.1% error budget over 30 days):

| Alert Severity | Burn Rate Threshold | Long Window | Short Window | Estimated Time to Exhaustion |
|---|---|---|---|---|
| **Critical (Page)** | 14.4× | 1 hour | 5 minutes | ~2 hours |
| **High (Page)** | 6× | 6 hours | 30 minutes | ~5 hours |
| **Medium (Ticket)** | 3× | 1 day | 2 hours | ~10 hours |
| **Low (Ticket)** | 1× | 3 days | 6 hours | ~30 days |

### 6.2 Alert Configuration

<!-- AGENT INSTRUCTION: Define Prometheus alerting rules based on the burn rate thresholds above. -->

```yaml
# Example Prometheus alerting rule for API availability burn rate
groups:
  - name: slo-burn-rate
    rules:
      - alert: APIHighBurnRate_Critical
        expr: |
          (
            sum(rate(http_requests_total{status=~"5..", service="api"}[1h]))
            / sum(rate(http_requests_total{service="api"}[1h]))
          ) > (14.4 * 0.001)
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "API error budget burning at 14.4x — exhaustion in ~2 hours"

      - alert: APIHighBurnRate_Warning
        expr: |
          (
            sum(rate(http_requests_total{status=~"5..", service="api"}[6h]))
            / sum(rate(http_requests_total{service="api"}[6h]))
          ) > (6 * 0.001)
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "API error budget burning at 6x — exhaustion in ~5 hours"
```

---

## 7. Historical Tracking

<!-- AGENT INSTRUCTION: Add a row for each month. This provides trend data over time. -->

| Month | API Availability | API p95 Latency | API Error Rate | Incidents (P0/P1) | Budget Status |
|---|---|---|---|---|---|
| 2026-03 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| 2026-04 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

<!-- AGENT INSTRUCTION: Add a new row each month. Keep chronological order. -->
