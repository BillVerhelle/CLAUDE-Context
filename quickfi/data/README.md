# QuickFi Data Directory

**Purpose:** Data storage, exports, and analytics for QuickFi operations

---

## What Goes Here

- SQLite database exports
- CSV data exports
- JSON data files
- Analytics reports
- Data visualizations (described)
- Research data compilations
- Prospect and customer databases
- Metrics and KPI tracking

---

## Naming Convention

```
YYYY-MM-DD-data-type-description.extension
```

**Examples:**
- `2026-01-17-competitive-analysis-export.csv`
- `2026-01-17-prospect-pipeline.json`
- `2026-01-17-market-metrics-q1.csv`
- `2026-01-17-research-compilation.json`

---

## Data Categories

### Competitive Intelligence Data
- Competitor profiles (structured)
- Feature comparisons
- Pricing data
- Market share estimates
- Win/loss records

### Market Research Data
- Market size and trends
- Customer segments
- Geographic data
- Industry statistics
- Demographic information

### Prospect & Customer Data
- Lead information
- Qualification data
- Engagement tracking
- Pipeline metrics
- Customer profiles

### Product & Feature Data
- Feature specifications
- User stories
- Roadmap items
- Requirements tracking
- Decision logs

### Analytics & Metrics
- KPIs and metrics
- Performance data
- Usage analytics
- Business intelligence
- Trend analysis

---

## Recommended Prompts

### Export Research to Data File:
```
"Export QuickFi research data to structured format:

Retrieve all Memory items tagged 'quickfi-*'
Query SQLite for all QuickFi-related tables

Create comprehensive data export:
1. Market research findings
2. Competitive intelligence
3. Prospect information
4. Product decisions
5. Key metrics

Export formats:
- JSON for hierarchical data
- CSV for tabular data
- Include metadata (source, date, confidence)

Save to Documents/quickfi-data/"
```

### Create Analytics Dashboard Data:
```
"Create data file for QuickFi analytics dashboard:

Compile from Memory + SQLite:
1. Pipeline metrics
   - Prospects by stage
   - Conversion rates
   - Deal values

2. Competitive metrics
   - Win/loss rates
   - Competitive encounters
   - Market share trends

3. Product metrics
   - Feature priorities
   - Development progress
   - User feedback

4. Market metrics
   - Market size trends
   - Segment growth
   - Industry developments

Export to JSON with structure:
{
  "generated": "timestamp",
  "period": "date range",
  "metrics": {
    "pipeline": {...},
    "competitive": {...},
    "product": {...},
    "market": {...}
  }
}

Save to Documents/quickfi-data/"
```

### Compile Research Database:
```
"Compile comprehensive research database for QuickFi:

Aggregate from all sources:
- Memory tagged 'quickfi-research-*'
- SQLite research tables
- Research files in quickfi-research/

Create unified dataset:
1. Equipment finance market data
2. Embedded lending trends
3. Competitive landscape
4. Customer insights
5. Technology trends
6. Regulatory environment

Export formats:
- master-research-database.json (complete)
- market-data.csv (metrics)
- trends.csv (time-series)
- competitors.csv (comparative)

Include:
- Source attribution
- Data quality scores
- Timestamps
- Update frequency

Save to Documents/quickfi-data/"
```

---

## Data Management

### Storage Strategy

**SQLite Database:**
- Primary structured data storage
- Located: `~/Documents/databases/claude.db`
- Tables by category:
  - quickfi_competitors
  - quickfi_prospects
  - quickfi_research
  - quickfi_features
  - quickfi_metrics

**CSV Files:**
- Tabular data exports
- Easy to import into spreadsheets
- Good for time-series data
- Portable format

**JSON Files:**
- Hierarchical/nested data
- API-friendly format
- Complex data structures
- Metadata inclusion

**Memory:**
- Quick reference data
- Frequently accessed facts
- Ongoing project context
- Tag: 'quickfi-[category]'

### Backup Strategy

**Daily:**
- Automatic via Time Machine (if enabled)
- SQLite database backed up

**Weekly:**
- Manual export to this folder
- Create timestamped backups
- Verify data integrity

**Monthly:**
- Archive old exports
- Clean up unused files
- Document data schema changes

---

## Data Schema Recommendations

### Competitor Data
```json
{
  "company_name": "string",
  "founded": "date",
  "category": "systems_of_record | systems_of_action",
  "approach": "employee_centric | borrower_driven",
  "funding": "number",
  "employees": "number",
  "products": ["array"],
  "target_market": "string",
  "strengths": ["array"],
  "weaknesses": ["array"],
  "last_updated": "timestamp"
}
```

### Prospect Data
```json
{
  "company_name": "string",
  "contact_name": "string",
  "title": "string",
  "industry": "string",
  "size": "string",
  "stage": "string",
  "score": "number",
  "needs": ["array"],
  "competitors_considered": ["array"],
  "next_steps": "string",
  "last_interaction": "timestamp"
}
```

