# Email to Team: WhyGO Tracking System Launch

**Subject**: WhyGO Tracking System - Your Quick Start Guide

---

Hi team,

Great kickoff meeting today! As promised, here's everything you need to get started with the WhyGO tracking system.

---

## 🎯 What This Is

A simple system to track our 2026 goals weekly. You record actuals, the system calculates status automatically, leadership sees progress in real-time.

**Why it matters**: We built ambitious WhyGOs together. This ensures they're living documents, not planning files that collect dust.

---

## 📊 Your Outcomes

**Attached** is your personalized cheat sheet with:
- All outcomes you own (company + department + individual)
- Q1 targets for each outcome
- Copy-paste commands ready to go
- Your Monday morning routine

**Quick summary:**
- Ben Kusin: 14 outcomes (Sales)
- Wayan Palmieri: 18 outcomes (Production)
- Fill Isgro: 13 outcomes (Generative)
- Daniel Kalotov: 9 outcomes (Community)
- Niels Hoffmann: 13 outcomes (Platform)

---

## ⏰ Weekly Cadence (Starting Monday)

Every Monday morning, takes 5-10 minutes:

1. **View your status** (2 min)
   - See which outcomes are on pace, which need attention

2. **Record updates** (3-5 min)
   - Update outcomes that changed this week
   - Add notes for context

3. **Flag blockers** (1 min)
   - If you're stuck, flag it so leadership can help

---

## 🛠️ How to Update

### Step 1: Navigate to project
```bash
cd ~/Desktop/Git\ Projects/WHYGOs
```

### Step 2: View your outcomes
```bash
python kartel-whygo-system/scripts/view_dashboard.py person person_YOUR_NAME
```

Replace `person_YOUR_NAME` with your person ID:
- `person_ben_kusin`
- `person_wayan_palmieri`
- `person_fill_isgro`
- `person_daniel_kalotov`
- `person_niels_hoffmann`

### Step 3: Update an outcome
```bash
python kartel-whygo-system/scripts/record_progress.py OUTCOME_ID Q1 VALUE \
  --person person_YOUR_NAME \
  --notes "Context about this update"
```

**Example** (Ben updating enterprise clients):
```bash
python kartel-whygo-system/scripts/record_progress.py cg_1_o1 Q1 5 \
  --person person_ben_kusin \
  --notes "Signed 5 enterprise clients in Q1"
```

### Step 4: Flag a blocker (if needed)
```bash
python kartel-whygo-system/scripts/record_progress.py OUTCOME_ID Q1 VALUE \
  --person person_YOUR_NAME \
  --blocker "Describe what's blocking you"
```

**Example** (Ben flagging a case study blocker):
```bash
python kartel-whygo-system/scripts/record_progress.py dept_sales_2_o1 Q1 0 \
  --person person_ben_kusin \
  --blocker "Waiting on legal approval"
```

---

## 📈 Understanding Status

The system automatically calculates status by comparing your actual vs target:

- **[+] On pace** - You're at 100%+ of target 🎉
- **[~] Slightly off** - You're at 80-99% of target
- **[-] Off pace** - You're below 80% of target ⚠️

**Important**: Off-pace is OK! It's early warning. Better to know now and course-correct than to be surprised later.

---

## 🚀 Coming Soon: Phase 3 (Slack Integration)

In the next few weeks, we're launching a Slack bot that makes this even easier:

**Instead of CLI commands**, you'll:
1. Get a DM every Monday morning
2. Reply in plain English: "Signed 5 clients, pipeline is $2M"
3. Bot records it automatically

For now, CLI gets us started. The Slack bot will be worth the wait!

---

## 💡 Tips for Success

1. **Bookmark your cheat sheet** - Everything you need in one place
2. **Update weekly** - Consistency builds habits
3. **Use notes** - Context helps leadership understand the story behind the numbers
4. **Flag blockers early** - Don't wait until you're off pace to ask for help
5. **Only update what changed** - If an outcome didn't change this week, skip it

---

## 🆘 Need Help?

**This week**: I'm on Slack all day to answer questions. If you get stuck on Monday:
1. Ping me immediately: @luke_peterson
2. Or bring it to Monday standup

**Common questions**:

**Q**: "I'm getting a 'command not found' error"
**A**: Make sure you're in the right directory: `cd ~/Desktop/Git\ Projects/WHYGOs`

**Q**: "What if I don't know my person_id?"
**A**: Check your cheat sheet - it's at the top of every command

**Q**: "What if my outcome didn't change this week?"
**A**: Skip it. Only update outcomes that changed.

**Q**: "How do I know if I'm entering the value correctly?"
**A**:
- Numbers: Just the number (5, 10, 50)
- Currency: Just the amount without symbols (1500000 for $1.5M)
- Percentages: Just the number (85 for 85%)
- Milestones: In quotes ("MVP", "Live", "Complete")

---

## 📅 What Happens Next

**Monday**: First update cycle begins
- Check your cheat sheet
- Run the commands
- Ping me with questions

**Wednesday**: I'll check in on Slack
- "Who's recorded updates? Who needs help?"

**Friday**: Company dashboard recap
- Share progress in #leadership channel
- Celebrate wins from week 1

**Next Monday**: Review in leadership meeting
- See what we learned
- Adjust as needed
- Plan for week 2

---

## 📂 Resources

**Your personalized cheat sheet**: *(Attached)*
**GitHub repo**: https://github.com/luke-peterson-kartel/Kartel_Whygos
**Demo video** (coming soon): I'll record a walkthrough for reference

---

## 🎉 Let's Do This

We're building something ambitious in 2026. This system ensures we stay aligned, move fast, and win together.

Your 5-10 minutes every Monday keeps us all on the same page. Small investment, massive impact.

See you Monday morning for the first update cycle!

Luke

---

**P.S.**: Reply to this email if anything is unclear. I want to make sure everyone feels confident before Monday.

---

## Attachments

✓ `cheatsheet-YOUR-NAME.md` - Your personalized quick reference
✓ `kickoff-meeting-script.md` - Today's presentation for reference
✓ `slide-deck.pdf` - Slides from today's meeting

---

*WhyGO Tracking System | Phase 2 Complete | Phase 3 (Slack Integration) Coming Soon*
