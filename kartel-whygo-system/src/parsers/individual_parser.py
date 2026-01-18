"""
Individual WhyGO Parser

Parses Individual WhyGOs from markdown files
"""

import re
from typing import List
from ..models.whygo import IndividualWhyGO, Outcome
from ..utils.id_generator import (
    generate_individual_goal_id,
    generate_outcome_id,
    generate_person_id,
    extract_owner_name
)
from .markdown_parser import (
    extract_section,
    extract_table_section,
    parse_markdown_table,
    extract_why_goal_from_table,
    normalize_value,
    extract_status_field
)
from .company_parser import infer_metric_type


def parse_individual_whygos(file_path: str, person_name: str) -> List[IndividualWhyGO]:
    """
    Parse all Individual WhyGOs from a markdown file

    Args:
        file_path: Path to markdown file
        person_name: Name of the person (e.g., "Wayan Palmieri")

    Returns: List of IndividualWhyGO objects
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract status
    status = extract_status_field(content)

    whygos = []

    # Find all WhyGO sections (typically 2-3)
    for whygo_num in range(1, 5):
        whygo = parse_single_individual_whygo(
            content,
            whygo_num,
            person_name,
            status
        )
        if whygo:
            whygos.append(whygo)

    return whygos


def parse_single_individual_whygo(
    content: str,
    whygo_number: int,
    person_name: str,
    status: str
) -> IndividualWhyGO:
    """
    Parse a single Individual WhyGO section

    Args:
        content: Full markdown content
        whygo_number: WhyGO number (1-3)
        person_name: Person's name
        status: Status from markdown

    Returns: IndividualWhyGO object or None
    """
    # Extract the WhyGO section
    section_pattern = rf'# Individual WhyGO #{whygo_number}:|## Individual WhyGO #{whygo_number}:'
    next_section = rf'# Individual WhyGO #{whygo_number + 1}:|## Individual WhyGO #{whygo_number + 1}:|# Addendum|## Addendum|—\s*End'

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
        return None

    # Generate ID
    goal_id = generate_individual_goal_id(person_name, whygo_number)

    # Generate person ID
    person_id = generate_person_id(person_name)

    # Extract parent goal IDs (Department WhyGOs)
    parent_goal_ids = extract_parent_department_goals(section_content)

    # Parse outcomes table
    outcomes = parse_individual_outcomes(section_content, goal_id, person_name)

    return IndividualWhyGO(
        id=goal_id,
        person_id=person_id,
        parent_goal_ids=parent_goal_ids,
        why=why_text or "",
        goal=goal_text or "",
        status=status,
        approved_by=None,
        fiscal_year=2026,
        outcomes=outcomes
    )


def parse_individual_outcomes(section_content: str, goal_id: str, person_name: str) -> List[Outcome]:
    """
    Parse outcomes table from an Individual WhyGO section

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

        # Get owner - for individual goals, usually the person themselves
        owner_name = row.get('Owner', row.get('owner', person_name))
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


def extract_parent_department_goals(section_content: str) -> List[str]:
    """
    Extract parent department goal IDs from the section content

    Looks for patterns like:
    - "Ladders To: Department WhyGO #1"
    - "Production WhyGO #2"
    """
    parent_goals = []

    # This is tricky without knowing the department
    # For now, look for any mentions of department goal numbers
    # In practice, this would be set based on the person's department

    # Find patterns like "Department WhyGO #1" or "Production WhyGO #1"
    matches = re.finditer(r'(?:Department|Production|Sales|Generative|Community|Platform)\s+WhyGO\s+#(\d+)', section_content, re.IGNORECASE)

    for match in matches:
        goal_num = int(match.group(1))
        # Can't determine exact ID without knowing department
        # This will need to be filled in by the import script based on person's department
        parent_goals.append(f"dept_unknown_{goal_num}")

    return parent_goals
