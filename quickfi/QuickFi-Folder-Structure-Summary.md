# QuickFi Folder Structure - Implementation Summary

**Created:** January 17, 2026
**Location:** `/Users/billverhelle/Documents/`

---

## Overview

A comprehensive folder structure has been created for organizing all QuickFi business development materials. All folders are configured to work seamlessly with your Claude Desktop MCP servers (Memory, SQLite, Filesystem, etc.).

---

## Folder Structure

```
~/Documents/
├── QuickFi-Business-Strategy.md (original vision document)
├── QuickFi-Context.md (50+ page reference guide)
├── QuickFi-Memory-Setup-Prompt.md (one-time Memory setup)
├── QuickFi-Prompting-Guide.md (how-to guide with templates)
└── QuickFi-Folder-Structure-Summary.md (this document)

├── quickfi-content/ (Content creation & marketing)
│   └── README.md
├── quickfi-research/ (Market research & analysis)
│   └── README.md
├── quickfi-sales/ (Sales materials & proposals)
│   └── README.md
├── quickfi-partnerships/ (Partnership development)
│   └── README.md
├── quickfi-product/ (Product specs & roadmap)
│   └── README.md
├── quickfi-competitive/ (Competitive intelligence)
│   └── README.md
└── quickfi-data/ (Data exports & analytics)
    └── README.md
```

---

## Folder Purposes

### 1. quickfi-content/
**Purpose:** Content creation and marketing materials

**Contents:**
- Blog posts and articles
- LinkedIn posts and social media content
- Thought leadership pieces
- Website copy and email campaigns
- Press releases and case studies
- White papers

**Key Features:**
- Recommended prompts for blog posts, LinkedIn content, sales materials
- Quality checklist ensuring QuickFi positioning
- Content type categorization

---

### 2. quickfi-research/
**Purpose:** Market research and competitive intelligence

**Contents:**
- Market analysis and trends
- Industry reports and statistics
- Customer persona research
- Technology landscape research
- Regulatory environment analysis

**Key Features:**
- Multi-tool research prompts (Exa + Brave + Playwright)
- Sequential Thinking integration for analysis
- Memory and SQLite storage strategies
- Research methodology templates

---

### 3. quickfi-sales/
**Purpose:** Sales enablement materials and proposals

**Contents:**
- Pitch decks and presentations
- Sales proposals and quotes
- Product demos and walk-throughs
- ROI calculators and business cases
- Battle cards and objection handling
- Customer success stories

**Key Features:**
- Audience-specific value propositions (Banks, Borrowers, Investors, Partners)
- Objection handling framework
- Discovery questions and qualification criteria
- Battle card templates

---

### 4. quickfi-partnerships/
**Purpose:** Partnership development and relationship management

**Contents:**
- Partnership proposals and agreements
- Partner research and profiles
- Ecosystem mapping
- Integration specifications
- Joint go-to-market plans
- Partner enablement materials

**Key Features:**
- Partner research prompts using multiple MCP servers
- 5-stage partnership development process
- Integration considerations (technical, business, strategic)
- Partner profile templates

---

### 5. quickfi-product/
**Purpose:** Product strategy and development documentation

**Contents:**
- Product strategy documents
- Feature specifications and user stories
- Technical architecture docs
- Product roadmaps
- User experience flows
- API documentation
- Product decision logs

**Key Features:**
- Feature specification template aligned with QuickFi principles
- 5 product principles (Borrower-First, Real-Time Action, AI-Enhanced, Embedded, Scalable)
- Development workflow guidance
- Product decision log template

---

### 6. quickfi-competitive/
**Purpose:** Competitive analysis and strategic positioning

**Contents:**
- Competitor profiles
- Competitive analyses and SWOT
- Battle cards
- Win/loss analyses
- Market positioning studies
- Feature and pricing comparisons

**Key Features:**
- 4-category competitor framework (Legacy Systems, Workflow Optimization, Digital Lending, Systems of Action)
- Comprehensive competitor profile template
- Battle card template with trap-setting questions
- Competitive monitoring schedule (daily/weekly/monthly/quarterly)
- Win/loss analysis framework

---

### 7. quickfi-data/
**Purpose:** Data storage, exports, and analytics

