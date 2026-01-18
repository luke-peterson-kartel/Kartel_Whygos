"""
Company WhyGO Parser

Parses Company WhyGOs from markdown files
"""

import re
from typing import List
from ..models.whygo import CompanyWhyGO, Outcome
from ..utils.id_generator import generate_company_goal_id, generate_outcome_id, generate_person_id, extract_owner_name
from .markdown_parser import (
    extract_section,
    extract_table_section,
    parse_markdown_table,
    extract_why_goal_from_table,
    normalize_value,
    extract_status_field
)


def parse_company_whygos(file_path: str) -> List[CompanyWhyGO]:
    """
    Parse all Company WhyGOs from the markdown file

    Returns: List of CompanyWhyGO objects
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    whygos = []

    # Find all WhyGO sections (should be 4)
    for whygo_num in range(1, 5):  # Company has 4 WhyGOs
        whygo = parse_single_company_whygo(content, whygo_num)
        if whygo:
            whygos.append(whygo)

    return whygos


def parse_single_company_whygo(content: str, whygo_number: int) -> CompanyWhyGO:
    """
    Parse a single Company WhyGO section

    Args:
        content: Full markdown content
        whygo_number: WhyGO number (1-4)

    Returns: CompanyWhyGO object or None
    """
    # Extract the WhyGO section
    section_pattern = rf'## WhyGO #{whygo_number}:'
    next_section = rf'## WhyGO #{whygo_number + 1}:' if whygo_number < 4 else r'## Tracking & Governance'

    section_content = extract_section(content, section_pattern, next_section)

    if not section_content:
        return None

    # Extract WHY - company format uses: | WHY | text |
    why_match = re.search(r'\|\s*WHY\s*\|\s*([^\|]+)\|', section_content, re.IGNORECASE)
    if why_match:
        why_text = why_match.group(1).strip()
    else:
        why_text = extract_why_goal_from_table(section_content, 'WHY')
        if not why_text:
            # Try alternate format
            why_match = re.search(r'### WHY\s*\n\n([^\n#]+)', section_content, re.DOTALL)
            if why_match:
                why_text = why_match.group(1).strip()

    # Extract GOAL - company format uses: | GOAL | text |
    goal_match = re.search(r'\|\s*GOAL\s*\|\s*([^\|]+)\|', section_content, re.IGNORECASE)
    if goal_match:
        goal_text = goal_match.group(1).strip()
    else:
        goal_text = extract_why_goal_from_table(section_content, 'GOAL')
        if not goal_text:
            # Try alternate format
            goal_match = re.search(r'### GOAL\s*\n\n([^\n#]+)', section_content, re.DOTALL)
            if goal_match:
                goal_text = goal_match.group(1).strip()

    # Generate ID - use simple format to match department references
    # Departments reference as "cg_1", "cg_2", etc.
    goal_id = f"cg_{whygo_number}"

    # Parse outcomes table
    outcomes = parse_company_outcomes(section_content, goal_id)

    # Extract status from overall document
    status = extract_status_field(content)

    # Company WhyGOs are owned by CEO
    owner_id = generate_person_id("Kevin Reilly")

    return CompanyWhyGO(
        id=goal_id,
        why=why_text or "",
        goal=goal_text or "",
        status=status,
        owner_id=owner_id,
        fiscal_year=2026,
        outcomes=outcomes
    )


def parse_company_outcomes(section_content: str, goal_id: str) -> List[Outcome]:
    """
    Parse outcomes table from a Company WhyGO section

    Expected table format:
    | # | Outcome | Annual | Q1 | Q2 | Q3 | Q4 | Owner |
    """
    # Extract outcomes table
    table_text = extract_table_section(section_content, r'### OUTCOMES|OUTCOMES')

    if not table_text:
        return []

    rows = parse_markdown_table(table_text)
    outcomes = []

    for idx, row in enumerate(rows, 1):
        # Get outcome description
        description = row.get('Outcome', row.get('outcome', ''))

        # Get owner
        owner_name = row.get('Owner', row.get('owner', ''))
        owner_full_name = extract_owner_name(owner_name)
        owner_id = generate_person_id(owner_full_name)

        # Get targets
        annual = normalize_value(row.get('Annual', row.get('annual', '')))
        q1 = normalize_value(row.get('Q1', ''))
        q2 = normalize_value(row.get('Q2', ''))
        q3 = normalize_value(row.get('Q3', ''))
        q4 = normalize_value(row.get('Q4', ''))

        # Determine metric type based on description and values
        metric_type = infer_metric_type(description, annual, q1, q2, q3, q4)

        outcome = Outcome(
            id=generate_outcome_id(goal_id, idx),
            goal_id=goal_id,
            description=description,
            metric_type=metric_type,
            owner_id=owner_id,
            target_annual=annual,
            target_q1=q1,
            target_q2=q2,
            target_q3=q3,
            target_q4=q4
        )

        outcomes.append(outcome)

    return outcomes


def infer_metric_type(description: str, *values) -> str:
    """
    Infer metric type from description and values

    Returns: 'number', 'percentage', 'currency', 'boolean', or 'milestone'
    """
    desc_lower = description.lower()

    # Check for percentages
    if '%' in description or 'rate' in desc_lower or 'margin' in desc_lower:
        return 'percentage'

    # Check for currency
    if '$' in description or 'revenue' in desc_lower or 'cost' in desc_lower:
        return 'currency'

    # Check for milestones (text-based targets like "MVP", "Live", "Done")
    for val in values:
        if val and isinstance(val, str) and not val.replace('.', '').replace('-', '').isdigit():
            if val.lower() in ['mvp', 'live', 'spec', 'done', 'baseline', 'iterate']:
                return 'milestone'

    # Check for boolean (yes/no)
    if 'completed' in desc_lower or 'delivered' in desc_lower:
        return 'boolean'

    # Default to number
    return 'number'
