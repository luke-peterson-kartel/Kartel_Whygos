# Implementation Plan: Phase 3 - Slack Integration & User Workflows

## Summary

Build Slack bot integration with automated reminders, natural language progress updates, and role-based dashboards. Focus on user adoption through seamless workflows that meet people where they already work (Slack).

**Phase 1**: ✅ COMPLETE - Data parser, 74 outcomes imported
**Phase 2**: ✅ COMPLETE - Progress tracking with repository pattern, CLI tools
**Phase 3**: 🚧 THIS PLAN - Slack integration for team adoption

## User Research Results

✅ **User flows refined based on 8 clarifying questions** (Jan 2026)

**Personas:**
- Leadership (Kevin, Luke, Ben) - High-level company tracking
- Department Heads (Wayan, Fill, Daniel, Niels) - Team management
- Individual Contributors - Personal outcome tracking

**Preferences:**
- **Cadence**: Weekly updates (Monday 9:00am sharp)
- **Interface**: Slack DMs with natural language
- **Trigger**: Automated reminders
- **Escalation**: Notify managers after 2 missed reminders (Tue→Wed→Thu escalation)
- **Summary Timing**: Leadership dashboard at 9:30am regardless of completion rate

**Leadership Needs:**
- Company-wide status (X/74 on pace)
- Change alerts (what moved this week)
- Active blockers with names (transparency)
- Department rollups

**UX Refinements:**
- Absolute value parsing priority ("now at 5" = set to 5)
- Batch confirmations for multi-update messages
- Neutral & factual tone for off-pace outcomes
- Ask for clarification on ambiguous input
- Include baseline outcomes in reminders

## User Flows

### Flow 1: Weekly Update (Monday 9am)

```
Bot DM → Ben (9:00am sharp):
"Good morning! Time for your weekly WhyGO update 📊
You own 3 outcomes:
• cg_1_o1: Enterprise clients signed (Target: 4, Last: 3)
• dept_sales_2_o1: Case studies (Target: 1, Last: 0)
• ig_ben_1_o1: Pipeline ($2M target, Last: $1.8M)

Reply with updates in plain English!"

Ben replies:
"Signed 2 new clients, now at 5 total.
 Case study still in review.
 Pipeline is $2.1M - hit target!"

Bot parses and confirms (batch format):
"✅ Updates recorded:

• Clients: 5/4 [+] Ahead of target
• Case study: 0/1 [-] At 0%, target is 1
• Pipeline: $2.1M/$2M [+] Above target"
```

**Key UX Decisions:**
- **Timing**: Monday 9:00am sharp (proactive, builds habit)
- **Input Parsing**: Absolute values take precedence ("now at 5" = set to 5, not +2)
- **Confirmation**: Batch confirm all updates at end (not line-by-line)
- **Tone**: Neutral & factual for off-pace items (no "Need support?" prompts)

### Flow 2: Leadership Dashboard (Monday 9:30am)

```
Bot → #leadership channel (9:30am - after update window):
📊 **Kartel WhyGO Weekly Summary**

Company Status (Q1 2026):
✅ 45/74 on pace [+]
⚠️  18/74 slightly off [~]
🔴 6/74 off pace [-]
⚪ 5/74 not yet recorded

This Week's Changes:
• cg_1_o1: Clients → [+] (+2, now at 5)
• cg_2_o2: On-time → [~] (dropped to 82%)

Active Blockers:
• dept_sales_2_o1 (Ben Kusin): Legal approval needed
• dept_prod_1_o3 (Wayan Palmieri): Tooling blocked

Department Rollups:
🎯 Sales: 8/10 [+]
🎯 Production: 10/15 [~]
[View Full Dashboard]
```

**Key UX Decisions:**
- **Timing**: 9:30am regardless of update completion (provides snapshot of current state)
- **Transparency**: Show names with blockers (Ben Kusin, not just "Ben")
- **Language**: "Not yet recorded" for missing updates (implies still expected)
- **Scope**: Posts even if only partial updates received (leadership sees current state)

### Flow 3: Manager Escalation

```
Tuesday 9am → Reminder to owner
Wednesday 9am → Second reminder
Thursday 9am → Escalate to manager:

Bot DM → Luke:
"Hi Luke, Ben hasn't updated 3 outcomes:
• cg_1_o1: Enterprise clients
• dept_sales_2_o1: Case studies
• ig_ben_1_o1: Pipeline

Can you follow up in your 1-on-1?"
```

**Accountability** without micromanaging

### Flow 4: Department View (/whygo command)

