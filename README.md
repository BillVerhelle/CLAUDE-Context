# CLAUDE-Context

Context files for Claude AI assistants. Contains the Claude Context Files shared to all BV Claude machines and Web instances.

## Folder Structure

```
CLAUDE-Context/
├── quickfi/                      # QuickFi business context
│   ├── QuickFi-Context.md        # Core company context
│   ├── QuickFi-Business-Strategy.md
│   ├── QuickFi-Memory-Setup-Prompt.md
│   ├── QuickFi-Folder-Structure-Summary.md
│   ├── competitive/              # Competitive intelligence
│   ├── content/                  # Marketing content
│   └── data/                     # Data documentation
├── projects/                     # Code projects
│   └── zillow-tracker/           # Nashville property tracker
├── mcp-configs/                  # MCP server configurations
└── shared-resources/             # Shared assets across contexts
```

## Usage

Clone this repo to provide Claude with persistent context across sessions:

```bash
git clone https://github.com/BillVerhelle/CLAUDE-Context.git
```

## Security Notes

- `.env` files and secrets are excluded via `.gitignore`
- Large data files (JSON) are excluded to keep the repo lightweight
- Review `.gitignore` before adding new file types
