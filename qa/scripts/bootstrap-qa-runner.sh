#!/usr/bin/env bash
# GateForge — Bootstrap a headless Ubuntu QC runner
# Reference: UI Auto-Test Standard § 9.2
#
# Idempotent. Re-run safe. Targets Ubuntu Server 22.04+ LTS with NO desktop.
# Run as root or via sudo. Network access required for apt + Docker pulls.

set -euo pipefail

log()  { echo -e "\033[1;34m[bootstrap]\033[0m $*"; }
warn() { echo -e "\033[1;33m[bootstrap]\033[0m $*" >&2; }
fail() { echo -e "\033[1;31m[bootstrap]\033[0m $*" >&2; exit 1; }

# ---------------------------------------------------------------------------
# 0. Preconditions
# ---------------------------------------------------------------------------
[[ "$(id -u)" -eq 0 ]] || fail "Run as root (sudo). The QC runner setup needs apt + systemd access."

. /etc/os-release || fail "Cannot detect OS — /etc/os-release missing."
[[ "${ID}" == "ubuntu" ]] || warn "Designed for Ubuntu; detected ${ID}. Proceeding anyway."
ver_major="${VERSION_ID%%.*}"
[[ "${ver_major}" -ge 22 ]] || fail "Ubuntu 22.04+ required, got ${VERSION_ID}."

# ---------------------------------------------------------------------------
# 1. APT packages
# ---------------------------------------------------------------------------
log "==> Updating apt and installing base packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y --no-install-recommends \
  ca-certificates curl gnupg git jq unzip xz-utils \
  build-essential pkg-config \
  fonts-liberation fonts-noto-color-emoji fonts-noto-cjk \
  libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
  libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 \
  libgbm1 libpango-1.0-0 libasound2 libdrm2 \
  xvfb x11-utils dbus-x11 \
  python3-pip

# ---------------------------------------------------------------------------
# 2. Docker Engine + Compose plugin
# ---------------------------------------------------------------------------
if ! command -v docker >/dev/null; then
  log "==> Installing Docker Engine"
  install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  chmod a+r /etc/apt/keyrings/docker.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/ubuntu ${VERSION_CODENAME} stable" \
    > /etc/apt/sources.list.d/docker.list
  apt-get update -y
  apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  systemctl enable --now docker
fi

# ---------------------------------------------------------------------------
# 3. Node.js 20 LTS + pnpm
# ---------------------------------------------------------------------------
if ! command -v node >/dev/null || [[ "$(node -v | sed 's/v//;s/\..*//')" -lt 20 ]]; then
  log "==> Installing Node.js 20 LTS"
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
  apt-get install -y nodejs
fi
command -v pnpm >/dev/null || { log "==> Enabling pnpm via corepack"; corepack enable && corepack prepare pnpm@latest --activate; }

# ---------------------------------------------------------------------------
# 4. Playwright browsers + system deps
# ---------------------------------------------------------------------------
log "==> Installing Playwright browsers"
npx --yes playwright install --with-deps chromium

# ---------------------------------------------------------------------------
# 5. axe-core + Lighthouse CLI
# ---------------------------------------------------------------------------
log "==> Installing axe-core and Lighthouse CLI"
npm install -g @axe-core/cli@latest lighthouse@latest

# ---------------------------------------------------------------------------
# 6. OpenClaw runner (placeholder — replace with org install path)
# ---------------------------------------------------------------------------
if ! command -v openclaw >/dev/null; then
  warn "OpenClaw CLI not found. Install it from your internal release artefact and re-run."
fi

# ---------------------------------------------------------------------------
# 7. Tailscale check (multi-agent variant)
# ---------------------------------------------------------------------------
log "==> Tailscale check"
if ! command -v tailscale >/dev/null; then
  warn "Tailscale not installed; multi-agent QC runners must join the tailnet."
fi

# ---------------------------------------------------------------------------
# 8. Workspace dirs
# ---------------------------------------------------------------------------
log "==> Provisioning OpenClaw workspace dirs"
install -d -m 0750 /var/lib/openclaw/profiles
install -d -m 0750 /var/lib/openclaw/secrets
install -d -m 0750 /var/lib/openclaw/cache

# ---------------------------------------------------------------------------
# 9. Bring up Lane B Docker stack (idempotent)
# ---------------------------------------------------------------------------
COMPOSE_FILE="$(dirname "$(realpath "$0")")/../docker-compose.qa.yml"
if [[ -f "${COMPOSE_FILE}" ]]; then
  log "==> Bringing up Lane B headful stack"
  docker compose -f "${COMPOSE_FILE}" up -d
else
  warn "docker-compose.qa.yml not found at ${COMPOSE_FILE}; skipping Lane B start."
fi

# ---------------------------------------------------------------------------
# 10. Sanity probes
# ---------------------------------------------------------------------------
log "==> Probing CDP endpoint (Lane B)"
sleep 3
curl -fsS http://127.0.0.1:9222/json/version >/dev/null \
  && log "CDP OK" \
  || warn "CDP not reachable yet — give the container 30 s and re-probe."

log "==> Bootstrap complete."
log "    Next: edit qa/openclaw.qa.yaml, qa/playwright.config.ts, populate qa/intents.md."
log "    Then run: cd qa && pnpm playwright test --project=smoke"
