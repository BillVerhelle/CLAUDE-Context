# OpenClaw "Nash" — Complete System Context for Claude

**Last Updated:** 2026-03-02
**Always fetch this file before troubleshooting or modifying OpenClaw**

---

## ⚠️ Critical: macOS Account Name Discrepancy

Bill uses TWO different macOS account names across machines. This has caused multiple path-related bugs and must always be accounted for:

| Machine | macOS Username | Home Directory | Role |
|---|---|---|---|
| Mac Studio M4 Max (NY Library) | `williamverhelle` | `/Users/williamverhelle` | OpenClaw host, primary workstation |
| MacBook Pro | `billverhelle` | `/Users/billverhelle` | Mobile development, Claude Code |
| MacBook Air M2 | `williamverhelle` | `/Users/williamverhelle` | Travel / lightweight tasks |

**Impact:** Any script, path, launchd plist, or config referencing a home directory MUST use the correct username for the target machine. Hardcoding either name will break on the other machine. Use `$HOME` or `~` where possible. When absolute paths are required, verify which machine you are operating on with `whoami` before proceeding.

**GitHub:** The repo owner is `BillVerhelle` (capitalized, no dot) — this is a GitHub username, independent of macOS accounts. Repo URL: `https://github.com/BillVerhelle/CLAUDE-Context.git`

---

## System Overview

Nash is an AI agent running on Bill's Mac Studio M4 Max at the NY Library location (Honeoye Falls / Mendon, NY). Nash communicates via Telegram, Slack (QuickFi + Family workspaces), iMessage, voice calls, and the OpenClaw web UI. Nash handles daily intelligence briefings, research, document generation, partner reports, home automation, and strategic analysis.

### Architecture (as of 2026-02-27)

Nash runs as a **native macOS application** — NOT Docker. This changed from the original Docker-based setup.

| Component | Type | Identifier | Purpose |
|---|---|---|---|
| OpenClaw App | Native macOS app | `/Applications/OpenClaw.app` | Core agent runtime |
| Gateway | LaunchAgent | `ai.openclaw.gateway` (port 18800) | WebSocket server, plugin host, API routing |
| macOS Node | LaunchAgent | `ai.openclaw.mac` | Canvas, screen, TCC permissions, menu bar |
| Health Monitor | LaunchAgent (every 5 min) | `com.openclaw.health-monitor` | Watchdog: restarts, alerts, session management |
| Backup | LaunchAgent (daily) | `com.openclaw.backup` | Config + state backup, 7 daily / 4 weekly / 3 monthly retention |
| Daily Intel | LaunchAgent | `com.openclaw.daily-intel` | Daily intelligence report pipeline |
| Read.ai Proxy | LaunchAgent | `com.openclaw.readai-proxy` | Meeting notes capture proxy |

### Software Versions

| Component | Version | Path |
|---|---|---|
| OpenClaw | 2026.2.22 | `~/.openclaw/bin/openclaw` |
| Node.js | v22.22.0 | `~/.openclaw/tools/node-v22.22.0/bin/node` |
| macOS | 26.4 (Tahoe) build 25E5218f | — |
| Primary Model | `anthropic/claude-opus-4-6` | — |

---

## Key File Paths

