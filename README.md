# How Cooked Am I? + Aura Check

A tiny Cubbie Skill with two student status checks powered by real Canvas deadlines and Calendar data.

```text
STUDENT STATUS MENU
1. How Cooked Am I? 🔥
2. Aura Check ✨
Reply 1 or 2.
```

## Example

> **Student:** cubbie how cooked am i
>
> **Cubbie:**  
> COOKED SCORE: 87% 🔥  
> Status: charcoal with academic seasoning  
> Main opp: CSE 310 project due tomorrow at 11:59 PM  
> Plot armor: spend 25 minutes making the outline at 3:05.  
> Want a mildly disrespectful lock-in call at 3:05?

The score measures near-term workload pressure for entertainment. It does not predict grades.

Aura Check starts at 50 and moves only from visible academic signals: submitted upcoming work, planned focus time, overdue work, and open work due within 24 hours. It rates academic momentum for fun, not the student's worth or personality.

## Install

Install this repository as an Agent Skill in Cubbie, then text:

```text
cubbie rate me
cubbie how cooked am i
cubbie check my aura
```

Canvas provides assignments and due dates. Google Calendar makes the score and suggested lock-in time more useful. If Calendar is unavailable, the Skill can still score Canvas deadlines.

## Local test

The scorer uses only the Python standard library.

```bash
python3 scripts/cook.py --mode cooked --input assets/sample_workload.json
python3 scripts/cook.py --mode aura --input assets/sample_workload.json
python3 -m unittest discover -s tests -v
```

The full Canvas, Calendar, iMessage, and call flow must be tested inside Cubbie.

## Privacy

The scorer reads a temporary JSON input and prints a result. It does not persist workload data or call external services.

