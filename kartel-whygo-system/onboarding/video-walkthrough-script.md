# Video Walkthrough Script: WhyGO Tracking System

**Duration**: 8-10 minutes
**Format**: Screen recording with voiceover
**Tool**: Loom, QuickTime, or OBS
**Audience**: All team members

---

## Pre-Recording Checklist

- [ ] Terminal window open and sized appropriately
- [ ] Font size increased (18-20pt for readability)
- [ ] Clear your terminal history (`clear` command)
- [ ] Have sample commands ready to paste
- [ ] Test audio levels
- [ ] Close unnecessary applications/notifications
- [ ] Set terminal to light theme (better contrast for recording)

---

## Scene 1: Introduction (30 seconds)

### On Screen
- Your face (optional camera)
- Terminal window ready

### Script

> "Hey team, Luke here. This is a quick walkthrough of the WhyGO tracking system - how to view your outcomes and record weekly updates.
>
> By the end of this 10-minute video, you'll know exactly what to do every Monday morning. Let's jump in."

---

## Scene 2: Navigating to the Project (30 seconds)

### On Screen
- Show terminal
- Type commands slowly

### Script

> "First, navigate to the project directory. Open your terminal and run:"

```bash
cd ~/Desktop/Git\ Projects/WHYGOs
```

> "This is where all the code lives. You'll start here every time."

*(Pause 2 seconds so they can see the command)*

> "If you get a 'directory not found' error, check where you cloned the repo. Adjust the path as needed."

---

## Scene 3: Viewing Your Outcomes (2 minutes)

### On Screen
- Run person dashboard command
- Scroll through output slowly

### Script

> "Now let's see all the outcomes you own. I'll use Ben as an example:"

```bash
python kartel-whygo-system/scripts/view_dashboard.py person person_ben_kusin
```

*(Let command run, show full output)*

> "This shows all 14 outcomes Ben owns. Let me walk through what you're seeing:
>
> At the top: Total outcomes owned and status breakdown. Right now it says 'Not recorded' because we just launched.
>
> Below that: Each outcome with its description, target, and current actual.
>
> The status indicators:
> - [+] means on pace - you're at 100% or better
> - [~] means slightly off - 80-99% of target
> - [-] means off pace - below 80%
>
> Replace 'person_ben_kusin' with your own person_id from your cheat sheet."

*(Scroll back to top of output)*

> "This is your starting point every Monday. Check your status, see what needs updating."

---

## Scene 4: Recording Your First Update (3 minutes)

### On Screen
- Type and run record command
- Show the confirmation output

### Script

> "Now let's record an update. Say Ben signed 5 enterprise clients in Q1. Here's the command:"

```bash
python kartel-whygo-system/scripts/record_progress.py cg_1_o1 Q1 5 \
  --person person_ben_kusin \
  --notes "Signed 5 enterprise clients in Q1"
```

