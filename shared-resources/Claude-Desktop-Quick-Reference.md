# Claude Desktop & Claude Code — Quick Reference

**Machine:** MacBook Pro M5 Max 128GB (Primary Management)
**Last Updated:** 2026-04-10

---

## Active MCP Servers (10)

| Server | Command | Purpose | Status |
|--------|---------|---------|--------|
| filesystem | npx @modelcontextprotocol/server-filesystem | Read/write ~/Documents and ~/Development | ✅ |
| sequential-thinking | node (global) | Structured reasoning for complex tasks | ✅ |
| memory | node (global) | Persistent knowledge graph | ✅ |
| time | python3 -m mcp_server_time | Timezone-aware time queries | ✅ |
| netlify | npx @netlify/mcp | Netlify deploy and management | ✅ |
| github | npx @modelcontextprotocol/server-github | GitHub repo management (PAT from .env) | ✅ |
| openclaw-nash | node openclaw-mcp | Nash — NY Library Mac Studio (100.65.195.9:18800) | ✅ |
| openclaw-lex | node openclaw-mcp | Lex — TN Mac Studio (100.96.133.64:18800) | ✅ |
| openclaw-rex | node openclaw-mcp | Rex — Mac Mini 02 (100.69.50.34:18800) | ✅ |
| openclaw-mack | node openclaw-mcp | Mack — Mac Mini 03 (100.92.84.30:18800) | ✅ |

---

## Managed AI Nodes

| Alias | Machine | Tailscale IP | OpenClaw | SSH |
|-------|---------|-------------|---------|-----|
| `nash` | NY Library Mac Studio M4 Max | 100.65.195.9 | ✅ live — OC 2026.4.8 (openclaw-nash) | `ssh nash` |
| `lex` | TN Mac Studio M4 Max | 100.96.133.64 | ✅ live — OC 2026.4.2 (openclaw-lex) | `ssh lex` |
| `mini02` | Mac Mini 02 (Rex) | 100.69.50.34 | ✅ live — OC 2026.4.2 (openclaw-rex) | `ssh mini02` |
| `mini03` | Mac Mini 03 (Mack) | 100.92.84.30 | ✅ live — OC 2026.4.2 (openclaw-mack) | `ssh mini03` |

---

## Claude Code Launcher (`cc`)

| Option | Workspace | Notes |
|--------|-----------|-------|
| 1 | General | Workflow rules only |
| 2 | QuickFi | + QuickFi project context |
| 3 | CLAUDE-Context | + repo context |
| 4 | Lex (TN Studio) | TN Mac Studio OpenClaw via Tailscale — full autonomy |
| 5 | Nash (Remote) | NY Mac Studio OpenClaw via Tailscale |

---

## Key File Locations

| File | Path | Purpose |
|------|------|---------|
| Claude Code config | `~/.claude/config.json` | MCP servers for Claude Code |
| Claude Desktop config | `~/Library/Application Support/Claude/claude_desktop_config.json` | MCP servers for Claude Desktop |
| Claude Code settings | `~/.claude/settings.json` | Global behavior flags |
| CLAUDE.md | `~/.claude/CLAUDE.md` | Workflow rules + machine/fleet context |
| API keys / secrets | `~/.claude/.env` | GitHub PAT, Slack, Airtable, OpenAI tokens |
| SSH config | `~/.ssh/config` | Host aliases for all managed nodes |
| cc launcher | `~/bin/cc` | Claude Code workspace menu |
| MCP logs | `~/Library/Logs/Claude/mcp-server-<name>.log` | Per-server diagnostics |

---

## Remote Management

```bash
# SSH to any node
ssh nash       # NY Library Mac Studio (100.65.195.9)
ssh lex        # TN Mac Studio (100.96.133.64)
ssh mini02     # Mac Mini 02 / Rex (100.69.50.34)
ssh mini03     # Mac Mini 03 / Mack (100.92.84.30)

# OpenClaw gateway health check (all bind to tailnet IP, NOT loopback)
curl http://100.65.195.9:18800/health    # Nash
curl http://100.96.133.64:18800/health   # Lex
curl http://100.69.50.34:18800/health    # Rex
curl http://100.92.84.30:18800/health    # Mack

# Power settings (all nodes configured as always-on servers)
# sleep=0, disksleep=0, powernap=0, autorestart=1, displaysleep=0

# Tailscale system daemon installed on ALL nodes (2026-04-09/10)
# FileVault unlock required after hard reboot → Tailscale auto-connects (no login needed)
```

---

## Troubleshooting

| Problem | Check |
|---------|-------|
| openclaw-nash/lex not connecting | `curl http://<ip>:18800/` — is gateway up? |
| Gateway down | `ssh <node>` → `launchctl list \| grep gateway` |
| Gateway config error | `ssh <node>` → `tail -20 ~/.openclaw/logs/gateway.err.log` |
| Gateway restart | `ssh <node>` → `launchctl bootout gui/$(id -u)/ai.openclaw.gateway && launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist` |
| Node offline | Check `tailscale status` — sleep settings should prevent this |
