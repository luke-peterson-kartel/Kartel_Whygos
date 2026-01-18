"""
Script to add email addresses to employees.json

Generates emails in format: firstname.lastname@kartelai.com
"""

import json
from pathlib import Path


def name_to_email(name: str) -> str:
    """Convert 'First Last' to 'first.last@kartelai.com'"""
    parts = name.lower().split()
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}@kartelai.com"
    else:
        return f"{parts[0]}@kartelai.com"


def main():
    # Load employees data
    data_dir = Path("data")
    employees_file = data_dir / "employees.json"

    with open(employees_file, 'r') as f:
        data = json.load(f)

    # Add email and onboarding fields to each employee
    for employee in data["employees"]:
        if "email" not in employee or not employee["email"]:
            employee["email"] = name_to_email(employee["name"])

        # Add onboarding fields with defaults
        if "onboarding_status" not in employee:
            employee["onboarding_status"] = "not_started"
        if "onboarding_started_at" not in employee:
            employee["onboarding_started_at"] = None
        if "onboarding_completed_at" not in employee:
            employee["onboarding_completed_at"] = None
        if "last_login" not in employee:
            employee["last_login"] = None
        if "timezone" not in employee:
            employee["timezone"] = "America/New_York"
        if "notification_enabled" not in employee:
            employee["notification_enabled"] = True

    # Update metadata
    from datetime import datetime
    data["metadata"]["last_updated"] = datetime.now().isoformat()

    # Write back
    with open(employees_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Added emails and onboarding fields to {len(data['employees'])} employees")
    print("\nSample emails generated:")
    for emp in data["employees"][:5]:
        print(f"  {emp['name']:25} → {emp['email']}")


if __name__ == "__main__":
    main()
