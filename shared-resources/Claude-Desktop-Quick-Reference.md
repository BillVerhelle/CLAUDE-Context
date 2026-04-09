# Claude Desktop & Claude Code — Quick Reference

**Machine:** MacBook Pro M5 Max 128GB (Primary Management)
**Last Updated:** 2026-04-09

---

## Active MCP Servers (8)

| Server | Command | Purpose | Status |
|--------|---------|---------|--------|
| filesystem | npx @modelcontextprotocol/server-filesystem | Read/write ~/Documents and ~/Development | ✅ |
| sequential-thinking | node (global) | Structured reasoning for complex tasks | ✅ |
| memory | node (global) | Persistent knowledge graph | ✅ |
| time | python3 -m mcp_server_time | Timezone-aware time queries | ✅ |
| netlify | npx @netlify/mcp | Netlify deploy and management | ✅ |
| github | npx @modelcontextprotocol/server-github | GitHub repo management (PAT from .env) | ✅ |
| openclaw-nash | node openclaw-mcp | Nash — NY Library Mac Studio (100.65.195.9:18800) | ✅ |
| openclaw-lex | node openclaw-mcp | Lex — TN Mac Studio (100.127.242.121:18800) | ✅ |

---

## Managed AI Nodes

| Alias | Machine | Tailscale IP | OpenClaw | SSH |
|-------|---------|-------------|---------|-----|
| `nash` | NY Library Mac Studio M4 Max | 100.65.195.9 | ✅ live (openclaw-nash) | `ssh nash` |
| `lex` | TN Mac Studio M4 Max | 100.127.242.121 | ✅ live (openclaw-lex) | `ssh lex` |
| `mini02` | Mac Mini 02 | 100.122.79.7 | ⏳ not installed | `ssh mini02` |
| `mini03` | Mac Mini 03 | 100.109.233.117 | ⏳ not installed | `ssh mini03` |

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
ssh nash       # NY Library Mac Studio
ssh lex        # TN Mac Studio
ssh mini02     # Mac Mini 02
ssh mini03     # Mac Mini 03

# OpenClaw gateway health check
curl http://100.65.195.9:18800/      # Nash
curl http://100.127.242.121:18800/   # Lex

# Power settings (all nodes configured as always-on servers)
# sleep=0, disksleep=0, powernap=0, autorestart=1, displaysleep=0
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
