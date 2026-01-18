# Knowledge Base

Business knowledge and framework documentation for the WHYGOs Management System.

## Overview

This directory contains the business rules, framework documentation, and reference data that govern how the WHYGOs system operates. These files should be read before implementing any goal-related features.

## Knowledge Files

### [WHYGO_FRAMEWORK.md](WHYGO_FRAMEWORK.md)
The core framework rules:
- WHY-GOAL-OUTCOMES structure
- Maximum 3 WhyGOs per entity rule
- "Ladder up" requirement (must connect to parent goals)
- Measurable outcomes requirements
- Status calculation ([+] [~] [-])
- Quarterly pacing guidelines

**Read this**: For any goal creation, editing, or methodology questions

### [COMPANY_WHYGOS.md](COMPANY_WHYGOS.md)
Kartel AI's 2026 company goals:
- 4 strategic company WhyGOs
- Full WHY-GOAL-OUTCOMES for each
- Quarterly targets and ownership
- Strategic alignment

**Read this**: When checking alignment or referencing company priorities

### [EMPLOYEE_REFERENCE.md](EMPLOYEE_REFERENCE.md)
Team directory:
- All employees with IDs
- Titles and departments
- Reporting structure (who reports to whom)
- Permission levels (executive, department_head, manager, ic)

**Read this**: When identifying users, their managers, or departments

### [DATA_STRUCTURES.md](DATA_STRUCTURES.md)
Data schemas and formats:
- JSON structure for company/department/individual goals
- Outcome format with quarterly targets
- Progress update schema
- Status calculation logic
- Data relationships and IDs

**Read this**: When building features or working with data

### [COACHING_INSTRUCTIONS.md](COACHING_INSTRUCTIONS.md)
Goal-setting guidance:
- Coaching flow for department heads
- Coaching flow for individual contributors
- Questions to ask users
- Validation checklist
- Examples of good vs bad goals

**Read this**: When guiding users through goal-setting

## Usage in Code

Frontend and backend code should reference these files for:
- Business rule validation
- User permission checks
- Goal alignment verification
- Status calculation
- Coaching prompts

## Related Resources

- **Technical Docs**: See [docs/](../docs/) directory
- **AI Assistant Instructions**: See [CLAUDE.md](../CLAUDE.md)
- **Current Status**: See [CURRENT_STATE.md](../CURRENT_STATE.md)

## Maintaining These Files

These files represent the source of truth for business rules. When updating:
1. Keep them in sync with actual implementation
2. Update [CLAUDE.md](../CLAUDE.md) if business rules change
3. Test that changes don't break existing features
4. Communicate changes to the team
