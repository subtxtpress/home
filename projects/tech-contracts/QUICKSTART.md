# Quick Start

## View the Dashboard

Visit the live site — no installation needed:

**[subtxtpress.github.io/home/tools/tech-contracts/tech-contracts.html](https://subtxtpress.github.io/home/tools/tech-contracts/tech-contracts.html)**

Features:
- Search 310 DHS vendor profiles from the EFF dataset
- Filter by prime contractor status and AI/ML usage
- Query live contracts from USASpending.gov
- Generate FPDS and SAM.gov search links
- Export results to CSV

## Local Python Tools

For deeper analysis, use the Python tools locally:

### Option 1: Standalone Research Tool
```bash
python demo.py
```
No API server needed. Uses pandas to search, filter, and export vendor data.

### Option 2: Interactive CLI
```bash
python search.py
```
Menu-driven search interface built on the standalone tool.

### Option 3: Full API Server
```bash
pip install -r requirements.txt
python main.py
# Visit http://localhost:8000/docs
```
REST API with live government database queries and enriched profiles.

## Updating the Dataset

If the EFF Excel file is updated:

```bash
pip install pandas openpyxl
python extract_data.py
# Commit and push vendors.json
```

## Key Dataset Fields

Each vendor profile includes:
- **Company Name** and **Ref** ID
- **Categories of Products/Services**
- **Corporate Summary**
- **AI/ML in Marketing** flag
- **DHS Prime Contractor** status
- **Border Expo/Tech Summit** participation
- **Parent Company** and **Related Companies**
- **Official DHS Programs**
- **Federal Agency Contracts**
- **USASpending.gov** and **FPDS** links