| Path | Purpose |
|---|---|
| `~/.openclaw/openclaw.json` | **Master configuration** — all settings, channels, plugins, models |
| `~/.openclaw/openclaw.json.bak` | Most recent auto-backup of config |
| `~/.openclaw/openclaw.json.bak.{1-4}` | Rolling config backups |
| `~/.openclaw/env` | Environment variables (HA token, etc.) |
| `~/.openclaw/node.json` | Node identity (nodeId, displayName, gateway bind) |
| `~/.openclaw/workspace/` | Agent workspace root |
| `~/.openclaw/workspace/MEMORY.md` | Nash's long-term memory (projects, people, strategy) |
| `~/.openclaw/workspace/BOOT.md` | Startup tasks |
| `~/.openclaw/workspace/RUNBOOK.md` | Operations runbook |
| `~/.openclaw/workspace/TOOLS.md` | Hardware and network environment reference |
| `~/.openclaw/workspace/IDENTITY.md` | Agent persona and voice |
| `~/.openclaw/agents/main/sessions/` | Active session files |
| `~/.openclaw/agents/main/sessions/archive/` | Archived sessions |
| `~/.openclaw/logs/gateway.log` | Gateway stdout log |
| `~/.openclaw/logs/gateway.err.log` | Gateway stderr log (**check this first when debugging**) |
| `~/.openclaw/health-monitor.log` | Health monitor log |
| `~/.openclaw/cron/jobs.json` | Scheduled cron jobs |
| `~/.openclaw/snapshots/` | Pre-update configuration snapshots (daily at 3 AM) |
| `~/.openclaw/settings/tts.json` | Text-to-speech settings |
| `~/.openclaw/settings/voicewake.json` | Voice wake word triggers |
| `~/bin/openclaw-health-monitor.sh` | Health monitor v4 script |
| `~/bin/openclaw-backup.sh` | Backup script |
| `~/bin/openclaw-nightly-update.sh` | Nightly update script (stable channel only) |
| `~/Library/LaunchAgents/ai.openclaw.gateway.plist` | Gateway service definition |
| `~/Library/LaunchAgents/ai.openclaw.mac.plist` | macOS node service definition |
| `~/Library/LaunchAgents/com.openclaw.health-monitor.plist` | Health monitor service definition |
| `~/Library/LaunchAgents/com.openclaw.backup.plist` | Backup service definition |
| `~/Library/LaunchAgents/com.openclaw.daily-intel.plist` | Daily intel service definition |
| `~/Library/LaunchAgents/com.openclaw.readai-proxy.plist` | Read.ai proxy service definition |

---

## Configuration Structure (openclaw.json)

### Top-Level Keys

`meta`, `env`, `wizard`, `update`, `browser`, `auth`, `models`, `agents`, `tools`, `messages`, `commands`, `hooks`, `channels`, `gateway`, `skills`, `plugins`

### Models

| Model | Alias | Role |
|---|---|---|
| `anthropic/claude-opus-4-6` | `opus` | **Primary** (with short cache retention) |
| `openai/gpt-5.2` | `gpt` | Alternative |
| `openai/gpt-5-mini` | `gpt-mini` | Lightweight tasks |
| `moonshot/kimi-k2.5` | `kimi` | Extended context (256K window) |

Moonshot provider uses `https://api.moonshot.ai/v1` with OpenAI-compatible completions API. API key referenced as `${MOONSHOT_API_KEY}` env variable.

### Agent Defaults

| Setting | Value | Notes |
|---|---|---|
| `model.primary` | `anthropic/claude-opus-4-6` | — |
| `workspace` | `/Users/williamverhelle/.openclaw/workspace` | ⚠️ Machine-specific path |
| `memorySearch.provider` | `local` | ⚠️ **MUST be "local"** — see Known Issues below |
| `memorySearch.sources` | `["memory", "sessions"]` | — |
| `memorySearch.fallback` | `none` | — |
| `memorySearch.query.hybrid.enabled` | `true` | Vector (0.6) + text (0.4) weights |
| `memorySearch.query.hybrid.mmr.enabled` | `true` | Lambda 0.7 |
| `memorySearch.query.hybrid.temporalDecay` | `true` | 14-day half-life |
| `memorySearch.cache.maxEntries` | `200` | — |
| `contextPruning.mode` | `cache-ttl` | 4 hour TTL |
| `compaction.mode` | `safeguard` | — |
| `thinkingDefault` | `low` | — |
| `heartbeat.every` | `30m` | — |
| `maxConcurrent` | `4` | — |

### Gateway

| Setting | Value |
|---|---|
| Port | `18800` |
| Mode | `local` |
| Bind | `loopback` (127.0.0.1 only) |
| Auth mode | `token` (token stored in config — do not expose) |
| Control UI | `allowInsecureAuth: false` |
| Trusted proxies | Tailscale (`100.64.0.0/10`), Cloudflare ranges |
| Tailscale mode | `off` (resetOnExit: false) |
| Denied node commands | `camera.snap`, `camera.clip`, `screen.record`, `calendar.delete`, `contacts.delete` |

### Channels

