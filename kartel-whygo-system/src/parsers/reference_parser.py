"""
Reference Data Parser

Parses employee and department reference data from markdown
"""

import re
from typing import List
from ..models.whygo import Person, Department
from ..utils.id_generator import generate_person_id, generate_department_id


def parse_employees_from_reference(file_path: str) -> List[Person]:
    """
    Parse employee data from EMPLOYEE_REFERENCE.md

    Returns: List of Person objects
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    employees = []

    # Find the "Employee Detail Reference" section
    section_match = re.search(r'## Employee Detail Reference(.+)', content, re.DOTALL)
    if not section_match:
        return employees

    detail_section = section_match.group(1)

    # Parse each employee entry (marked by ### Name)
    employee_blocks = re.findall(r'### (.+?)\n(.+?)(?=###|\Z)', detail_section, re.DOTALL)

    for name, details in employee_blocks:
        name = name.strip()

        # Extract fields
        title_match = re.search(r'-\s*\*\*Title:\*\*\s*(.+)', details)
        dept_match = re.search(r'-\s*\*\*Department:\*\*\s*(.+)', details)
        reports_match = re.search(r'-\s*\*\*Reports To:\*\*\s*(.+)', details)
        level_match = re.search(r'-\s*\*\*Level:\*\*\s*(.+)', details)
        emp_type_match = re.search(r'-\s*\*\*Employment Type:\*\*\s*(.+)', details)
        status_match = re.search(r'-\s*\*\*Employment Type:\*\*\s*(.+)', details)

        if not all([title_match, dept_match, level_match]):
            continue  # Skip if missing critical fields

        title = title_match.group(1).strip()
        department = dept_match.group(1).strip()
        reports_to = reports_match.group(1).strip() if reports_match else None
        level = level_match.group(1).strip().lower()
        emp_type = emp_type_match.group(1).strip() if emp_type_match else "w2"

        # Normalize employment type
        emp_type_normalized = normalize_employment_type(emp_type)

        # Normalize level
        level_normalized = normalize_level(level)

        # Generate IDs
        person_id = generate_person_id(name)
        dept_id = generate_department_id(department)
        manager_id = generate_person_id(reports_to) if reports_to and reports_to.lower() != 'board' else None

        # Determine status
        status = 'trial' if 'trial' in emp_type.lower() else 'active'

        employee = Person(
            id=person_id,
            name=name,
            title=title,
            department_id=dept_id,
            manager_id=manager_id,
            level=level_normalized,
            employment_type=emp_type_normalized,
            status=status
        )

        employees.append(employee)

    return employees


def parse_departments() -> List[Department]:
    """
    Create department reference data based on known structure

    This uses the hardcoded department structure from DATA_STRUCTURES.md
    """
    departments = [
        Department(
            id="dept_sales",
            name="Sales",
            head_id=generate_person_id("Ben Kusin"),
            primary_company_goal_ids=["cg_1_pmf"],
            secondary_company_goal_ids=["cg_2_ops"],
            reports_to=generate_person_id("Kevin Reilly")
        ),
        Department(
            id="dept_production",
            name="Production",
            head_id=generate_person_id("Wayan Palmieri"),
            primary_company_goal_ids=["cg_2_ops"],
            secondary_company_goal_ids=["cg_1_pmf"],
            reports_to=generate_person_id("Luke Peterson")
        ),
        Department(
            id="dept_generative",
            name="Generative Engineering",
            head_id=generate_person_id("Fill Isgro"),
            primary_company_goal_ids=["cg_2_ops"],
            secondary_company_goal_ids=["cg_3_talent", "cg_4_platform"],
            reports_to=generate_person_id("Luke Peterson")
        ),
        Department(
            id="dept_community",
            name="Community & Partnerships",
            head_id=generate_person_id("Daniel Kalotov"),
            primary_company_goal_ids=["cg_3_talent"],
            secondary_company_goal_ids=["cg_1_pmf"],
            reports_to=generate_person_id("Luke Peterson")
        ),
        Department(
            id="dept_platform",
            name="Platform Engineering",
            head_id=generate_person_id("Niels Hoffmann"),
            primary_company_goal_ids=["cg_4_platform"],
            secondary_company_goal_ids=["cg_2_ops"],
            reports_to=generate_person_id("Luke Peterson")
        )
    ]

    return departments


def normalize_employment_type(emp_type: str) -> str:
    """Normalize employment type to schema values"""
    emp_lower = emp_type.lower()

    if 'w2' in emp_lower or 'w-2' in emp_lower:
        return 'w2'
    elif 'contractor' in emp_lower:
        if 'international' in emp_lower:
            return 'international'
        return 'contractor'
    elif 'trial' in emp_lower:
        return 'trial'
    else:
        return 'w2'


def normalize_level(level: str) -> str:
    """Normalize level to schema values"""
    level_lower = level.lower()

    if 'executive' in level_lower or 'ceo' in level_lower or 'cfo' in level_lower or 'president' in level_lower:
        return 'executive'
    elif 'department' in level_lower or 'head' in level_lower or 'svp' in level_lower or 'cto' in level_lower or 'cro' in level_lower:
        return 'department_head'
    elif 'manager' in level_lower or 'director' in level_lower:
        return 'manager'
    else:
        return 'ic'
