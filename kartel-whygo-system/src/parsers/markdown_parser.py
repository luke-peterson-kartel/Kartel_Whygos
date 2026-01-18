"""
Markdown Parser Utilities

Core utilities for parsing markdown WhyGO documents
"""

import re
from typing import List, Dict, Optional, Tuple


def parse_markdown_table(table_text: str) -> List[Dict[str, str]]:
    """
    Parse a markdown table into a list of dictionaries

    Example input:
    | Outcome | Q1 | Q2 | Q3 | Q4 | Owner |
    | --- | --- | --- | --- | --- | --- |
    | Clients signed | 4 | 10 | 14 | 18+ | Ben |

    Returns: [{"Outcome": "Clients signed", "Q1": "4", "Q2": "10", ...}]
    """
    lines = [line.strip() for line in table_text.strip().split('\n') if line.strip()]

    if len(lines) < 2:
        return []

    # Parse header row
    header_line = lines[0]
    headers = [h.strip() for h in header_line.split('|') if h.strip()]

    # Skip separator line (the one with --- )
    data_lines = [l for l in lines[2:] if '---' not in l]

    # Parse data rows
    rows = []
    for line in data_lines:
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) >= len(headers):
            row = {headers[i]: cells[i] for i in range(len(headers))}
            rows.append(row)

    return rows


def extract_section(content: str, section_pattern: str, end_pattern: Optional[str] = None) -> Optional[str]:
    """
    Extract content between section markers

    Args:
        content: Full markdown content
        section_pattern: Regex pattern for section start (e.g., r'## WhyGO #1')
        end_pattern: Optional regex pattern for section end (e.g., r'## WhyGO #2' or r'## Addendum')

    Returns: Content between start and end patterns, or None if not found
    """
    match = re.search(section_pattern, content, re.IGNORECASE | re.MULTILINE)
    if not match:
        return None

    start_pos = match.end()

    if end_pattern:
        end_match = re.search(end_pattern, content[start_pos:], re.IGNORECASE | re.MULTILINE)
        if end_match:
            end_pos = start_pos + end_match.start()
            return content[start_pos:end_pos].strip()

    return content[start_pos:].strip()


def extract_table_section(content: str, before_pattern: str) -> Optional[str]:
    """
    Extract markdown table that appears after a specific pattern

    Args:
        content: Full markdown content
        before_pattern: Pattern that appears before the table (e.g., "### OUTCOMES" or "OUTCOMES")

    Returns: The markdown table text, or None if not found
    """
    # Find the pattern
    match = re.search(before_pattern, content, re.IGNORECASE | re.MULTILINE)
    if not match:
        return None

    # Start looking for table after the pattern
    content_after = content[match.end():]

    # Find the start of the table (first line with |)
    table_start = None
    for i, char in enumerate(content_after):
        if char == '|':
            table_start = i
            break

    if table_start is None:
        return None

    # Find the end of the table (first empty line or next heading)
    lines = content_after[table_start:].split('\n')
    table_lines = []

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            break
        if line_stripped.startswith('#'):
            break
        if '|' in line_stripped:
            table_lines.append(line)
        elif table_lines:  # Stop if we've started collecting and hit non-table line
            break

    if not table_lines:
        return None

    return '\n'.join(table_lines)


def extract_text_between_markers(content: str, start_marker: str, end_marker: str) -> Optional[str]:
    """
    Extract text between two markers

    Example: Extract WHY text from markdown table cell:
    | WHY
    This is the why text... |
    """
    # Try to find start marker
    start_idx = content.find(start_marker)
    if start_idx == -1:
        return None

    start_idx += len(start_marker)

    # Try to find end marker
    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        # If no end marker, take rest of content
        return content[start_idx:].strip()

    return content[start_idx:end_idx].strip()