**Contents:**
- SQLite database exports
- CSV data exports
- JSON data files
- Analytics reports
- Research data compilations
- Prospect and customer databases
- Metrics and KPI tracking

**Key Features:**
- Integration with `~/Documents/databases/claude.db` SQLite database
- Data schema recommendations (Competitor, Prospect, Research, Product Feature)
- Backup strategy (daily/weekly/monthly)
- Data quality standards and validation checklist
- Useful SQLite queries for exports and analysis
- Automation script templates

---

## Universal Naming Convention

All QuickFi files follow this convention:
```
YYYY-MM-DD-topic-type.md
```

**Examples:**
- `2026-01-17-embedded-lending-blog-post.md`
- `2026-01-17-acme-corp-partnership-proposal.md`
- `2026-01-17-competitor-x-profile.md`
- `2026-01-17-borrower-dashboard-spec.md`

---

## Integration with MCP Servers

### Filesystem MCP
- **Access:** All folders accessible via `/Users/billverhelle/Documents`
- **Usage:** Read/write/search QuickFi files

### Memory MCP
- **Setup:** Run `QuickFi-Memory-Setup-Prompt.md` once to store core context
- **Tags:** Use `quickfi-[category]` for persistent storage
- **Access:** Available across all Claude Desktop conversations

### SQLite MCP
- **Database:** `~/Documents/databases/claude.db`
- **Tables:** Recommended structure for competitors, prospects, research, features, metrics
- **Export:** Use quickfi-data/ folder for CSV/JSON exports

### Research MCP Servers (Exa, Brave, Playwright)
- **Exa:** Semantic search for deep research
- **Brave:** Recent news and developments
- **Playwright:** LinkedIn, company pages, structured data extraction

### Sequential Thinking MCP
- **Usage:** Complex analysis requiring multi-step reasoning
- **Best for:** Market analysis, competitive strategy, product decisions

---

## How to Use This Structure

### One-Time Setup

1. **Store QuickFi Context in Memory:**
   ```
   Read and execute: ~/Documents/QuickFi-Memory-Setup-Prompt.md
   ```
   This makes QuickFi context available in all future conversations.

2. **Initialize SQLite Tables (Optional):**
   Create tables for structured data storage:
   - quickfi_competitors
   - quickfi_prospects
   - quickfi_research
   - quickfi_features
   - quickfi_metrics

### Daily Workflow

**For Content Creation:**
```
"Read QuickFi-Context.md and create a LinkedIn post about embedded lending
transforming equipment finance. Research latest trends with Exa.
Save to Documents/quickfi-content/"
```

**For Market Research:**
```
"Research the current state of embedded lending in equipment finance.
Use Exa for deep analysis, Brave for recent news, Playwright for company data.
Save findings to Documents/quickfi-research/"
```

**For Competitive Analysis:**
```
"Create comprehensive competitor profile for [COMPETITOR].
Read QuickFi-Context.md first. Research with Exa + Brave + Playwright.
Analyze positioning using Sequential Thinking.
Save to Documents/quickfi-competitive/"
```

**For Sales Materials:**
```
"Create pitch deck outline for QuickFi targeting commercial banks.
Reference QuickFi-Context.md for positioning.
Save to Documents/quickfi-sales/"
```

**For Partnership Development:**
```
"Research potential partnership with [PARTNER].
Use Playwright for LinkedIn, Exa for business model, Brave for news.
Analyze fit with Sequential Thinking.
Save to Documents/quickfi-partnerships/"
```

**For Product Specs:**
```
"Create feature specification for borrower self-service dashboard.
Reference QuickFi-Context.md for systems of action principles.
Save to Documents/quickfi-product/"
```

**For Data Exports:**
```
"Export QuickFi research data to structured format.
Retrieve Memory items tagged 'quickfi-*'
Query SQLite for all QuickFi-related tables.
Export to JSON and CSV in Documents/quickfi-data/"
```

---

## Quality Standards

Each folder README includes a quality checklist. Key universal standards:

