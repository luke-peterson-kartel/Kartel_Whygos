"""
Department WhyGO Parser

Parses Department WhyGOs from markdown files
"""

import re
from typing import List
from ..models.whygo import DepartmentWhyGO, Outcome
from ..utils.id_generator import (
    generate_department_goal_id,
    generate_outcome_id,
    generate_person_id,
    generate_department_id,
    extract_owner_name
)
from .markdown_parser import (
    extract_section,
    extract_table_section,
    parse_markdown_table,
    extract_why_goal_from_table,
    normalize_value,
    extract_status_field,
    extract_department_name,
    parse_alignment_table
)
from .company_parser import infer_metric_type


def parse_department_whygos(file_path: str) -> List[DepartmentWhyGO]:
    """
    Parse all Department WhyGOs from a markdown file

    Returns: List of DepartmentWhyGO objects
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract department name
    dept_name = extract_department_name(content)
    if not dept_name:
        print(f"Warning: Could not extract department name from {file_path}")
        return []

    dept_id = generate_department_id(dept_name)

    # Extract alignment table to map which department goals ladder to which company goals
    alignment_map = parse_alignment_table(content)

    # Extract status
    status = extract_status_field(content)

    whygos = []

    # Find all WhyGO sections (typically 2-3 per department)
    for whygo_num in range(1, 5):  # Check up to 4 WhyGOs
        whygo = parse_single_department_whygo(
            content,
            whygo_num,
            dept_name,
            dept_id,
            alignment_map,
            status
        )
        if whygo:
            whygos.append(whygo)

    return whygos


def parse_single_department_whygo(
    content: str,
    whygo_number: int,
    dept_name: str,
    dept_id: str,
    alignment_map: dict,
    status: str
) -> DepartmentWhyGO:
    """
    Parse a single Department WhyGO section

    Args:
        content: Full markdown content
        whygo_number: WhyGO number (1-3)
        dept_name: Department name (e.g., "Sales", "Production")
        dept_id: Department ID (e.g., "dept_sales")
        alignment_map: Mapping of department goals to company goals
        status: Status from markdown

    Returns: DepartmentWhyGO object or None
    """
    # Extract the WhyGO section
    section_pattern = rf'# WhyGO #{whygo_number}:|## WhyGO #{whygo_number}:'
    next_section = rf'# WhyGO #{whygo_number + 1}:|## WhyGO #{whygo_number + 1}:|# Addendum|## Addendum'

    section_content = extract_section(content, section_pattern, next_section)

    if not section_content:
        return None

    # Extract WHY
    why_text = extract_why_goal_from_table(section_content, 'WHY')
    if not why_text:
        # Try alternate format
        why_match = re.search(r'(WHY|Why)\s*\n\n([^\n#]+)', section_content, re.DOTALL)
        if why_match:
            why_text = why_match.group(2).strip()

    # Extract GOAL
    goal_text = extract_why_goal_from_table(section_content, 'GOAL')
    if not goal_text:
        # Try alternate format
        goal_match = re.search(r'(GOAL|Goal)\s*\n\n([^\n#]+)', section_content, re.DOTALL)
        if goal_match:
            goal_text = goal_match.group(2).strip()

    if not goal_text:
        return None  # Can't create a goal without goal text

    # Generate ID
    goal_id = generate_department_goal_id(dept_name, whygo_number)

    # Get parent goal IDs from alignment map
    parent_goal_ids = alignment_map.get(f"dept_goal_{whygo_number}", [])

    # If alignment map didn't work, try to extract from "Ladders To" section
    if not parent_goal_ids:
        parent_goal_ids = extract_parent_goals_from_section(section_content)

    # Parse outcomes table
    outcomes = parse_department_outcomes(section_content, goal_id, dept_name)

    return DepartmentWhyGO(
        id=goal_id,
        department_id=dept_id,
        parent_goal_ids=parent_goal_ids,
        why=why_text or "",
        goal=goal_text or "",
        status=status,
        approved_by=None,  # Can be set later
        fiscal_year=2026,
        outcomes=outcomes
    )


def parse_department_outcomes(section_content: str, goal_id: str, dept_name: str) -> List[Outcome]:
    """
    Parse outcomes table from a Department WhyGO section

    Expected table format:
    | Outcome | Q1 | Q2 | Q3 | Q4 | Owner |
    """
    # Extract outcomes table
    table_text = extract_table_section(section_content, r'### OUTCOMES|## OUTCOMES|OUTCOMES')

    if not table_text:
        return []

    rows = parse_markdown_table(table_text)
    outcomes = []

    for idx, row in enumerate(rows, 1):
        # Get outcome description
        description = row.get('Outcome', row.get('outcome', ''))

        if not description:
            continue

        # Get owner
        owner_name = row.get('Owner', row.get('owner', ''))
        if not owner_name:
            # Default to department name if no owner specified
            owner_name = dept_name

        owner_full_name = extract_owner_name(owner_name)
        owner_id = generate_person_id(owner_full_name)

        # Get targets
        annual = row.get('Q4 (Annual)', row.get('Annual', row.get('Q4', '')))
        annual = normalize_value(annual) if annual else None

        q1 = normalize_value(row.get('Q1', ''))
        q2 = normalize_value(row.get('Q2', ''))
        q3 = normalize_value(row.get('Q3', ''))
        q4 = normalize_value(row.get('Q4', ''))

        # If annual not set but Q4 is, use Q4 as annual
        if annual is None and q4 is not None:
            annual = q4

        # Determine metric type
        metric_type = infer_metric_type(description, annual, q1, q2, q3, q4)

        outcome = Outcome(
            id=generate_outcome_id(goal_id, idx),
            goal_id=goal_id,
            description=description,
            metric_type=metric_type,
            owner_id=owner_id,
            target_annual=annual if annual is not None else q4,
            target_q1=q1,
            target_q2=q2,
            target_q3=q3,
            target_q4=q4
        )

        outcomes.append(outcome)

    return outcomes


def extract_parent_goals_from_section(section_content: str) -> List[str]:
    """
    Extract parent company goal IDs from the section content

    Looks for patterns like:
    - "Ladders To: Company #1"
    - "Company WhyGO #2"
    - References to "Company Goal #3"
    """
    parent_goals = []

    # Find all company goal references
    matches = re.finditer(r'Company\s+(?:WhyGO\s+)?#(\d+)', section_content, re.IGNORECASE)

    for match in matches:
        goal_num = int(match.group(1))
        goal_id = f"cg_{goal_num}"
        if goal_id not in parent_goals:
            parent_goals.append(goal_id)

    return parent_goals