def extract_why_goal_from_table(content: str, keyword: str) -> Optional[str]:
    """
    Extract WHY or GOAL text from markdown table format

    Example format:
    | WHY
    Enterprise clients require... |
    | --- |

    or:
    | GOAL
    Onboard 10 enterprise clients... |
    | --- |
    """
    # Pattern: | KEYWORD followed by text until next |
    pattern = rf'\|\s*{keyword}\s*\n([^\|]+)\|'
    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)

    if match:
        return match.group(1).strip()

    # Alternative pattern: | KEYWORD | on separate line, then text
    # This handles cases where WHY is in a header cell
    pattern2 = rf'\|\s*{keyword}\s*\|.*?\n\|\s*---\s*\|.*?\n\|\s*([^\|]+)\|'
    match2 = re.search(pattern2, content, re.IGNORECASE | re.DOTALL)

    if match2:
        return match2.group(1).strip()

    return None


def parse_alignment_table(content: str) -> Dict[str, List[str]]:
    """
    Parse the "Company WhyGO Alignment" table from department docs

    Example:
    | Department WhyGO | Ladders To | Connection |
    | #1: Land Clients | Company #1 (PMF) | Primary |

    Returns: {"dept_goal_1": ["cg_1_pmf"], ...}
    """
    # Find the alignment table
    table_text = extract_table_section(content, r'(Company WhyGO Alignment|Alignment)')

    if not table_text:
        return {}

    rows = parse_markdown_table(table_text)
    alignment = {}

    for row in rows:
        # Get department WhyGO number from first column
        dept_whygo = row.get('Department WhyGO', '')
        match = re.search(r'#(\d+)', dept_whygo)
        if not match:
            continue

        dept_goal_num = int(match.group(1))

        # Get company goal references from "Ladders To" column
        ladders_to = row.get('Ladders To', '')
        company_goals = []

        # Find all company goal references (e.g., "#1", "Company #2", etc.)
        for comp_match in re.finditer(r'#(\d+)', ladders_to):
            company_goals.append(f"cg_{comp_match.group(1)}")

        if company_goals:
            alignment[f"dept_goal_{dept_goal_num}"] = company_goals

    return alignment


def normalize_value(value: str) -> Optional[any]:
    """
    Normalize table cell values

    - "Baseline" -> None
    - "—" or "TBD" -> None
    - Numeric strings -> try to convert to int/float
    - Keep other strings as-is
    """
    value = value.strip()

    # Handle baseline/TBD/empty markers
    if value.lower() in ['baseline', 'tbd', '—', '-', '']:
        return None

    # Try to parse as number
    # Remove common suffixes like "+" or "M" or "%"
    clean_value = re.sub(r'[+%$]', '', value).strip()

    # Handle "18+" format
    if clean_value.endswith('+'):
        clean_value = clean_value[:-1]

    # Handle "$7M" format
    if 'M' in clean_value or 'm' in clean_value:
        clean_value = re.sub(r'[Mm]', '', clean_value)
        try:
            return float(clean_value) * 1_000_000
        except:
            pass

    # Try int
    try:
        if '.' not in clean_value:
            return int(clean_value)
    except:
        pass

    # Try float
    try:
        return float(clean_value)
    except:
        pass

    # Return original value if can't parse
    return value


def extract_status_field(content: str) -> str:
    """
    Extract status from markdown header table

    Example:
    | Status | APPROVED - Ready for Team Cascade |
    """
    pattern = r'\|\s*Status\s*\|\s*([^\|]+)\|'
    match = re.search(pattern, content, re.IGNORECASE)

    if match:
        status_text = match.group(1).strip().lower()
        if 'approved' in status_text:
            return 'approved'
        elif 'draft' in status_text or 'pending' in status_text:
            return 'draft'

    return 'draft'


def extract_department_name(content: str) -> Optional[str]:
    """
    Extract department name from header

    Example: "Sales Department" or "Community & Partnerships Department"
    """
    # Try to find in table format first
    pattern = r'\|\s*Department\s*\|\s*([^\|]+)\|'
    match = re.search(pattern, content, re.IGNORECASE)

    if match:
        return match.group(1).strip()

    # Try heading format
    pattern2 = r'^(.+?)\s+Department'
    match2 = re.search(pattern2, content, re.MULTILINE | re.IGNORECASE)

    if match2:
        return match2.group(1).strip()

    return None
