# Wayan Palmieri's WhyGO Cheat Sheet - Q1 2026

## Your Outcomes at a Glance

You own **18 outcomes** across company, department, and individual levels.

### Company Level (1 outcomes)

1. `cg_2_o2` - On-Time Delivery Rate
   - **Target Q1**: 80
   - **Type**: Percentage

### Department Level - Production (12 outcomes)

2. `dept_production_1_o1` - Active client engagements
   - **Target Q1**: 6-8
   - **Type**: Number

3. `dept_production_1_o3` - Handoff #2 Compliance (Prod→Gen)
   - **Target Q1**: 80
   - **Type**: Number

4. `dept_production_1_o5` - Handoff #4: Closing Reports delivered
   - **Target Q1**: 80
   - **Type**: Boolean

5. `dept_production_1_o6` - Case study packages delivered
   - **Target Q1**: 2
   - **Type**: Boolean

6. `dept_production_1_o7` - Avg. onboarding time (SOW → pod)
   - **Target Q1**: 21 days
   - **Type**: Number

7. `dept_production_2_o1` - Production Margin
   - **Target Q1**: 40
   - **Type**: Percentage

8. `dept_production_2_o2` - On-Time Delivery vs. Workflow SLA
   - **Target Q1**: 80
   - **Type**: Number

9. `dept_production_2_o3` - Client job requests submitted (platform)
   - **Target Q1**: Baseline
   - **Type**: Number

10. `dept_production_3_o1` - Producers on team
   - **Target Q1**: 3
   - **Type**: Number

11. `dept_production_3_o2` - Client-to-Producer ratio (actual)
   - **Target Q1**: Baseline
   - **Type**: Number

12. `dept_production_3_o3` - Producer onboarding time (hire → independent)
   - **Target Q1**: Baseline
   - **Type**: Number

13. `dept_production_3_o4` - Producer job description & hiring criteria documented
   - **Target Q1**: Done
   - **Type**: Milestone

### Individual Level (5 outcomes)

14. `ig_wayan_1_o1` - Decision categories delegated (scope, timelines, staffing, quality, margin)
   - **Target Q1**: 1/5
   - **Type**: Percentage

15. `ig_wayan_1_o2` - Escalations requiring Wayan per week
   - **Target Q1**: Baseline
   - **Type**: Number

16. `ig_wayan_2_o1` - Monthly Execution Truth Briefs delivered
   - **Target Q1**: 3
   - **Type**: Boolean

17. `ig_wayan_2_o2` - Issues surfaced → changes made (pricing, SOW, platform, enablement)
   - **Target Q1**: 2
   - **Type**: Number

18. `ig_wayan_2_o3` - Repeat issues (same problem 2x+ across clients)
   - **Target Q1**: Baseline
   - **Type**: Number

---

## Quick Commands (Copy-Paste Ready)

### View All Your Outcomes
```bash
cd ~/Desktop/Git\ Projects/WHYGOs
python kartel-whygo-system/scripts/view_dashboard.py person person_wayan_palmieri
```

### View Your Department Dashboard
```bash
python kartel-whygo-system/scripts/view_dashboard.py department dept_prod
```

### Update Outcome (Template)
```bash
python kartel-whygo-system/scripts/record_progress.py OUTCOME_ID Q1 VALUE \
  --person person_wayan_palmieri \
  --notes "Your context here"
```

### Example Update
```bash
# Replace OUTCOME_ID and VALUE with your actual data
python kartel-whygo-system/scripts/record_progress.py cg_2_o2 Q1 VALUE \
  --person person_wayan_palmieri \
  --notes "Context about this update"
```

### With a Blocker
```bash
python kartel-whygo-system/scripts/record_progress.py OUTCOME_ID Q1 VALUE \
  --person person_wayan_palmieri \
  --blocker "Describe what's blocking you"
```

---

## Monday Morning Routine (5-10 minutes)

### Step 1: View Your Status (2 min)
```bash
python kartel-whygo-system/scripts/view_dashboard.py person person_wayan_palmieri
```

### Step 2: Update Changed Outcomes (3-5 min)
- Update any outcomes that changed this week
- Add notes for context
- Flag blockers if you're stuck

### Step 3: Review (1 min)
- Quick check: Are you on pace? [+] [~] [-]
- Any outcomes need attention this week?

---

## Status Indicators

- **[+] On pace** - You're at 100%+ of target 🎉
- **[~] Slightly off** - You're at 80-99% of target
- **[-] Off pace** - You're below 80% of target ⚠️

---

## Tips

1. **Update weekly** - Consistency builds habits
2. **Use notes** - Context helps leadership understand the story
3. **Flag blockers early** - Don't wait until you're off pace
4. **Ask questions** - Ping Luke on Slack if you're stuck

---

## Need Help?

- **Slack**: @luke_peterson
- **Monday Standup**: Bring questions
- **Phase 3 Coming**: Slack bot will make this even easier