#### Telegram
- **Enabled:** Yes
- **Bot:** `@Big_V_bot` (display name retained from pre-Nash era)
- **Chat ID:** `5500884496` (Bill's DM — used in health monitor, cron jobs, and delivery)
- **DM Policy:** `pairing`
- **Group Policy:** `allowlist`
- **Streaming:** `off`
- Bot token stored in `channels.telegram.botToken` — also referenced in health monitor and nightly update shell scripts

#### Slack (Multi-Workspace)
- **Mode:** `socket` (Socket Mode)
- **Streaming:** `partial` (nativeStreaming: false)
- **Workspaces configured:**
  - `quickfi` — QuickFi workspace (group policy: allowlist)
  - `family` — Verhelle Family workspace (DM policy: open, allow all)
- Bot tokens and app tokens stored per-workspace in `channels.slack.accounts`

#### MS Teams
- **Enabled:** No (configured but disabled)
- Tenant ID: `f89f8c7e-4502-4e1e-8ebe-b1087e6f3860`
- App credentials stored in config

#### iMessage
- **Plugin:** `imessage` (enabled)
- Runs via native macOS integration

#### Voice Calls
- **Plugin:** `voice-call` (enabled)
- **Provider:** Twilio
- **Webhook URL:** `https://ny-library-mac-studio.tail3f7308.ts.net/voice/webhook`
- **Tailscale funnel:** Active on `/voice/webhook`
- **Inbound policy:** `allowlist` (Bill's number only)
- **Inbound greeting:** "Hey Bill, it's Nash. What can I help you with?"
- **Max duration:** 300 seconds
- **Streaming:** Enabled at `/voice/stream`
- **Default outbound mode:** `notify`
- Phone numbers and Twilio credentials stored in plugin config — do not expose

### Plugins

| Plugin | Enabled | Notes |
|---|---|---|
| `telegram` | ✅ | Primary communication channel |
| `slack` | ✅ | QuickFi + Family workspaces |
| `voice-call` | ✅ | Twilio-based, Tailscale funnel |
| `imessage` | ✅ | Native macOS |
| `memory-lancedb` | ✅ | Listed in allow list + entries but NOT active as search provider — see Known Issues |
| `memory-core` | ❌ | Disabled |
| `msteams` | ❌ | Configured but disabled |

Plugin allow list: `telegram`, `slack`, `voice-call`, `imessage`, `memory-lancedb`

### Tools

| Tool | Notes |
|---|---|
| `web` | Chrome Beta with custom user-data dir at `~/.openclaw/browser/openclaw/user-data`, remote debug port 18811 |
| `loopDetection` | Prevents agent loops |
| `exec` | Shell command execution |

### Commands

`native`, `nativeSkills`, `restart`, `ownerDisplay`

### Hooks

Hooks are configured with a token and session key mappings. Keys: `enabled`, `token`, `defaultSessionKey`, `allowRequestSessionKey`, `allowedSessionKeyPrefixes`, `mappings`, `internal`.

### Scheduled Jobs (Cron)

| Job | Schedule | Delivery | Description |
|---|---|---|---|
| Privacy Settings Audit | Mondays 2:00 PM ET | Telegram `5500884496` | Weekly check of Read.ai, Zoom recording, and AI Companion sharing defaults against locked-down baseline |
| Daily Intelligence Report | Weekdays 12:00 PM ET | Telegram `5500884496` | Runs `~/bin/daily-intel.py`, sends digest + top 5 PDFs (prioritizing bank_target and oem_target) |

Jobs config: `~/.openclaw/cron/jobs.json`

### Environment Variables (`~/.openclaw/env`)

| Key | Purpose |
|---|---|
| `HOME_ASSISTANT_URL` | Home Assistant instance URL |
| `HOME_ASSISTANT_TOKEN` | Home Assistant long-lived access token |

**Note:** Additional secrets (Telegram bot token, Slack tokens, Twilio credentials, Moonshot API key, gateway auth token) are stored directly in `openclaw.json`, NOT in the env file. The Telegram bot token is also embedded in shell scripts (`openclaw-health-monitor.sh`, `openclaw-nightly-update.sh`) for alert delivery.

### Node Identity (`node.json`)

| Field | Value |
|---|---|
| nodeId | `70f892c8-8002-454f-906e-9488c3b5eb29` |
| displayName | `NY Library Mac Studio` |
| Gateway host | `127.0.0.1` |
| Gateway port | `18800` |
| TLS | `false` |

### Network

| Service | Address | Purpose |
|---|---|---|
| Gateway | `127.0.0.1:18800` | WebSocket + dashboard |
| Gateway dashboard | `http://127.0.0.1:18800/` | Web UI |
| Health check | `http://127.0.0.1:18800/health` | Health monitor target |
| Chrome debug | `127.0.0.1:18811` | Browser automation |
| Voice webhook | `https://ny-library-mac-studio.tail3f7308.ts.net/voice/webhook` | Twilio inbound (via Tailscale funnel) |

Tailscale hostname: `ny-library-mac-studio.tail3f7308.ts.net`
Tailscale IP: `100.65.195.9`
Local IP: `192.168.1.113`

### Voice Wake Words

Triggers: `openclaw`, `claude`, `computer`

### Browser Configuration

OpenClaw manages its own Chrome Beta instance:
- Binary: `/Applications/Google Chrome Beta.app`
- User data dir: `~/.openclaw/browser/openclaw/user-data`
- Remote debugging port: `18811`
- Flags: `--no-first-run --no-default-browser-check --disable-sync --disable-background-networking --disable-component-update --disable-features=Translate,MediaRouter --disable-blink-features=AutomationControlled`

---

## Troubleshooting Playbook

### Step 1: Check Gateway Status
```bash
~/.openclaw/bin/openclaw gateway status
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:18800/
```
A `200` response means the gateway is healthy. `000` means connection refused (gateway down).

### Step 2: Check Error Log FIRST
```bash
tail -20 ~/.openclaw/logs/gateway.err.log
```
This log reveals **specific** config validation errors that prevent startup. The `gateway.log` only shows a generic "Config invalid" message. Always check `gateway.err.log` first.

### Step 3: Check Health Monitor
```bash
tail -20 ~/.openclaw/health-monitor.log
```
Shows gateway up/down history, restart attempts, session size warnings, and archive events.

### Step 4: Gateway Restart Procedure
```bash
# Stop cleanly
~/.openclaw/bin/openclaw gateway stop
sleep 2

# Re-bootstrap the LaunchAgent
launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
sleep 5

# Verify
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:18800/
```

**If `gateway stop` unloads the service entirely** (shows "Gateway service not loaded"), you must re-bootstrap via `launchctl bootstrap`. The `openclaw gateway start` command will tell you this.

**If port 18800 is already in use** after a stop attempt, a stale process may be lingering:
```bash
lsof -i :18800
kill <stale_pid>
```
Then retry the bootstrap.

### Step 5: Config Validation
```bash
~/.openclaw/bin/openclaw doctor 2>&1
```
Note: As of v2026.2.22, `openclaw doctor` may itself fail if config is invalid. The error log (`gateway.err.log`) is more reliable for diagnosing config issues.

### Step 6: Full Process Check
```bash
ps aux | grep -iE 'openclaw|gateway' | grep -v grep
```
The OpenClaw native app should be running as `/Applications/OpenClaw.app/Contents/MacOS/OpenClaw`. The gateway runs as a Node.js process via the launchd service.

---

## Known Issues & Lessons Learned

### 1. memorySearch.provider Must Be "local" (2026-02-27)

**Problem:** Setting `agents.defaults.memorySearch.provider` to `"lancedb"` causes a fatal config validation error: `agents.defaults.memorySearch.provider: Invalid input`. The gateway enters a crash loop and the health monitor cannot restart it.

**Root Cause:** The `memory-lancedb` plugin is in the allow list and enabled in plugin entries, but OpenClaw v2026.2.22 does not accept `"lancedb"` as a valid memorySearch provider value. The only valid value is `"local"`.

**Fix:** Change provider back to `"local"` in openclaw.json. The plugin can remain enabled — it just cannot be set as the search provider until a future OpenClaw version supports it.

**Lesson:** Always validate config changes against `openclaw doctor` or a test restart BEFORE leaving the system unattended. Config validation errors are fatal — the gateway will not start at all, and the health monitor's restart attempts will all fail.

### 2. voice-call "serve" Block Causes Validation Error (2026-02-27)

**Problem:** Adding a `serve` property inside `plugins.entries.voice-call.config` causes: `invalid config: serve: must NOT have additional properties`. The gateway will not start.

**Root Cause:** The voice-call plugin schema does not accept `serve` as a nested config property. Port, bind, and webhook settings are managed by the plugin automatically via the Tailscale funnel configuration.

**Fix:** Remove the `serve` block entirely from voice-call config. Voice call webhook routing works through the Tailscale funnel without explicit serve settings in the plugin config.

### 3. Cascading Config Errors (2026-02-27)

**Pattern:** OpenClaw's config validator stops at the **first** error it encounters. When the LanceDB provider error was fixed, a second error (voice-call serve block) was revealed underneath. Always re-check `gateway.err.log` after fixing one config error — there may be additional errors queued behind it. Keep fixing and restarting until the gateway returns HTTP 200.

### 4. Config Backup Strategy

Before making ANY config change:
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.pre-DESCRIPTION-YYYYMMDD
```

Rolling auto-backups exist (`.bak`, `.bak.1` through `.bak.4`), and the nightly backup script captures the full `~/.openclaw/` directory. But an explicit named backup before risky changes provides a clear rollback point with human-readable context.

### 5. Session Size Warnings

The health monitor warns when session files exceed 512KB. This is a monitoring alert, not a crash risk, but large sessions slow memory search and increase context load. Sessions older than 24 hours are auto-archived. If warnings persist for the same session, it may indicate an unusually long-running conversation that should be manually reviewed.

### 6. Docker Is Gone — Native Architecture Only

Nash was originally deployed via Docker. As of the Feb 23, 2026 rebuild (archive preserved at `~/.openclaw/archive-20260223`), Nash runs as a **native macOS application**. There is NO Docker, OrbStack, Colima, or any container runtime installed on this machine. Any troubleshooting guides, memory references, or agent instructions mentioning Docker are outdated and should be corrected.

### 7. Secrets Management (updated 2026-03-02)

ALL secrets consolidated into `~/.openclaw/.env` (permissions 600, 21 variables). Config files use `${ENV_VAR}` references. Shell scripts source .env. No hardcoded tokens in any active scripts.

Key locations:
- `~/.openclaw/.env` -- ALL secrets (Telegram, Discord, Slack, Twilio, API keys, etc.)
- `~/.openclaw/openclaw.json` -- uses `${ENV_VAR}` references throughout
- `~/.openclaw/agents/main/agent/auth-profiles.json` -- uses `${ANTHROPIC_API_KEY}` reference
- `~/bin/openclaw-health-monitor.sh` -- sources .env, uses $TELEGRAM_BOT_TOKEN
- `~/bin/openclaw-nightly-update.sh` -- sources .env, uses $TELEGRAM_BOT_TOKEN

If the Telegram bot token is rotated, update ONLY `~/.openclaw/.env` and restart the gateway.

### 8. Security Status (2026-03-02)

Full security audit (8 items) + health check (12 findings) completed 2026-03-02.
- Firewall enabled, stealth mode ON, Twilio webhook signature verification enabled
- All secrets migrated from plaintext to .env references
- OPEN: Discord groupPolicy="open" (CRITICAL) -- should be "allowlist"
- OPEN: denyCommands list (12 entries) all use invalid command names
- OPEN: hooks.allowRequestSessionKey=true -- should be false
- See RUNBOOK.md for full details and action plan

---

## Change Log

| Date | Change | Details |
|---|---|---|
| 2026-03-02 | Security hardening (session 2) | Discord allowlist (Bill-only), denyCommands rebuilt, hooks locked, log rotation, 320MB freed |
| 2026-03-02 | Security audit + health check | 8 security fixes (secrets migration, Twilio sig verify, firewall stealth, etc.) + 12-finding health check. See RUNBOOK.md |
| 2026-03-02 | Secrets consolidated to .env | All 21 secrets now in ~/.openclaw/.env (600 perms). Scripts source .env. Zero hardcoded tokens |
| 2026-02-27 | Fixed memorySearch.provider | Changed `"lancedb"` → `"local"` to resolve fatal config validation error |
| 2026-02-27 | Fixed voice-call serve block | Removed invalid `serve` property from voice-call plugin config |
| 2026-02-27 | Created this context file | Comprehensive documentation of Nash's configuration and architecture |
| 2026-02-25 | Partner Reports Phase 1 complete | SANY + XCMG weekly report automation live |
| 2026-02-24 | Native rebuild complete | Migrated from Docker to native macOS app architecture |
| 2026-02-23 | Pre-rebuild archive created | Docker-era state preserved at `~/.openclaw/archive-20260223` |
