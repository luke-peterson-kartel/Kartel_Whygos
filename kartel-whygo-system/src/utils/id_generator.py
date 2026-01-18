"""
ID Generator

Generates consistent semantic IDs for WhyGO entities
"""

import re


def generate_company_goal_id(goal_number: int, goal_text: str) -> str:
    """
    Generate company goal ID
    Example: cg_1_pmf (company goal 1 - product market fit)
    """
    # Extract key words from goal
    key_words = extract_key_words(goal_text)
    return f"cg_{goal_number}_{key_words}"


def generate_department_goal_id(department_name: str, goal_number: int) -> str:
    """
    Generate department goal ID
    Example: dept_sales_1, dept_generative_2
    """
    dept_slug = department_name.lower().replace(' ', '_').replace('&', 'and')
    return f"dept_{dept_slug}_{goal_number}"


def generate_individual_goal_id(person_name: str, goal_number: int) -> str:
    """
    Generate individual goal ID
    Example: ig_wayan_1, ig_ben_2
    """
    first_name = person_name.split()[0].lower()
    return f"ig_{first_name}_{goal_number}"


def generate_outcome_id(goal_id: str, outcome_number: int) -> str:
    """
    Generate outcome ID
    Example: cg_1_pmf_o1, dept_sales_1_o2
    """
    return f"{goal_id}_o{outcome_number}"


def generate_person_id(person_name: str) -> str:
    """
    Generate person ID
    Example: person_kevin_reilly, person_ben_kusin
    """
    name_slug = person_name.lower().replace(' ', '_')
    return f"person_{name_slug}"


def generate_department_id(department_name: str) -> str:
    """
    Generate department ID
    Example: dept_sales, dept_platform, dept_community
    """
    dept_slug = department_name.lower().replace(' ', '_').replace('&', 'and')
    # Simplify long names
    if 'community' in dept_slug and 'partnership' in dept_slug:
        dept_slug = 'community'
    elif 'generative' in dept_slug or 'engineering' in dept_slug:
        if 'generative' in dept_slug:
            dept_slug = 'generative'

    return f"dept_{dept_slug}"


def extract_key_words(text: str, max_words: int = 3) -> str:
    """
    Extract key words from goal text to create semantic ID suffix

    Examples:
    - "Prove Product-Market Fit" -> "pmf"
    - "Build Operational Excellence" -> "ops"
    - "Build the Talent Engine" -> "talent"
    - "Deploy Enterprise Platform" -> "platform"
    """
    # Predefined mappings for known goals
    mappings = {
        'product-market fit': 'pmf',
        'product market fit': 'pmf',
        'prove product': 'pmf',
        'operational excellence': 'ops',
        'build operational': 'ops',
        'talent engine': 'talent',
        'build the talent': 'talent',
        'build talent': 'talent',
        'enterprise platform': 'platform',
        'deploy enterprise': 'platform',
    }

    text_lower = text.lower()

    # Check for known mappings
    for phrase, abbreviation in mappings.items():
        if phrase in text_lower:
            return abbreviation

    # Extract significant words (remove common words)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    words = re.findall(r'\b\w+\b', text_lower)
    significant_words = [w for w in words if w not in stop_words and len(w) > 2]

    # Take first max_words significant words
    key_words = '_'.join(significant_words[:max_words])

    return key_words if key_words else 'goal'


def generate_progress_update_id(outcome_id: str, quarter: str) -> str:
    """
    Generate progress update ID
    Example: cg_1_o1_q1_update_20260117
    """
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    quarter_lower = quarter.lower()
    return f"{outcome_id}_{quarter_lower}_update_{timestamp}"


def extract_owner_name(text: str) -> str:
    """
    Extract owner name from various formats in markdown
    Examples:
    - "Ben" -> "Ben Kusin"
    - "Kevin" -> "Kevin Reilly"
    - "Fill" -> "Fill Isgro"
    """
    # Common name mappings from the team
    name_mappings = {
        'ben': 'Ben Kusin',
        'kevin': 'Kevin Reilly',
        'luke': 'Luke Peterson',
        'wayan': 'Wayan Palmieri',
        'fill': 'Fill Isgro',
        'daniel': 'Daniel Kalotov',
        'niels': 'Niels Hoffmann',
        'emmet': 'Emmet Reilly',
        'veronica': 'Veronica Diaz',
        'estefania': 'Estefania Guarderas',
        'jason': 'Jason Goldwatch',
        'noah': 'Noah Shields',
        'brandon': 'Brandon Valedez',
        'sean': 'Sean Geisterfer',
        'trent': 'Trent Hunter',
        'elliot': 'Elliot Quartz',
        'marc': 'Marc Donhue',
        'ahmed': 'Ahmed Yakout',
        'matthias': 'Matthias Thoemmes',
        'lukas': 'Lukas Motiejunas',
        'zac': 'Zac Bagley',
        'jerry': 'Jerry Bellman',
        'marketing': 'Marketing',
        'ops lead': 'Ops Lead',
        'community': 'Daniel Kalotov',
        'platform': 'Niels Hoffmann',
        'sales': 'Ben Kusin',
        'production': 'Wayan Palmieri',
        'generative': 'Fill Isgro'
    }

    text_lower = text.strip().lower()

    # Direct lookup
    if text_lower in name_mappings:
        return name_mappings[text_lower]

    # Return as-is if not found (may need manual correction)
    return text.strip()
