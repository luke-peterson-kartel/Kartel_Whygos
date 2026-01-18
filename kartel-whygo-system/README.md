# Kartel AI WhyGO Management System

An agentic system for managing and tracking Kartel AI's 2026 company, department, and individual goals.

## What is WhyGO?

WhyGO is a goal-setting framework with three components:
- **WHY** - Strategic context (why this goal matters)
- **GOAL** - Clear objective statement
- **OUTCOMES** - Measurable results with quarterly targets

## Project Structure

```
kartel-whygo-system/
├── CLAUDE.md              # Agent instructions (Claude Code reads this)
├── README.md              # This file
├── knowledge/             # Reference documentation
│   ├── WHYGO_FRAMEWORK.md
│   ├── COMPANY_WHYGOS.md
│   ├── EMPLOYEE_REFERENCE.md
│   ├── DATA_STRUCTURES.md
│   └── COACHING_INSTRUCTIONS.md
├── source-docs/           # Original source files
│   ├── *.docx
│   └── Employee_List_2026.xlsx
├── src/                   # Application code
│   ├── models/
│   ├── services/
│   ├── api/
│   └── utils/
└── data/                  # JSON data files
```

## Key Concepts

### Goal Hierarchy
```
Company WhyGOs (4 goals)
    └── Department WhyGOs (max 3 per department)
            └── Individual WhyGOs (max 3 per person)
```

### 2026 Company Priorities
1. **Prove Product-Market Fit** - 10 clients across 5 verticals
2. **Build Operational Excellence** - 50% margin, 90% on-time, 50+ NPS
3. **Build the Talent Engine** - 1,000 community members, 20 deployed talent
4. **Deploy Enterprise Platform** - Client Portal, Production Management, Generative Platform

### Status Tracking
| Status | Meaning | Threshold |
|--------|---------|-----------|
| [+] | On pace | ≥100% of target |
| [~] | Slightly off | 80-99% of target |
| [-] | Off pace | <80% of target |

## Usage

The system supports:
- **Goal Setting** - Guided creation of WhyGOs with coaching prompts
- **Progress Tracking** - Recording actuals against quarterly targets
- **Reporting** - Dashboards at company, department, and individual levels
- **Alignment Validation** - Ensuring all goals ladder to parent goals

## Key Rules

1. Maximum **3 WhyGOs** per department or individual
2. Every goal must **ladder up** to a parent goal
3. All outcomes must be **measurable** with quarterly targets
4. Each outcome has **exactly one owner**

## Getting Started

1. Clone this repository
2. Review `CLAUDE.md` for agent instructions
3. Review `knowledge/` files for methodology and data
4. Implement features per `knowledge/DATA_STRUCTURES.md`

## Team

- **CEO**: Kevin Reilly
- **President**: Luke Peterson  
- **CRO**: Ben Kusin
- **Department Heads**: Wayan (Production), Fill (Generative), Daniel (Community), Niels (Platform)

See `knowledge/EMPLOYEE_REFERENCE.md` for full org chart.
