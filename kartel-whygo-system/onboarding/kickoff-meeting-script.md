# WhyGO Tracking System - Kickoff Meeting Script

**Duration**: 30 minutes
**Attendees**: Leadership + All Department Heads
**Format**: Live meeting with screen share

---

## Opening (2 minutes)

**Luke:**

> "Thanks everyone for joining. We're launching the WhyGO tracking system today - the tool that makes our 2026 goals *living documents* instead of planning files that sit unused.
>
> We spent Q4 working together to build our WhyGOs. We have 4 company goals, 14 department goals, and 74 measurable outcomes. This system ensures we actually track them weekly, know where we stand, and course-correct fast.
>
> Today I'll show you how it works, what's expected, and get you set up. This is 30 minutes well-spent to keep us aligned all year."

---

## Part 1: The Problem We're Solving (3 minutes)

**Luke:**

> "Let me start with why we need this.
>
> **The Old Way**: Goals exist in documents. You check them quarterly at best. By the time you realize something's off track, it's too late to fix.
>
> **The New Way**: Weekly updates. Real-time visibility. Leadership sees the full picture. Department heads see their teams. Everyone knows exactly where we stand.
>
> **What This Prevents**:
> - Surprises at the end of Q1: 'Wait, we thought we were on pace...'
> - Misalignment: Production thinks they're crushing it, but Sales needs different outputs
> - Invisible blockers: Someone stuck for 3 weeks before anyone notices
>
> **What This Enables**:
> - Clear accountability: You own outcomes, you update them weekly
> - Fast course-correction: See problems early, fix them fast
> - Leadership clarity: I can see company health at a glance
>
> This is how we scale without losing alignment."

---

## Part 2: Live Demo (10 minutes)

**Luke:** *(Share screen - terminal window)*

### Demo 1: Company Dashboard

```bash
python kartel-whygo-system/scripts/view_dashboard.py company
```

**Talk through what you're showing:**

> "This is the company dashboard. Shows all 4 company goals, all outcomes, and their status.
>
> See these indicators:
> - [+] On pace - we're at 100%+ of target
> - [~] Slightly off - 80-99% of target
> - [-] Off pace - below 80%
>
> Right now most outcomes show 'Not recorded' because we just launched. By next Monday, you'll see real status."

### Demo 2: Department View

```bash
python kartel-whygo-system/scripts/view_dashboard.py department dept_sales
```

**Talk through it:**

> "This is Ben's sales department view. Shows his team's goals and outcomes. Ben can check this anytime to see how Sales is doing.
>
> Notice it shows who owns each outcome. Clear accountability."

### Demo 3: Recording an Update

```bash
python kartel-whygo-system/scripts/record_progress.py cg_1_o1 Q1 5 \
  --person person_ben_kusin \
  --notes "Signed 5 enterprise clients in Q1"
```

**Talk through it:**

> "Here's how you update. Let's say Ben signed 5 enterprise clients. He runs this command with:
> - The outcome ID (cg_1_o1)
> - The quarter (Q1)
> - The actual value (5)
> - His person ID
> - Optional notes for context
>
> Watch what happens... *(run command)* ...the system calculates status automatically. Target was 4, Ben hit 5, so it shows [+] On pace!
>
> Takes 30 seconds per outcome."

### Demo 4: Person View

```bash
python kartel-whygo-system/scripts/view_dashboard.py person person_ben_kusin
```

**Talk through it:**

> "This is Ben's personal view. Shows all 14 outcomes he owns:
> - 3 at company level
> - 11 in his Sales department
>
> Ben checks this every Monday, updates what changed, done. 5-10 minutes total."

### Demo 5: Blocker Flag

```bash
python kartel-whygo-system/scripts/record_progress.py dept_sales_2_o1 Q1 0 \
  --person person_ben_kusin \
  --blocker "Waiting on legal approval for case study"
```

**Talk through it:**

> "If you're blocked, flag it. The --blocker flag lets leadership know you need help. We can see all active blockers in the dashboard and unblock you fast."

---

## Part 3: What's Expected (5 minutes)

**Luke:**

