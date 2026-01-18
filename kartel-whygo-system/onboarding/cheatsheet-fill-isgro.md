# Fill Isgro's WhyGO Cheat Sheet - Q1 2026

## Your Outcomes at a Glance

You own **13 outcomes** across company and department levels.

### Company Level (2 outcomes)

1. `cg_3_o2` - Tier 5: Approved Kartel Talent (deployed on client work)
   - **Target Q1**: 5
   - **Type**: Number

2. `cg_4_o3` - Generative Platform: Workflows, LoRA training, client data, media gen
   - **Target Q1**: MVP
   - **Type**: Milestone

### Department Level - Generative (11 outcomes)

3. `dept_generative_engineering_1_o1` - Role Playbooks completed (5 roles)
   - **Target Q1**: 2
   - **Type**: Boolean

4. `dept_generative_engineering_1_o2` - Playbooks reviewed & approved as onboarding ready
   - **Target Q1**: 1
   - **Type**: Number

5. `dept_generative_engineering_1_o3` - Pod capacity load-tested (full cycle: workflow → LoRA → output → feedback)
   - **Target Q1**: Tested
   - **Type**: Number

6. `dept_generative_engineering_1_o4` - Max concurrent clients per Gen pod (discovered)
   - **Target Q1**: Test
   - **Type**: Number

7. `dept_generative_engineering_2_o1` - QC process documented and in use (bulk run success + visual standards)
   - **Target Q1**: Done
   - **Type**: Milestone

8. `dept_generative_engineering_2_o2` - R&D reports (team explores, Fill synthesizes)
   - **Target Q1**: 3
   - **Type**: Number

9. `dept_generative_engineering_2_o3` - LoRA Eval tool deployed and integrated
   - **Target Q1**: MVP
   - **Type**: Percentage

10. `dept_generative_engineering_2_o4` - Bulk run success rate (≥1 client-worthy output per batch)
   - **Target Q1**: Baseline
   - **Type**: Percentage

11. `dept_generative_engineering_3_o1` - Internal Enterprise Platform: Key use cases (LoRA, captioning, curation, chat)
   - **Target Q1**: 1
   - **Type**: Number

12. `dept_generative_engineering_3_o3` - Platform adopted into standard workflow
   - **Target Q1**: Baseline
   - **Type**: Number

13. `dept_generative_engineering_3_o5` - Monthly Kartel Labs Demo Day
   - **Target Q1**: 3
   - **Type**: Number

---

## Quick Commands (Copy-Paste Ready)

### View All Your Outcomes
```bash
cd ~/Desktop/Git\ Projects/WHYGOs
python kartel-whygo-system/scripts/view_dashboard.py person person_fill_isgro
```

### View Your Department Dashboard
```bash
python kartel-whygo-system/scripts/view_dashboard.py department dept_gen
```

### Update Outcome (Template)
```bash
python kartel-whygo-system/scripts/record_progress.py OUTCOME_ID Q1 VALUE \
  --person person_fill_isgro \
  --notes "Your context here"
```

### Example Update
```bash
# Replace OUTCOME_ID and VALUE with your actual data
python kartel-whygo-system/scripts/record_progress.py cg_3_o2 Q1 VALUE \
  --person person_fill_isgro \
  --notes "Context about this update"
```

### With a Blocker
```bash
python kartel-whygo-system/scripts/record_progress.py OUTCOME_ID Q1 VALUE \
  --person person_fill_isgro \
  --blocker "Describe what's blocking you"
```

---

## Monday Morning Routine (5-10 minutes)

### Step 1: View Your Status (2 min)
```bash
python kartel-whygo-system/scripts/view_dashboard.py person person_fill_isgro
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