```
User: /whygo sales

Bot (ephemeral):
📊 **Sales Department**

Goal 1: Sign 18+ spec engagements
✅ Specs signed: 5/4 [+]
⚪ Paying clients: Not recorded
✅ Revenue: $1.8M/$1.5M [+]

Goal 2: 50+ NPS, case studies
⚪ NPS: Not recorded
⚠️  Case studies: 0/1 [-] BLOCKER
🔴 Retention: 85%/90% [-]

Team: 6/10 on pace
[View All] [Check Updates]
```

**On-demand** department view for managers

### Flow 5: Ad-hoc Updates

```
Ben: "Just closed 3 more clients! We're at 8 🎉"

Bot: "Great! Which outcome is this for?
• cg_1_o1: Enterprise clients signed
• dept_sales_1_o1: Spec engagements signed"

Ben: "First one"

Bot: "✅ Updated cg_1_o1 to 8 (was 5)
[+] At 200% of target (4)

Your progress:
Week 1: 3 → Week 2: 5 → Week 3: 8 📈"
```

**Key UX Decisions:**
- **Ambiguous Input**: When unclear which outcome, ask user to clarify (show full outcome descriptions)
- **Anytime Access**: Accepts updates 24/7, not just during Monday reminder window
- **Progress Trends**: Show historical progression when updating ad-hoc

## Edge Cases & Special Handling

### Baseline Outcomes (No Quarterly Targets)

Some outcomes have "Baseline" as their Q1 target, meaning we're establishing a baseline in Q1 rather than measuring against a target.

**Example**: `cg_1_o3: Active clients post-spec (Q1 target: Baseline)`

```
Monday 9am reminder includes baseline outcomes:
"• cg_1_o3: Active clients post-spec (Target: Baseline, Last: Not recorded)"

User update:
"Active clients is 2"

Bot confirmation:
"✅ Updates recorded:
• Active clients: 2 [+] Baseline recorded"
```

**UX Decision**: Still ask for updates on baseline outcomes. They're important data points even without targets. Display status as `[+]` when baseline value is recorded.

### Ambiguous Update Parsing

When user provides a number that could apply to multiple outcomes:

```
User: "We're at 5 now"

Bot: "Which outcome is this for?
• cg_1_o1: Enterprise clients signed
• dept_sales_1_o1: Spec engagements signed
• cg_1_o3: Active clients post-spec"

User selects or replies with outcome ID/name
```

**UX Decision**: Show full outcome descriptions (not just IDs) to help user identify correct outcome.

### Multi-Update Parsing Logic

When user provides multiple updates in one message:

```
User: "Signed 2 new clients, now at 5 total. Pipeline is $2.1M"

Bot extracts:
1. "now at 5 total" → Absolute value = 5
2. "Pipeline is $2.1M" → Absolute value = $2.1M

Bot confirms (batch):
"✅ Updates recorded:
• Clients: 5/4 [+] Ahead of target
• Pipeline: $2.1M/$2M [+] Above target"
```

**Parsing Priority**:
1. Absolute values ("now at 5", "total of 5", "at 5") → Set to that value
2. Delta indicators ("+2", "2 more") → Add to last value (if absolute not found)

### Status Tone Guidelines

**For [+] On Pace:**
- "Ahead of target"
- "Above target"
- "On pace"

**For [~] Slightly Off:**
- "At 85% of target"
- "Slightly behind"

**For [-] Off Pace:**
- "At 50%, target is 10" (factual, no judgment)
- "Below target"

**Avoid**: Emotional language, questions ("Need support?"), exclamation marks for negative status

### Leadership Summary Timing

**Scenario**: Only 30% of team has updated by 9:30am Monday

**Behavior**: Still send leadership summary at 9:30am showing:
- Outcomes updated so far
- "Not yet recorded" for missing updates
- Current state of what's been submitted

**Rationale**: Leadership gets consistent timing. Missing updates visible, prompting follow-up if needed.

## Technical Architecture

```
Slack (Interface)
    ↓
Slack Bot Layer (NEW)
  - Message handler
  - NL parser
  - Reminder scheduler
  - Dashboard formatter
    ↓
Service Layer (REUSE from Phase 2)
  - ProgressService
  - WhygoService
    ↓
Repository Layer (REUSE from Phase 2)
  - JsonWhygoRepository
    ↓
JSON Files
```

**80% of logic already exists!** We're just adding Slack interface.

## Implementation Components

### 1. Slack Bot Foundation

**File:** `slack_bot/app.py`

```python
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initialize Slack app
app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Initialize existing services
whygo_repo = JsonWhygoRepository()
progress_repo = JsonProgressRepository()
progress_service = ProgressService(whygo_repo, progress_repo)
whygo_service = WhygoService(whygo_repo)
```