- **Always reference** QuickFi-Context.md for accurate positioning
- **Use correct terminology:** Systems of action, embedded lending, borrower-driven
- **Avoid incorrect positioning:** CRM, incremental improvements, systems of record
- **Include sources:** Cite research with Exa, Brave, or other tools
- **Store systematically:** Follow naming conventions
- **Update Memory/SQLite:** Store key findings for future reference
- **Tag appropriately:** Use quickfi-[category] tags

---

## System Configuration

**No additional configuration needed.** The existing Claude Desktop setup already supports this structure:

✅ **Filesystem MCP:** Has access to `/Users/billverhelle/Documents`
✅ **Memory MCP:** Ready for QuickFi context storage
✅ **SQLite MCP:** Connected to `~/Documents/databases/claude.db`
✅ **Research Servers:** Exa, Brave, Playwright configured
✅ **Sequential Thinking:** Available for complex analysis

---

## Next Steps

### Immediate
1. **Run QuickFi Memory Setup:**
   - Open `QuickFi-Memory-Setup-Prompt.md` in Claude Desktop
   - Execute the prompt to store core context in Memory
   - Verify with: "Retrieve all Memory items tagged 'quickfi'"

2. **Test the Structure:**
   - Create a sample piece of content using the recommended prompts
   - Verify files save correctly to appropriate folders

3. **Create First SQLite Tables (Optional):**
   - Use prompts in quickfi-data/README.md to create database schema
   - Test with sample data

### Ongoing
- **Daily:** Create and organize QuickFi materials in appropriate folders
- **Weekly:** Export data from Memory/SQLite to quickfi-data/
- **Monthly:** Review and consolidate research findings
- **Quarterly:** Update competitive intelligence and market analysis

---

## Resources

### Core Documents
- **QuickFi-Context.md:** Comprehensive reference (read this first!)
- **QuickFi-Prompting-Guide.md:** How-to guide with template prompts
- **QuickFi-Business-Strategy.md:** Original vision document

### Folder READMEs
Each folder has a detailed README with:
- Purpose and scope
- Naming conventions
- Recommended Claude Desktop prompts
- Templates and frameworks
- Quality checklists
- Integration guidelines

### Claude Desktop Documentation
- **00-START-HERE.md:** Master guide
- **Advanced-Prompt-Engineering-Guide.md:** COSMIC framework and orchestration
- **Workflow-Templates-Library.md:** 25+ ready-to-use templates
- **Claude-Desktop-Quick-Reference.md:** All 15 MCP servers with examples

---

## Troubleshooting

### Files Not Saving
- Verify Filesystem MCP server is running (check Claude Desktop status)
- Ensure path is `/Users/billverhelle/Documents/quickfi-[folder]/`

### Memory Not Available
- Run QuickFi-Memory-Setup-Prompt.md once
- Check Memory MCP server status in Claude Desktop

### SQLite Errors
- Verify database exists: `~/Documents/databases/claude.db`
- Check SQLite MCP server configuration
- Create database if missing: `sqlite3 ~/Documents/databases/claude.db`

### Research Servers Not Working
- Verify API keys in config: Exa, Brave, Google Maps
- Check MCP server status in Claude Desktop
- Review error messages for specific issues

---

## Maintenance

### Weekly
- Review new files in all quickfi-* folders
- Export important findings to SQLite
- Update Memory with key insights
- Clean up duplicate or outdated files

### Monthly
- Export SQLite data to quickfi-data/ (CSV/JSON backups)
- Review and consolidate research findings
- Update competitive intelligence
- Archive old files if needed

### Quarterly
- Comprehensive review of all folders
- Update folder READMEs if processes change
- Review SQLite schema and optimize
- Strategic planning using aggregated data

---

## Success Metrics

You'll know this structure is working when:

✅ All QuickFi materials organized in appropriate folders
✅ Easy to find previous research, analyses, and content
✅ Memory provides QuickFi context automatically in conversations
✅ SQLite contains structured data for queries and analysis
✅ Can quickly create new materials using recommended prompts
✅ Consistent naming and quality across all files
✅ Research findings easily accessible and reusable

---

**Folder Structure Status:** ✅ COMPLETE
**READMEs Created:** ✅ 7/7
**System Configuration:** ✅ No changes needed
**Ready for Use:** ✅ YES

---

**Last Updated:** January 17, 2026
