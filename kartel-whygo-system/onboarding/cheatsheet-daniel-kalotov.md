# Daniel Kalotov's WhyGO Cheat Sheet - Q1 2026

## Your Outcomes at a Glance

You own **9 outcomes** across company and department levels.

### Company Level (2 outcomes)

1. `cg_3_o1` - Discord Community Members
   - **Target Q1**: 300
   - **Type**: Number

2. `cg_3_o3` - Roles covered (Workflow Eng, AI Generalist, Data Spec, Training Spec, Preditor)
   - **Target Q1**: 3/5
   - **Type**: Number

### Department Level - Community (7 outcomes)

3. `dept_community_and_partnerships_1_o1` - Discord community members
   - **Target Q1**: 300
   - **Type**: Number

4. `dept_community_and_partnerships_1_o2` - Qualified talent ready for pod deployment (Tier 5)
   - **Target Q1**: 5
   - **Type**: Number

5. `dept_community_and_partnerships_1_o3` - Lighthouse certification live (4 role tracks)
   - **Target Q1**: Setup
   - **Type**: Milestone

6. `dept_community_and_partnerships_1_o4` - Sponsored community events (Prompetitions, brand challenges)
   - **Target Q1**: 1
   - **Type**: Number

7. `dept_community_and_partnerships_2_o1` - Active member rate (weekly engagement)
   - **Target Q1**: Baseline
   - **Type**: Percentage

8. `dept_community_and_partnerships_2_o2` - Tier progression velocity (Tier 1 → Tier 4)
   - **Target Q1**: Baseline
   - **Type**: Number

9. `dept_community_and_partnerships_2_o3` - Generation credits utilized
   - **Target Q1**: Baseline
   - **Type**: Number

---

## Quick Commands (Copy-Paste Ready)

### View All Your Outcomes
```bash
cd ~/Desktop/Git\ Projects/WHYGOs
python kartel-whygo-system/scripts/view_dashboard.py person person_daniel_kalotov
```

### View Your Department Dashboard
```bash
python kartel-whygo-system/scripts/view_dashboard.py department dept_comm
```

### Update Outcome (Template)
```bash
python kartel-whygo-system/scripts/record_progress.py OUTCOME_ID Q1 VALUE \
  --person person_daniel_kalotov \
  --notes "Your context here"
```

### Example Update
```bash
# Replace OUTCOME_ID and VALUE with your actual data
python kartel-whygo-system/scripts/record_progress.py cg_3_o1 Q1 VALUE \
  --person person_daniel_kalotov \
  --notes "Context about this update"
```

### With a Blocker
```bash
python kartel-whygo-system/scripts/record_progress.py OUTCOME_ID Q1 VALUE \
  --person person_daniel_kalotov \
  --blocker "Describe what's blocking you"
```

---

## Monday Morning Routine (5-10 minutes)

### Step 1: View Your Status (2 min)
```bash
python kartel-whygo-system/scripts/view_dashboard.py person person_daniel_kalotov
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
