---
name: how-cooked
description: Gives students a funny cooked score or academic aura score from real Canvas and Calendar signals. Use when a student asks "how cooked am I?", requests an aura check, says "rate me", wants a vibe check, or wants a playful workload reality check.
---

# Student Status: Cooked Score and Aura Check

Give the student a fast, funny status check based on real deadlines, completed work, and planned focus time. Keep it light, accurate, and short enough to screenshot.

## When to use

Use this skill when the student asks how cooked they are, requests an aura score, says "rate me" or "vibe check", or wants their academic workload roasted.

When the request does not name a score, send only this menu:

```text
STUDENT STATUS MENU
1. How Cooked Am I? 🔥
2. Aura Check ✨
Reply 1 or 2.
```

Treat `1` as How Cooked Am I and `2` as Aura Check. Also accept the option name. Do not show the menu when the student already chose a score.

For Cooked Score, default to the next 72 hours. For Aura Check, default to the next 7 days plus current overdue items. If the student gives another time range, use it and mention it in the reply.

## Gather the workload

1. Read the student's Canvas assignments, due dates, and submitted state for the requested window, plus current overdue items.
2. For Cooked Score, exclude work that Canvas clearly marks as submitted or complete.
3. Read Google Calendar for open time before the nearest deadlines and focus blocks that are clearly scheduled for schoolwork.
4. Never invent an assignment, due date, submission state, or free block.
5. If Canvas is unavailable, ask the student to connect it or text their deadlines. If Calendar is unavailable, continue with Canvas and say the calendar was not included.

Treat an item as an exam or project only when its title or Canvas details make that clear. Do not guess its importance from the course name.

## Calculate the cooked score

Build a temporary JSON object with this shape:

```json
{
  "now": "2026-10-24T14:00:00-07:00",
  "window_hours": 72,
  "available_minutes": 120,
  "planned_focus_minutes": 60,
  "tasks": [
    {
      "name": "Project 2",
      "course": "CSE 310",
      "due": "2026-10-25T23:59:00-07:00",
      "submitted": false,
      "kind": "project"
    }
  ]
}
```

Run:

```bash
python3 scripts/cook.py --input /path/to/workload.json
```

Use the script's score, level, biggest threat, and calculation. The score is workload triage for entertainment, not a grade prediction.

If the script cannot run, apply the same rubric yourself:

- overdue: 25 points each
- due in 12 hours: 20 points each
- due in 24 hours: 15 points each
- due in 48 hours: 10 points each
- due in 72 hours: 5 points each
- due later in a longer requested window: 2 points each
- clearly labeled exam or project in the window: 5 extra points each
- subtract 5 points per available hour before the deadlines, up to 20 points
- clamp the total from 0 to 100

Levels:

- 0–20: refrigerated
- 21–40: lightly toasted
- 41–60: air-fried
- 61–80: well done
- 81–99: charcoal
- 100: academically cremated

## Calculate the aura score

Use the same temporary JSON object, including submitted upcoming work and `planned_focus_minutes`. Count only Calendar blocks that are clearly for studying, assignments, or an identified course. Generic free time is not planned focus time.

Run:

```bash
python3 scripts/cook.py --mode aura --input /path/to/workload.json
```

Aura measures visible academic momentum for fun. It does not measure the student's value, intelligence, popularity, or personality.

If the script cannot run, start at 50 and apply the same rubric:

- add 5 for each already-submitted item due in the requested window, up to 20
- add 5 per scheduled focus hour, up to 20
- add 10 when there are no current overdue items
- subtract 10 per overdue item, up to 30
- subtract 5 per open item due within 24 hours, up to 15
- clamp the total from 0 to 100

Aura levels:

- 0–20: aura debt
- 21–40: side-quest energy
- 41–60: respectable motion
- 61–80: campus main character
- 81–99: generational aura
- 100: mythic office-hours lore

## Write the reply

Send one plain-text iMessage with four or five short lines:

1. `COOKED SCORE: [score]% [emoji]`
2. `Status: [level plus a fresh, absurd cooking image]`
3. `Main opp: [real biggest threat and its due time]`
4. One specific 25-minute first move that reduces the threat
5. When useful: `Want a mildly disrespectful lock-in call at [suggested time]?`

Example tone:

```text
COOKED SCORE: 87% 🔥
Status: charcoal with academic seasoning
Main opp: CSE 310 project due tomorrow at 11:59 PM
Plot armor: spend 25 minutes making the outline at 3:05.
Want a mildly disrespectful lock-in call at 3:05?
```

Keep the entire reply under 420 characters. Use one roast line, not a paragraph. Vary the cooking image instead of repeating the same joke. Roast the workload or the student's procrastination, never their identity, ability, body, finances, disability, mental health, grief, or serious circumstances. If the student sounds distressed, drop the roast and give a calm next step.

Choose a first move that can genuinely begin in 25 minutes, such as opening the assignment instructions, making an outline, completing the first problem, or reviewing one lecture. Do not promise that the action mathematically lowers the score unless rerunning the rubric confirms it.

## Write the aura reply

Send one plain-text iMessage with four short lines:

1. `AURA SCORE: [score]/100 [emoji]`
2. `Status: [aura level plus one fresh joke]`
3. `Aura gained: [strongest real positive signal]`
4. `Aura tax: [strongest real negative signal, or "no overdue work detected"]`

Example tone:

```text
AURA SCORE: 80/100 ✨
Status: campus main character with the syllabus receipts
Aura gained: 2 assignments already submitted
Aura tax: quiz still open with 8 hours left
```

Keep it under 360 characters. Mention only signals present in the score calculation. If no positive signal exists, say `Aura gained: attendance pending` rather than inventing one. Roast behavior lightly; never turn the score into a judgment of the student's worth or identity.

## Lock-in call

Cubbie can call only its own student. It cannot text or call friends on the student's behalf.

Suggest a time that falls inside a real free calendar block. Before scheduling any reminder or call, ask the student and wait for an explicit yes. After approval, schedule one call that names the biggest threat and the 25-minute first move. Keep the call playful and brief.