*(Type it out slowly, don't just paste)*

> "Let me break this down:
>
> - `cg_1_o1` - This is the outcome ID. You'll find this in your cheat sheet.
> - `Q1` - The quarter we're recording for
> - `5` - The actual value achieved
> - `--person person_ben_kusin` - Who's recording this update
> - `--notes` - Optional context about the update
>
> Now let's run it..."

*(Press enter, show output)*

> "Great! The system confirms:
> - Progress recorded
> - Target was 4, actual is 5
> - Status is [+] On pace - 125% of target!
>
> It also shows which files were updated. The system does all the math for you."

---

## Scene 5: Viewing Updated Status (1 minute)

### On Screen
- Re-run person dashboard
- Show the updated status

### Script

> "Let's check Ben's dashboard again to see the update:"

```bash
python kartel-whygo-system/scripts/view_dashboard.py person person_ben_kusin
```

> "Now look - cg_1_o1 shows:
> - Actual: 5
> - Status: [+] On pace
>
> The update is recorded and status calculated automatically. That's the power of this system."

---

## Scene 6: Recording Different Value Types (2 minutes)

### On Screen
- Show examples of different metric types

### Script

> "Let me show you how to record different types of values.
>
> **Numbers** (like client count):"

```bash
python kartel-whygo-system/scripts/record_progress.py cg_1_o1 Q1 5 \
  --person person_ben_kusin
```

> "Just enter the number.
>
> **Currency** (like revenue):"

```bash
python kartel-whygo-system/scripts/record_progress.py dept_sales_1_o4 Q1 1800000 \
  --person person_ben_kusin \
  --notes "Q1 revenue: $1.8M"
```

> "Enter the amount without dollar signs or commas. So $1.8 million is 1800000. Add the $ in your notes for clarity.
>
> **Percentages** (like NPS or retention):"

```bash
python kartel-whygo-system/scripts/record_progress.py dept_sales_2_o3 Q1 92 \
  --person person_ben_kusin \
  --notes "Client retention at 92%"
```

> "Just the number, no percent sign. So 92% is entered as 92.
>
> **Milestones** (like 'MVP' or 'Live'):"

```bash
python kartel-whygo-system/scripts/record_progress.py cg_4_o1 Q1 "MVP" \
  --person person_ben_kusin \
  --notes "Client portal MVP launched"
```

> "Put the milestone in quotes. Match exactly what the target says."

---

## Scene 7: Flagging a Blocker (1 minute)

### On Screen
- Show blocker command
- Run and show output

### Script

> "If you're blocked on something, flag it immediately. Here's how:"

```bash
python kartel-whygo-system/scripts/record_progress.py dept_sales_2_o1 Q1 0 \
  --person person_ben_kusin \
  --blocker "Waiting on legal approval for case study"
```

> "The --blocker flag tells leadership you need help. We can see all active blockers in the dashboard and unblock you fast.
>
> Don't wait until you're off pace to ask for help. Flag it early."

---

## Scene 8: Department & Company Views (1 minute)

### On Screen
- Show department view
- Show company view

### Script

> "You can also check your department's status:"

```bash
python kartel-whygo-system/scripts/view_dashboard.py department dept_sales
```

> "This shows all Sales outcomes and who owns them.
>
> And leadership can see the full company view:"

```bash
python kartel-whygo-system/scripts/view_dashboard.py company
```

> "All 4 company goals, all 74 outcomes, company-wide status at a glance."

---

## Scene 9: Your Monday Routine (1 minute)

### On Screen
- Show list of steps on screen or in terminal

### Script

> "Here's your Monday morning routine. Takes 5-10 minutes:
>
> **Step 1** (2 min): View your status
> Run the person dashboard, see what's on pace, what needs attention.
>
> **Step 2** (3-5 min): Update changed outcomes
> Only update outcomes that changed this week. Skip the rest.
>
> **Step 3** (1 min): Flag blockers
> If you're stuck, flag it with --blocker.
>
> That's it. Simple, quick, keeps us aligned."

---

## Scene 10: Common Mistakes to Avoid (1 minute)

### On Screen
- Type out examples of errors

### Script

> "Quick tips on common mistakes:
>
> **Wrong directory**:
> If you get 'No such file or directory', make sure you're in the WHYGOs folder first.
>
> **Wrong person_id**:
> Check your cheat sheet. It's person_YOUR_NAME, all lowercase, underscores.
>
> **Currency formatting**:
> Don't use $ or commas. 1500000, not $1,500,000.
>
> **Quotes on milestones**:
> Put milestones in quotes. 'MVP' not MVP.
>
> If you hit an error, ping Luke on Slack. I'll help you debug."

---

## Scene 11: What's Coming (30 seconds)

### On Screen
- Show Phase 3 plan or Slack logo

### Script

> "One last thing: Phase 3 is coming soon - Slack integration.
>
> Instead of CLI commands, you'll get a DM every Monday. Reply in plain English like 'Signed 5 clients, pipeline is $2M' and the bot records it automatically.
>
> For now, CLI gets us started. The Slack bot will be worth the wait!"

---

## Scene 12: Closing (30 seconds)

### On Screen
- Your face (if using camera)
- Or terminal with resources displayed

### Script

> "That's it! You now know how to:
> - View your outcomes
> - Record updates
> - Flag blockers
> - Check your status
>
> Your cheat sheet has all the commands ready to copy-paste. Bookmark it.
>
> See you Monday morning for the first update cycle. Ping me on Slack with any questions.
>
> Let's make 2026 our best year. Thanks team!"

---

## Post-Production

### Editing Checklist
- [ ] Add title card at beginning with "WhyGO Tracking System Walkthrough"
- [ ] Add chapter markers at each scene
- [ ] Add callout boxes/arrows highlighting key commands
- [ ] Add text overlays for:
  - Person IDs (person_ben_kusin, etc.)
  - Key commands (record_progress.py, view_dashboard.py)
  - Status indicators ([+], [~], [-])
- [ ] Add transitions between scenes (simple fade)
- [ ] Normalize audio levels
- [ ] Add captions/subtitles (for accessibility)

### End Card
- Text: "Resources"
- Link to GitHub repo
- Link to cheat sheets
- Link to Slack channel for questions
- "Questions? Ping @luke_peterson"

---

## Distribution

**Upload to**:
1. Loom (if using Loom)
2. Company shared drive
3. Slack #announcements channel
4. Include link in follow-up email

**Pin in Slack** so new team members can find it later.

---

## Optional: Create 60-Second Version

For quick reference, create a condensed version:
- Skip the detailed explanations
- Show only: Navigate → View → Update → Done
- Text overlays with key points
- Share as "Quick Start" video

---

## Thumbnail Design

**For video preview/thumbnail**:
- Screenshot of terminal with status indicators
- Text overlay: "WhyGO Tracking System"
- Subtext: "Your 10-Minute Quick Start"
- Kartel logo in corner
- Make it visually distinct so people can find it easily
