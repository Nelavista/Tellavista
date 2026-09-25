# LASU CBT question-bank authoring spec (shared across all batches)

This file is internal working material for the content pipeline (not seeded into the
app). Output: one JSON file per course code at
`C:\Users\PC\Documents\Tellavista\data\cbt_question_banks\lasu\<CODE>.json`

Shape for a normal (exam) course:
```json
{
  "course_code": "CSC101",
  "title": "Introduction to Computer Science",
  "level": "100",
  "source_note": "One or two sentences: what grounded this bank.",
  "questions": [
    {
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "correct_answer": "... (must be copied EXACTLY, character-for-character, from one of the options)",
      "explanation": "1-2 sentences: WHY that answer is correct.",
      "topic": "short topic label within the course, e.g. 'Number systems'",
      "difficulty": "easy" | "medium" | "hard"
    }
  ]
}
```

Shape for a SIWES / Research Project / Seminar course: same top-level shape, but each
question item is `{ "question": "...", "mark_scheme": "...", "topic": "..." }` (no
options/correct_answer/explanation/difficulty). All of these are already done -- do not
author any *399/*499/seminar codes unless explicitly asked.

## Rules (non-negotiable)
1. Every question must be something a LASU student in that exact course would actually
   need to know -- grounded in real, standard content of that course, at the stated
   level. Use your own accurate domain knowledge of standard Nigerian university
   (NUC-aligned) curricula; if genuinely unsure of a fact, drop the question rather than
   invent it.
2. Exactly one correct answer per MCQ; `correct_answer` copied verbatim from `options`.
   No duplicate options, no two arguably-correct options. 4 options unless the subject
   genuinely needs fewer (never fewer than 3).
3. No filler, no reworded repeats, no two questions testing the same single fact. Cover
   the course's real spread of major topics.
4. Mix styles: definition/concept, understanding, application, calculation (where the
   subject has computation), scenario-based, theory, practical/lab-oriented for
   practical courses.
5. Volume: 30+ per course normally; 50 for 100-level/GST courses where the subject
   supports it. If you can't reach the target without padding/fabricating, write fewer
   and say so in source_note.
6. Do not invent LASU-specific facts (dates, staff, buildings, policy numbers) you're
   not certain of. General factual/scientific content is expected -- that's the subject.
7. Keep adjacent courses in a sequence (I/II/III) distinct -- don't repeat content
   across them.
8. Self-check each file before finishing: valid JSON, no duplicate `question` text,
   `correct_answer` present verbatim in `options`.

Write every file directly with the Write tool. Author all assigned courses and report
back a one-line-per-course summary (code, question count, shortfalls + why). Do not ask
for confirmation partway through.
