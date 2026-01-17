# Claude Desktop MCP Servers - Quick Reference Guide

**Last Updated:** January 17, 2026
**Total MCP Servers:** 15

---

## 📁 File & Data Management

### **Filesystem**
- **Access:** Documents, Desktop, Downloads, Projects
- **Use for:** Reading/writing files, managing projects
- **Example:** "Read all markdown files in Documents folder"

### **SQLite**
- **Database:** ~/Documents/databases/claude.db
- **Use for:** Structured data storage, analysis, reporting
- **Example:** "Create a table to track my leads and store this data"

### **Git**
- **Repository:** ~/Projects/zillow-property-tracker
- **Use for:** Version control, commits, branches
- **Example:** "Show me recent commits in my zillow project"

---

## 🔍 Search & Discovery

### **Brave Search**
- **Type:** Keyword-based web search
- **Use for:** General queries, news, current events
- **Example:** "Search for recent real estate market trends"

### **Exa Search** ⭐ NEW
- **Type:** AI-powered semantic search
- **Use for:** Finding specific content, research papers, niche topics
- **Example:** "Find technical articles about property valuation algorithms"
- **Status:** ⚠️ Needs API key

### **Everything** ⭐ NEW
- **Type:** Fast local file search (macOS)
- **Use for:** Finding files instantly across entire Mac
- **Example:** "Find all PDF files related to real estate"

---

## 🌐 Web Automation & Scraping

### **Fetch** ⭐ NEW
- **Type:** Web content extraction
- **Use for:** Scraping websites, extracting data, downloading content
- **Example:** "Fetch and extract the main content from this URL"

### **Playwright** ⭐ NEW
- **Type:** Advanced browser automation
- **Use for:** LinkedIn automation, complex web interactions, form filling
- **Example:** "Navigate to this LinkedIn profile and extract the work history"

### **Puppeteer**
- **Type:** Browser automation (simpler than Playwright)
- **Use for:** Screenshots, PDF generation, basic automation
- **Example:** "Take a screenshot of this website"

---

## 📄 Document Processing

### **Docling**
- **Type:** Document conversion (PDF, Word, etc.)
- **Use for:** Converting documents to markdown, extracting text
- **Example:** "Convert this PDF to markdown format"

### **YouTube Transcript** ⭐ NEW
- **Type:** Video transcript extraction
- **Use for:** Getting transcripts from YouTube videos
- **Example:** "Get the transcript from this YouTube video: [URL]"

---

## 💼 Business & Productivity

### **GitHub**
- **Connected:** ✅ With your personal access token
- **Use for:** Managing repos, issues, PRs, code search
- **Example:** "Show me open issues in my repositories"

### **Google Maps** ⭐ NEW
- **Type:** Location and mapping data
- **Use for:** Property locations, distance calculations, place info
- **Example:** "Find properties within 5 miles of downtown Nashville"
- **Status:** ⚠️ Needs API key

### **Memory**
- **Type:** Persistent context storage
- **Use for:** Remembering information across conversations
- **Example:** "Remember that my target market is Nashville real estate investors"

---

## 🧠 Enhanced Capabilities

### **Sequential Thinking** ⭐ NEW
- **Type:** Advanced reasoning for complex problems
- **Use for:** Multi-step analysis, strategic planning, complex research
- **Example:** "Use sequential thinking to analyze the best market entry strategy"

---

## 🎯 Common Workflows

### Real Estate Research
```
Combining: Google Maps + Fetch + SQLite
1. Find properties in target area (Maps)
2. Scrape property details (Fetch)
3. Store in database (SQLite)
4. Analyze trends
```

### LinkedIn Lead Generation
```
Combining: Playwright + Fetch + Memory
1. Search for prospects (Playwright)
2. Extract profile data (Fetch)
3. Store research notes (Memory)
4. Export to CSV (Filesystem)
```

### YouTube Content Analysis
```
Combining: YouTube Transcript + Sequential Thinking + Memory
1. Extract transcript (YouTube)
2. Analyze key points (Sequential Thinking)
3. Store insights (Memory)
4. Generate summary (Filesystem)
```

