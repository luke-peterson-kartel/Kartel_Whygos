# Kartel AI WhyGO Management System

Enterprise goal tracking and progress management system for Kartel AI's 2026 company, department, and individual goals.

## Overview

The WhyGO Management System tracks 74 outcomes across 4 company goals, 14 department goals, and 2 individual goals for Kartel AI's 2026 fiscal year. Built with a clean architecture that separates business logic from data access, making it easy to scale from JSON files to a full database.

## Features

- **Progress Tracking**: Record quarterly actuals with automatic status calculation
- **Status Indicators**:
  - `[+]` On pace (≥100% of target)
  - `[~]` Slightly off (80-99% of target)
  - `[-]` Off pace (<80% of target)
- **Dashboard Views**: Company, department, outcome, and person-level views
- **Clean Architecture**: Repository pattern with swappable data backends
- **CLI Tools**: Command-line interface for recording and viewing progress

## Quick Start

### View Current Status

```bash
# View company dashboard
python scripts/view_dashboard.py company

# View department dashboard
python scripts/view_dashboard.py department dept_sales

# View specific outcome details
python scripts/view_dashboard.py outcome cg_1_o1

# View all outcomes for a person
python scripts/view_dashboard.py person person_ben_kusin
```

### Record Progress

```bash
# Record numeric actual
python scripts/record_progress.py cg_1_o1 Q1 5 --person person_ben_kusin --notes "Signed 5 clients"

# Record milestone actual
python scripts/record_progress.py cg_4_o3 Q1 "MVP" --person person_niels

# Record with blocker
python scripts/record_progress.py cg_2_o1 Q1 35 --person person_luke_peterson --blocker "Workflow delays"
```

## Project Structure

```
WHYGOs/
├── kartel-whygo-system/        # Main application
│   ├── src/
│   │   ├── models/             # Data models
│   │   ├── repositories/       # Data access layer
│   │   ├── services/           # Business logic
│   │   ├── parsers/            # Markdown to JSON parsers
│   │   └── utils/              # Helper functions
│   ├── scripts/                # CLI tools
│   │   ├── record_progress.py
│   │   ├── view_dashboard.py
│   │   ├── import_whygos.py
│   │   └── verify_data.py
│   ├── data/                   # JSON data files
│   │   ├── company_whygos.json
│   │   ├── department_goals.json
│   │   ├── individual_goals.json
│   │   ├── progress_updates.json
│   │   ├── employees.json
│   │   └── departments.json
│   └── knowledge/              # Documentation
└── Company WhyGos/             # Source markdown files
```

## Architecture

The system uses a layered architecture with clean separation of concerns:

```
┌─────────────────────────────┐
│   CLI Tools (Presentation)  │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  Service Layer (Business)   │
│  - ProgressService           │
│  - WhygoService             │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  Repository Layer (Data)    │
│  - JsonWhygoRepository      │
│  - JsonProgressRepository   │
└──────────────┬──────────────┘
               │
         ┌─────▼─────┐
         │ JSON Files│
         └───────────┘
```

**Key Benefits:**
- **Swappable Backend**: Replace JSON with PostgreSQL/MongoDB by implementing the same interfaces
- **Testable**: Each layer can be tested independently
- **Maintainable**: Changes to one layer don't affect others

## Data Import

The system includes a parser that converts markdown WhyGO documents to structured JSON:

```bash
# Re-import data from markdown files
python scripts/import_whygos.py

# Verify imported data
python scripts/verify_data.py
```

## Current Status (Phase 2 Complete)

- ✅ **Phase 1**: Data parser and import system
- ✅ **Phase 2**: Progress tracking with repository pattern
- 🚧 **Phase 3**: Web dashboard (planned)
- 🚧 **Phase 4**: Goal creation workflow (planned)
- 🚧 **Phase 5**: Analytics and reporting (planned)

## Technology Stack

- **Language**: Python 3.9+
- **Data Storage**: JSON (designed for easy database migration)
- **Architecture**: Repository pattern with ABC interfaces
- **CLI**: Argparse for command-line tools

## Team

- **CEO**: Kevin Reilly
- **President**: Luke Peterson
- **CRO**: Ben Kusin
- **Production**: Wayan Palmieri
- **Generative**: Fill Isgro
- **Community**: Daniel Kalotov
- **Platform**: Niels Hoffmann

## 2026 Company Goals

1. **Prove Product-Market Fit**: 10 clients across 5 verticals
2. **Build Operational Excellence**: 50% margin, 90% on-time, 50+ NPS
3. **Build the Talent Engine**: 1,000 community members, 20 deployed talent
4. **Deploy Enterprise Platform**: Client Portal, Production Management, Generative Platform

## License

Proprietary - Kartel AI, Inc.

## Contributing

This is an internal tool for Kartel AI. For questions or support, contact Luke Peterson.