**Tech**: Use Slack Bolt (official Python framework)
**Auth**: Socket mode (no public endpoint needed)

### 2. Natural Language Parser

**File:** `slack_bot/nl_parser.py`

```python
class NaturalLanguageParser:
    def parse_update(self, text: str, user_outcomes: List[Outcome]) -> List[UpdateIntent]:
        """
        Parse: "Signed 2 clients, now at 5 total. Pipeline is $2.1M"

        Returns: [
            UpdateIntent(outcome_id='cg_1_o1', value=5, parsing_method='absolute'),
            UpdateIntent(outcome_id='ig_ben_1_o1', value=2100000, parsing_method='absolute')
        ]
        """
        # Parsing priority:
        # 1. Absolute values ("now at 5", "total of 5", "at 5")
        # 2. Delta values ("+2", "2 more") - only if no absolute found

        # Use regex + keyword matching
        # Match keywords to outcome descriptions
        # Ask user to clarify if ambiguous
```

**Strategy:**
- Start with regex patterns for absolute values (priority: "now at X", "total of X", "at X")
- Fall back to delta patterns ("+X", "X more") only if no absolute found
- Extract currency ($2.1M), percentages (85%), milestones ("MVP")
- Match keywords to outcome descriptions
- If multiple outcomes match or no clear match, ask user to clarify
- Return parsing_method for debugging/logging

### 3. Reminder Scheduler

**File:** `slack_bot/scheduler.py`

```python
import schedule
from datetime import datetime

def send_weekly_reminders():
    """Every Monday 9am"""
    outcomes_by_owner = get_outcomes_grouped_by_owner()

    for person_id, outcomes in outcomes_by_owner.items():
        slack_user_id = get_slack_id_for_person(person_id)
        send_update_reminder(slack_user_id, outcomes)

schedule.every().monday.at("09:00").do(send_weekly_reminders)
```

**Scheduling:**
- Monday 9am: Weekly reminders
- Monday 9:30am: Leadership summary
- Tuesday/Wednesday: Follow-up reminders
- Thursday: Manager escalation

### 4. Dashboard Formatter

**File:** `slack_bot/formatters.py`

```python
def format_leadership_summary(data: dict) -> str:
    """Format weekly summary for #leadership channel"""
    # Use Slack Block Kit for rich formatting
    # Emoji indicators
    # Interactive buttons

def format_department_view(dept_data: dict) -> str:
    """Format department dashboard"""
    # Group by goals
    # Show status indicators
    # Highlight blockers
```

**UI**: Slack Block Kit for rich, interactive messages

### 5. Message Handlers

**File:** `slack_bot/handlers.py`

```python
@app.message(".*")
def handle_dm(message, say):
    """Handle DM replies to bot"""
    user_id = message['user']
    text = message['text']

    # Get user's outcomes
    person_id = get_person_id_from_slack(user_id)
    outcomes = whygo_service.get_all_outcomes_for_person(person_id)

    # Parse natural language
    updates = nl_parser.parse_update(text, outcomes)

    # Record each update
    for update in updates:
        progress_service.record_actual(
            outcome_id=update.outcome_id,
            quarter='Q1',
            actual_value=update.value,
            recorded_by=person_id,
            notes=update.notes
        )

    # Send confirmation
    say(format_confirmation(updates))

@app.command("/whygo")
def handle_whygo_command(ack, command, respond):
    """Handle /whygo slash command"""
    ack()
    dept = command['text']
    data = whygo_service.get_department_dashboard_data(dept)
    respond(format_department_view(data))
```

### 6. User Mapping

**File:** `slack_bot/user_mapping.py`

```python
# Map Slack user IDs to person IDs
USER_MAPPING = {
    'U12345': 'person_ben_kusin',
    'U23456': 'person_kevin_reilly',
    # ... from employees.json
}

def get_slack_id_for_person(person_id: str) -> str:
    """person_ben_kusin → U12345"""

def get_person_id_from_slack(slack_id: str) -> str:
    """U12345 → person_ben_kusin"""
```

**Setup**: One-time mapping of Slack IDs to employee records

## Implementation Steps

### Step 1: Slack App Setup
- Create Slack app in workspace
- Get bot token and app token
- Configure bot permissions (DMs, channels, slash commands)
- Install app to workspace

### Step 2: Build Bot Foundation
- Install slack-bolt Python package
- Create basic bot that responds to messages
- Test connection with "hello world"

### Step 3: Build Natural Language Parser
- Start with simple regex for numbers/currency
- Add keyword matching to outcomes
- Test with various input formats
- Add confirmation for ambiguous inputs

