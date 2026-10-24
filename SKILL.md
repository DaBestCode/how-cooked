---
name: how-cooked
description: Rates how academically cooked a student is from their upcoming Canvas work and calendar, then gives one playful roast and one useful next move. Use when a student asks "how cooked am I?", wants a cooked score, or wants a funny workload reality check.
---

# How Cooked Am I?

Give the student a fast, funny workload reality check based on real deadlines and available time. Keep it light, accurate, and short enough to screenshot.

## When to use

Use this skill when the student asks how cooked they are, requests a cooked score, or wants their academic workload roasted.

Default to the next 72 hours. If the student says "this week" or gives another time range, use that range and mention it in the reply.

## Gather the workload

1. Read the student's Canvas assignments and due dates for the requested window.
2. Exclude work that Canvas clearly marks as submitted or complete.
3. Read Google Calendar for open time before the nearest deadlines.
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

## Lock-in call

Cubbie can call only its own student. It cannot text or call friends on the student's behalf.

Suggest a time that falls inside a real free calendar block. Before scheduling any reminder or call, ask the student and wait for an explicit yes. After approval, schedule one call that names the biggest threat and the 25-minute first move. Keep the call playful and brief.