### Research Data
```json
{
  "topic": "string",
  "category": "string",
  "date_researched": "timestamp",
  "sources": ["array"],
  "key_findings": ["array"],
  "statistics": {},
  "implications": ["array"],
  "confidence_level": "number",
  "tags": ["array"]
}
```

### Product Feature Data
```json
{
  "feature_name": "string",
  "description": "string",
  "category": "string",
  "priority": "number",
  "status": "string",
  "user_stories": ["array"],
  "technical_complexity": "number",
  "business_value": "number",
  "dependencies": ["array"],
  "assigned_to": "string",
  "target_release": "string"
}
```

---

## Analytics & Reporting

### Key Metrics to Track

**Pipeline Metrics:**
- Total prospects
- Prospects by stage
- Conversion rates
- Average deal size
- Sales cycle length
- Win rate

**Competitive Metrics:**
- Competitors encountered
- Win/loss by competitor
- Competitive displacement rate
- Feature gap analysis
- Price positioning

**Market Metrics:**
- Total addressable market
- Serviceable market
- Market growth rate
- Segment sizes
- Trend indicators

**Product Metrics:**
- Features delivered
- Development velocity
- User satisfaction
- Adoption rates
- Feature utilization

### Report Types

**Weekly:**
- Activity summary
- Pipeline changes
- Competitive developments
- Key metrics snapshot

**Monthly:**
- Comprehensive metrics
- Trend analysis
- Strategic insights
- Action items

**Quarterly:**
- Business review
- Market analysis
- Competitive landscape
- Strategic planning

---

## Data Quality Standards

### Quality Criteria

**Accuracy:**
- Verified from multiple sources
- Regular updates
- Error checking
- Source attribution

**Completeness:**
- Required fields populated
- Comprehensive coverage
- Missing data documented
- Regular audits

**Consistency:**
- Standard formats
- Consistent terminology
- Unified schema
- Cross-referenced

**Timeliness:**
- Recent data
- Update frequency noted
- Timestamp all entries
- Flag stale data

### Data Validation

Before using data:
- [ ] Check data freshness
- [ ] Verify sources
- [ ] Validate calculations
- [ ] Review for completeness
- [ ] Test consistency
- [ ] Document limitations

---

## Integration with Other Folders

### Research → Data
Research findings exported to structured data

### Competitive → Data
Competitor profiles stored in database

### Sales → Data
Pipeline and prospect tracking

### Product → Data
Feature specs and roadmap in database

### Partnerships → Data
Partner profiles and opportunities

---

## Data Security & Privacy

### Security Considerations

**Sensitive Data:**
- Prospect/customer info
- Pricing information
- Financial data
- Strategic plans

**Access Control:**
- Limit access to sensitive data
- Use encryption where appropriate
- Regular security audits
- Backup securely

**Compliance:**
- Data privacy regulations
- Data retention policies
- Data disposal procedures
- Audit trails

### Best Practices

- Don't store passwords or API keys
- Anonymize customer data when possible
- Encrypt sensitive exports
- Document data handling procedures
- Regular security reviews

---

## Useful SQLite Queries

### View All QuickFi Tables:
```sql
SELECT name FROM sqlite_master
WHERE type='table' AND name LIKE 'quickfi_%';
```

### Export Table to CSV:
```sql
.mode csv
.output Documents/quickfi-data/export.csv
SELECT * FROM quickfi_competitors;
.output stdout
```

### Get Recent Research:
```sql
SELECT * FROM quickfi_research
WHERE date_researched >= date('now', '-30 days')
ORDER BY date_researched DESC;
```

### Competitor Summary:
```sql
SELECT category, COUNT(*) as count,
       AVG(funding) as avg_funding
FROM quickfi_competitors
GROUP BY category;
```

---

## Automation Opportunities

### Scheduled Exports:
```bash
#!/bin/bash
# Weekly data export script

DATE=$(date +%Y-%m-%d)
EXPORT_DIR=~/Documents/quickfi-data

# Export from SQLite
sqlite3 ~/Documents/databases/claude.db <<EOF
.mode csv
.output $EXPORT_DIR/$DATE-competitors.csv
SELECT * FROM quickfi_competitors;
.output $EXPORT_DIR/$DATE-prospects.csv
SELECT * FROM quickfi_prospects;
.output $EXPORT_DIR/$DATE-research.csv
SELECT * FROM quickfi_research;
EOF

echo "Data exported to $EXPORT_DIR"
```

### Data Refresh:
Create prompts to refresh data weekly:
```
"Refresh QuickFi competitive data:
1. Check for updates on tracked competitors
2. Update SQLite database
3. Export to quickfi-data/
4. Store summary in Memory"
```

---

## Quality Standards

Data files should:
- [ ] Use consistent naming convention
- [ ] Include metadata (date, source, version)
- [ ] Be properly formatted
- [ ] Have clear documentation
- [ ] Be regularly updated
- [ ] Include data dictionary
- [ ] Be backed up
- [ ] Follow security guidelines

---

**Last Updated:** January 17, 2026
