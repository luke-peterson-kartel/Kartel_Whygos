# Ben Kusin's WhyGO Cheat Sheet - Q1 2026

## Your Outcomes at a Glance

You own **14 outcomes** across company and department levels.

### Company Level (3 outcomes)

**Company Goal #1: Prove Product-Market Fit**

1. `cg_1_o1` - Enterprise clients signed (total)
   - **Target Q1**: 4
   - **Type**: Number

2. `cg_2_o3` - Client NPS (avg across all clients)
   - **Target Q1**: 50
   - **Type**: Number

3. `cg_3_o4` - Deployed talent (total talent placed on projects)
   - **Target Q1**: 10
   - **Type**: Number

### Department Level - Sales (11 outcomes)

**Sales Goal #1: Sign 18+ enterprise spec engagements**

4. `dept_sales_1_o1` - Spec engagements signed (cumulative)
   - **Target Q1**: 18
   - **Type**: Number

5. `dept_sales_1_o2` - Post-spec paying clients (converted)
   - **Target Q1**: 4
   - **Type**: Number

6. `dept_sales_1_o3` - Verticals represented in client base
   - **Target Q1**: 3
   - **Type**: Number

7. `dept_sales_1_o4` - Revenue closed (cumulative)
   - **Target Q1**: $1,500,000
   - **Type**: Currency

**Sales Goal #2: Achieve 50+ NPS and publish case studies**

8. `dept_sales_2_o1` - Case studies published (public)
   - **Target Q1**: 1
   - **Type**: Number

9. `dept_sales_2_o2` - Client NPS score (average)
   - **Target Q1**: 50
   - **Type**: Number

10. `dept_sales_2_o3` - Client retention rate (%)
    - **Target Q1**: 90%
    - **Type**: Percentage

**Sales Goal #3: Enterprise sales infrastructure**

11. `dept_sales_3_o1` - CRM pipeline accuracy (forecasted vs actual)
    - **Target Q1**: 85%
    - **Type**: Percentage

12. `dept_sales_3_o2` - Average deal cycle length (days)
    - **Target Q1**: 45
    - **Type**: Number

13. `dept_sales_3_o3` - Win rate on qualified opportunities (%)
    - **Target Q1**: 30%
    - **Type**: Percentage

14. `dept_sales_3_o4` - Repeat business rate (%)
    - **Target Q1**: 20%
    - **Type**: Percentage

---

## Quick Commands (Copy-Paste Ready)

### View All Your Outcomes
```bash
cd ~/Desktop/Git\ Projects/WHYGOs
python kartel-whygo-system/scripts/view_dashboard.py person person_ben_kusin
```

### View Sales Department Dashboard
```bash
python kartel-whygo-system/scripts/view_dashboard.py department dept_sales
```

### Update Outcome (Template)
```bash
python kartel-whygo-system/scripts/record_progress.py OUTCOME_ID Q1 VALUE \
  --person person_ben_kusin \
  --notes "Your context here"
```

### Common Updates (Copy & Modify)

**Enterprise clients:**
```bash
python kartel-whygo-system/scripts/record_progress.py cg_1_o1 Q1 5 \
  --person person_ben_kusin \
  --notes "Signed [COMPANY NAME]"
```

**Spec engagements:**
```bash
python kartel-whygo-system/scripts/record_progress.py dept_sales_1_o1 Q1 20 \
  --person person_ben_kusin \
  --notes "Total specs signed this quarter"
```

**Revenue closed:**
```bash
python kartel-whygo-system/scripts/record_progress.py dept_sales_1_o4 Q1 1800000 \
  --person person_ben_kusin \
  --notes "Q1 revenue total"
```

**With a blocker:**
```bash
python kartel-whygo-system/scripts/record_progress.py dept_sales_2_o1 Q1 0 \
  --person person_ben_kusin \
  --blocker "Waiting on legal approval"
```

---

## Monday Morning Routine (5-10 minutes)

### Step 1: View Your Status (2 min)
```bash
python kartel-whygo-system/scripts/view_dashboard.py person person_ben_kusin
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
