# How Cooked Am I?

A tiny Cubbie Skill that checks a student's real Canvas deadlines and free calendar time, calculates a transparent workload-pressure score, and replies with one playful roast plus one useful 25-minute next move.

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

## Install

Install this repository as an Agent Skill in Cubbie, then text:

```text
cubbie how cooked am i
```

Canvas provides assignments and due dates. Google Calendar makes the score and suggested lock-in time more useful. If Calendar is unavailable, the Skill can still score Canvas deadlines.

## Local test

The scorer uses only the Python standard library.

```bash
python3 scripts/cook.py --input assets/sample_workload.json
python3 -m unittest discover -s tests -v
```

The full Canvas, Calendar, iMessage, and call flow must be tested inside Cubbie.

## Privacy

The scorer reads a temporary JSON input and prints a result. It does not persist workload data or call external services.