### Market Research
```
Combining: Exa + Brave Search + Docling + SQLite
1. Find research papers (Exa)
2. Search recent news (Brave)
3. Convert PDFs (Docling)
4. Analyze and store (SQLite)
```

### Competitor Analysis
```
Combining: Playwright + GitHub + Memory + Sequential Thinking
1. Research companies (Playwright on LinkedIn)
2. Check their GitHub (GitHub)
3. Store findings (Memory)
4. Strategic analysis (Sequential Thinking)
```

---

## 💡 Pro Tips

### For Research:
- Start with **Exa** for semantic search, fall back to **Brave** for current events
- Use **Sequential Thinking** for complex, multi-step analysis
- Store findings in **Memory** for quick recall

### For Automation:
- Use **Playwright** for complex interactions (LinkedIn, forms)
- Use **Puppeteer** for simple tasks (screenshots, PDFs)
- Use **Fetch** for static content extraction

### For Data Management:
- **SQLite** for structured data you'll query
- **Memory** for quick notes and context
- **Filesystem** for reports and exports

### For LinkedIn:
- Use **Playwright** to navigate and interact
- Use **Fetch** to extract specific content
- Add delays (2-5 seconds) between actions
- Store results in **SQLite** for analysis

---

## 🚀 Example Prompts

### YouTube Research:
```
"Get the transcript from this YouTube video and summarize the key points: [URL]"
```

### LinkedIn Profile Research:
```
"Use Playwright to extract information from this LinkedIn profile: [URL]
Store the work history and skills in Memory tagged as 'lead-research'"
```

### Property Research:
```
"Use Google Maps to find all properties within 3 miles of [address]
Then use Fetch to get details from each property listing
Store results in SQLite database"
```

### Market Analysis:
```
"Use Exa to find recent articles about [topic]
Then use Sequential Thinking to analyze trends
Save analysis to Documents/market-analysis.md"
```

### File Search:
```
"Use Everything to find all Excel files related to 'property' or 'real estate'
from the last 30 days"
```

---

## ⚙️ Configuration Status

| Server | Status | Notes |
|--------|--------|-------|
| Filesystem | ✅ Active | 4 directories |
| Docling | ✅ Active | With caching |
| Memory | ✅ Active | - |
| SQLite | ✅ Active | claude.db |
| Git | ✅ Active | zillow-property-tracker |
| Puppeteer | ✅ Active | - |
| GitHub | ✅ Active | Authenticated |
| Brave Search | ✅ Active | Authenticated |
| YouTube Transcript | ✅ Active | - |
| Fetch | ✅ Active | - |
| Playwright | ✅ Active | - |
| Sequential Thinking | ✅ Active | - |
| Everything | ✅ Active | - |
| Exa | ⚠️ Pending | Need API key |
| Google Maps | ⚠️ Pending | Need API key |

---

## 🔑 Pending Setup

### To Complete Full Setup:

1. **Get Exa API Key**
   - Visit: https://exa.ai/
   - Sign up for free account
   - Copy API key
   - Provide to me to add to config

2. **Get Google Maps API Key**
   - Visit: https://console.cloud.google.com/google/maps-apis
   - Create project
   - Enable Maps JavaScript API and Places API
   - Create credentials
   - Copy API key
   - Provide to me to add to config

---

## 📚 Additional Resources

- **LinkedIn Automation Guide:** ~/Documents/LinkedIn-Automation-Workflow.md
- **Claude Desktop Logs:** ~/Library/Logs/Claude/
- **SQLite Database:** ~/Documents/databases/claude.db
- **Config File:** ~/Library/Application Support/Claude/claude_desktop_config.json

---

## 🆘 Getting Help

Ask Claude Desktop:
- "Show me examples of using [server name]"
- "Help me create a workflow for [task]"
- "What's the best way to [accomplish goal]?"
- "Combine [server 1] and [server 2] to [do something]"

---

**Happy Automating! 🚀**