### Step 4: Integrate Existing Services
- Connect to JsonWhygoRepository (Phase 2)
- Use ProgressService for recording (Phase 2)
- Use WhygoService for dashboards (Phase 2)
- Test end-to-end update flow

### Step 5: Build Reminder System
- Schedule Monday 9am reminders
- Group outcomes by owner
- Format reminder messages
- Track who responded

### Step 6: Build Escalation Logic
- Track reminder responses
- Send follow-up reminders
- Escalate to managers after 2 misses
- Allow manager override

### Step 7: Build Leadership Dashboard
- Aggregate company status
- Detect changes from last week
- Format summary message
- Schedule for Monday 9:30am

### Step 8: Add Slash Commands
- /whygo [department] - View department
- /whygo me - View my outcomes
- /whygo company - View company status

### Step 9: Polish & Deploy
- Add error handling
- Add logging
- Deploy to server (keep running)
- Test with small group first

## Critical Files

### New Files (Phase 3)

1. **`slack_bot/__init__.py`** - Package init
2. **`slack_bot/app.py`** - Main bot application
3. **`slack_bot/handlers.py`** - Message and command handlers
4. **`slack_bot/nl_parser.py`** - Natural language parser
5. **`slack_bot/scheduler.py`** - Reminder scheduling
6. **`slack_bot/formatters.py`** - Message formatting
7. **`slack_bot/user_mapping.py`** - Slack ↔ Person mapping
8. **`slack_bot/config.py`** - Bot configuration
9. **`requirements.txt`** - Add slack-bolt, schedule packages
10. **`.env.example`** - Environment variables template

### Modified Files

1. **`src/services/whygo_service.py`** - Add change detection method
2. **`src/services/progress_service.py`** - Add last update tracking

## Dependencies

```
slack-bolt==1.18+
schedule==1.2+
python-dotenv==1.0+
```

## Environment Variables

```
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
REMINDER_TIME=09:00
ESCALATION_DAYS=2
```

## Testing Strategy

### Phase 1: Manual Testing
- Test bot responds to DMs
- Test natural language parsing
- Test update recording

### Phase 2: Small Group Pilot
- 5 users (1 from each department)
- Run for 2 weeks
- Gather feedback

### Phase 3: Full Rollout
- All 22 team members
- Monitor adoption rate
- Iterate on UX

## Success Metrics

**Adoption:**
- 80%+ of outcome owners update weekly
- <5 manager escalations per week

**Engagement:**
- Average response time to reminder <4 hours
- 90%+ of outcomes recorded by Friday

**Leadership Value:**
- Leadership views dashboard weekly
- Blockers resolved within 1 week

## Rollout Plan

### Week 1: Foundation
- Build bot and test locally
- Manual testing with developer

### Week 2: Alpha
- Deploy to Slack
- Test with 2 users (you + 1 other)
- Refine NL parsing

### Week 3: Beta
- Expand to 5 users
- Test all flows
- Fix edge cases

### Week 4: Launch
- Announce to full team
- Send onboarding guide
- Monitor first update cycle

### Week 5+: Optimize
- Gather feedback
- Improve parsing
- Add requested features

## Alternative: Simpler MVP

If full Slack bot is too complex, start with:

**Option A: Webhook-based**
- CLI tool generates reminder messages
- Manually paste to Slack
- Users DM you with updates
- You run CLI tool to record

**Option B: Slack Incoming Webhooks**
- Automated messages only (no DMs)
- Post reminders to #whygos channel
- Users still use CLI tools
- Post summaries to #leadership

**Recommendation**: Build full bot (Option 1). Investment pays off in adoption.

## Key Design Decisions

1. **Natural Language vs Commands**
   - ✅ Chosen: Natural language (lower friction)
   - Users say "5 clients" not `/update cg_1_o1 5`

2. **DMs vs Channel**
   - ✅ Chosen: DMs for updates (private)
   - Channel for summaries (visibility)

3. **Proactive vs Reactive**
   - ✅ Chosen: Proactive reminders
   - Don't wait for users to remember

4. **LLM vs Regex Parsing**
   - ✅ Chosen: Start with regex
   - Add LLM later if needed (cost/complexity)

5. **Always-on Bot vs Scheduled**
   - ✅ Chosen: Always-on (accepts anytime updates)
   - Scheduled reminders as trigger

## Next Steps After Phase 3

**Phase 4: Analytics**
- Trend analysis
- Predictive insights
- Anomaly detection

**Phase 5: Goal Creation**
- Slack-based goal creator
- AI coaching for goal quality
- Approval workflows

**Phase 6: Integrations**
- Notion sync
- Google Sheets export
- Calendar reminders