> "Here's what I need from each of you:
>
> **Department Heads (Ben, Wayan, Fill, Daniel, Niels)**:
> - Update your outcomes every Monday morning
> - Takes 5-10 minutes
> - Flag blockers immediately, don't wait
> - Check your team's status weekly
>
> **Leadership (Kevin, Luke, Ben)**:
> - Review company dashboard weekly
> - Spot blockers and help unblock
> - Use this in our leadership meetings
>
> **Timeline**:
> - Starting this Monday: First weekly update cycle begins
> - Every Monday moving forward
> - Phase 3 (Slack integration) coming soon to make this even easier
>
> **Where**:
> - CLI tools for now (I'll send you cheat sheets)
> - Slack bot in Phase 3 (you'll just reply to a DM)
>
> **Accountability**:
> - Your outcomes, your responsibility
> - If you miss 2 weeks, I'll follow up
> - This only works if we all commit

---

## Part 4: Your Outcomes (5 minutes)

**Luke:**

> "Let me show you what each person owns. I'm sending personalized cheat sheets after this meeting, but here's the summary:"

### Ownership Breakdown

**Ben Kusin**: 14 outcomes
- 3 company (clients, NPS, deployed talent)
- 11 sales department (engagements, revenue, case studies, infrastructure)

**Wayan Palmieri**: 18 outcomes
- 1 company (on-time delivery)
- 12 production department (capacity, quality, systems)
- 5 individual (personal goals)

**Fill Isgro**: 13 outcomes
- 2 company (generative capabilities, cost efficiency)
- 11 generative department (models, workflows, quality)

**Daniel Kalotov**: 9 outcomes
- 2 company (community growth, talent deployment)
- 7 community department (member engagement, talent activation)

**Niels Hoffmann**: 13 outcomes
- 2 company (platform milestones, client adoption)
- 11 platform department (features, uptime, integrations)

**Luke:**

> "Check your cheat sheet for the full list with targets and IDs. Your cheat sheet has copy-paste commands ready to go."

---

## Part 5: Q&A (5 minutes)

**Luke:**

> "Questions?"

**Common Questions to Anticipate:**

**Q**: "What if I forget the commands?"
**A**: "Your cheat sheet has every command you need. Copy-paste ready. Bookmark it."

**Q**: "What if my outcome didn't change this week?"
**A**: "Only update outcomes that changed. If nothing changed, skip it."

**Q**: "What happens if I'm off pace?"
**A**: "Status shows [-]. That's OK - it's early warning. We course-correct together. Better to know early than late."

**Q**: "How long will this take?"
**A**: "5-10 minutes every Monday. Small investment for massive alignment benefit."

**Q**: "What if I'm stuck on something?"
**A**: "Flag it with --blocker. Leadership will see it and help unblock you."

**Q**: "When does Phase 3 Slack integration launch?"
**A**: "In the next few weeks. For now, CLI gets us started. Slack will make it even easier - you'll just reply to a DM in plain English."

---

## Closing (1 minute)

**Luke:**

> "Here's what happens next:
>
> 1. **Right now**: I'm sending you an email with:
>    - Your personalized cheat sheet
>    - The full quick-start guide
>    - Links to everything you need
>
> 2. **This Monday**: First update cycle begins. Check your cheat sheet, run the commands, update your outcomes.
>
> 3. **This week**: I'm available on Slack for questions. If you get stuck, ping me immediately.
>
> 4. **Next Monday**: We'll review the company dashboard in our leadership meeting. See what we learned from week 1.
>
> **Why This Matters**:
> We're building something ambitious in 2026. This system ensures we stay aligned, move fast, and win together.
>
> Let's make this the year Kartel becomes the category leader in Creative Intelligence Infrastructure.
>
> Thanks everyone!"

---

## Post-Meeting Actions

1. **Immediately send email** with:
   - Personalized cheat sheets (attached)
   - Quick start guide
   - Link to GitHub repo

2. **Monday morning**: Send Slack reminder: "WhyGO update day! Check your cheat sheet or ping Luke for help."

3. **Wednesday check-in**: Slack message: "Who's recorded updates? Who needs help?"

4. **Friday recap**: Share company dashboard in #leadership: "Here's our Q1 progress so far..."

5. **Next week's leadership meeting**: Review week 1 learnings, celebrate early adopters, address blockers.
