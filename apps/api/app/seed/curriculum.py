"""The AI Data Annotation curriculum (F7).

One skill, one learning path, five lessons, five task types (with practice
samples and expected answers), one assessment with five gold tasks, and one
practical task with a rubric. The same skill is the first one a student can be
verified in, so the content here is the honest minimum: what annotation is, how a
guideline becomes a decision, and where quality comes from.

Authoring decisions come from G4: Nelavista owns the curriculum, it is authored
in house and published under the Nelavista Contributor Licence 1.0. The task
types are the five the engine already validates (`exact_key`, `label_set`,
`span_overlap`, `ranking`, `numeric_tolerance`) so adding content needed no new
code.

Everything is idempotent and keyed by a stable slug or title. Re-running the seed
updates nothing that already exists; it only fills gaps. The local seed also
creates a matching AID301 course with topics, material chunks and CBT questions so
the Academia and Ask screens have real content to read and search.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.academia import Course, Material, MaterialChunk, Question, Topic
from app.models.skills import (
    STATUS_PUBLISHED,
    LearningPath,
    LearningPathStep,
    Lesson,
    Skill,
    SkillCategory,
    TaskTemplate,
)
from app.models.verification import Assessment, AssessmentTask, PracticalTask

SKILL_SLUG = "ai-data-annotation"
PATH_SLUG = "ai-data-annotation-foundations"
ASSESSMENT_SLUG = "ai-data-annotation-verification"
PRACTICAL_SLUG = "annotation-quality-audit"
COURSE_CODE = "AID301"

# --- lessons -----------------------------------------------------------------

LESSONS: list[dict] = [
    {
        "slug": "annotation-why-quality-matters",
        "title": "What data annotation is, and why quality is the product",
        "estimated_minutes": 20,
        "body_md": """# What data annotation is

Data annotation is the work of turning raw material — a message, an image, a
recording, a document — into examples a model can learn from. The model is only
as good as the examples, so annotation is not clerical work around the product:
it **is** the product's raw material.

## The three questions every task answers

- **What is being labelled?** A whole item, a span inside it, or a relationship
  between two items.
- **Which labels are allowed?** The taxonomy in the guideline, not a synonym you
  prefer.
- **What counts as correct?** The decision rule, including what to do when two
  labels seem to fit.

## Why "looks right" is not enough

A label that feels right but breaks the guideline teaches the model the wrong
rule at scale. Two annotators who disagree usually are not careless: one is
following a different reading of the guideline. That is a **guideline defect**,
and the fix is an escalation, not a quiet guess.

## What this path asks of you

Read the guideline before the data. Label the item, not your impression of the
item. When the guideline does not decide, say so and escalate.
""",
    },
    {
        "slug": "annotation-reading-a-guideline",
        "title": "Reading a guideline and applying a label taxonomy",
        "estimated_minutes": 25,
        "body_md": """# From guideline to decision

A usable guideline has four parts:

1. **Scope** — what the task covers and what it excludes.
2. **Taxonomy** — every allowed label, with a one-line definition.
3. **Decision rules** — the order in which labels win when more than one applies.
4. **Edge cases** — the examples the team has already argued about, and the
   answer they settled on.

## Apply the rules in order

When two labels both seem plausible, the guideline's priority order decides. If
there is no priority order, the item is ambiguous and should be escalated rather
than forced into a label.

## The label must be in the taxonomy

`Refund request` and `Billing question` may mean the same thing to a reader, but
only one of them is in the taxonomy. Free text is not a label, and a near-synonym
is a defect even when it is more descriptive.

## Practice habit

Before labelling a batch, restate the decision rule in one sentence. If you cannot
restate it, you are guessing.
""",
    },
    {
        "slug": "annotation-classification",
        "title": "Classifying items: one label or several",
        "estimated_minutes": 30,
        "body_md": """# Classification

Classification assigns labels to a whole item. There are two shapes:

- **Single-label**: exactly one label is correct. A support ticket is a billing
  issue or a bug report, not both.
- **Multi-label**: every label that applies is correct, and the set matters. A
  product review can be about delivery *and* quality.

## Single-label discipline

For single-label work the labels must be mutually exclusive. If two labels can
both be true, the taxonomy is wrong or the task is multi-label. Do not "pick the
closest" silently.

## Multi-label discipline

Submit exactly the labels that apply — no more, no fewer. Adding a label "just in
case" is as wrong as missing one. The validator compares the set, not the order.

## A worked example

> The parcel arrived three days late and the box was crushed, though the item
> itself works.

Labels: `delivery` and `packaging`. Not `quality`, because the item works. The
distinction is the guideline's, not a feeling about the sentence.
""",
    },
    {
        "slug": "annotation-span-tagging",
        "title": "Span tagging: marking the exact words",
        "estimated_minutes": 30,
        "body_md": """# Span tagging

A span is a contiguous run of characters inside the text, with a label. It is
defined by **where it starts and where it ends**, not by what it means in the
sentence.

## Boundaries are the task

If the guideline says to mark the full organisation name, mark `Lagos Test
University`, not `Lagos`. If it says to mark the person only, do not include their
job title.

## Overlap

Two spans may touch but should not overlap unless the guideline explicitly allows
nested entities. Overlapping spans usually mean one annotator marked a phrase and
another marked the word inside it.

## Why offsets matter

An offset pair is checkable: a reviewer can highlight the exact text. A quoted
string is not, because it can appear more than once. Mark the occurrence the
guideline points at.

## Practice

Read the sentence once for meaning, then once for boundaries. The second read is
where most span errors are caught.
""",
    },
    {
        "slug": "annotation-edge-cases",
        "title": "Ambiguity, disagreement and escalation",
        "estimated_minutes": 25,
        "body_md": """# When the guideline runs out

Real data contains items the guideline did not anticipate. The professional move
is not to invent a rule; it is to make the ambiguity visible.

## Escalate, do not improvise

Escalate when:

- two labels fit and the priority order does not decide;
- the text is truncated or unreadable;
- the item is in a language the guideline does not cover;
- applying the rule would produce an obviously harmful label.

## Disagreement is data

Inter-annotator disagreement is a signal about the guideline. Record what each
annotator saw. A team that resolves disagreement with a written rule gets better;
a team that resolves it by seniority gets quieter, not better.

## Quality checks

Gold tasks are items with a known answer, mixed into the queue. They catch drift.
Failing one is not punishment: it is a prompt to reread the guideline before the
next batch.

## The standard

A label you cannot defend from the guideline is not finished work, even if it is
the label everyone else chose.
""",
    },
]

# --- task templates ----------------------------------------------------------

CLASSIFICATION_OPTIONS = [
    {"key": "A", "label": "Product question"},
    {"key": "B", "label": "Billing or refund"},
    {"key": "C", "label": "Bug report"},
    {"key": "D", "label": "Spam or promotion"},
]

TEMPLATES: list[dict] = [
    {
        "slug": "annotation-single-label",
        "name": "Single-label classification",
        "instructions_md": (
            "Read the message and choose the one label the guideline's priority order "
            "selects. If no label fits, do not guess: escalate."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The item to classify."},
            },
            "options": CLASSIFICATION_OPTIONS,
        },
        "answer_schema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "enum": [option["key"] for option in CLASSIFICATION_OPTIONS]},
            },
            "required": ["key"],
        },
        "validator": "exact_key",
        "config": {
            "sample": (
                "Sample: “I was charged twice for the same order and I need one of the "
                "payments reversed.” → Billing or refund."
            ),
            "expected_answer": {"key": "B"},
        },
    },
    {
        "slug": "annotation-multi-label",
        "name": "Multi-label classification",
        "instructions_md": (
            "Select every label that applies and nothing else. The set is compared, "
            "not the order; an extra label is as wrong as a missing one."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The item to label."},
            },
            "labels": ["delivery", "packaging", "product quality", "price", "support"],
        },
        "answer_schema": {
            "type": "object",
            "properties": {
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "enum": ["delivery", "packaging", "product quality", "price", "support"],
                },
            },
            "required": ["labels"],
        },
        "validator": "label_set",
        "config": {
            "sample": (
                "Sample: “Arrived two days late and the box was crushed, but the item "
                "works and support answered quickly.” → delivery, packaging, support."
            ),
            "expected_answer": {"labels": ["delivery", "packaging", "support"]},
        },
    },
    {
        "slug": "annotation-span-tagging",
        "name": "Entity span tagging",
        "instructions_md": (
            "Mark the exact character span for each entity the guideline names. "
            "Boundaries matter: mark the full name, not part of it."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The text to mark up."},
            },
            "labels": ["organisation", "person", "location"],
        },
        "answer_schema": {
            "type": "object",
            "properties": {
                "spans": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "start": {"type": "integer"},
                            "end": {"type": "integer"},
                            "label": {"type": "string"},
                        },
                        "required": ["start", "end", "label"],
                    },
                },
            },
            "required": ["spans"],
        },
        "validator": "span_overlap",
        "config": {
            "min_overlap": 0.5,
            "sample": (
                "Sample: text “Ada met the Lagos team at Zenith Bank.” with spans for "
                "Ada (person), Lagos (location) and Zenith Bank (organisation)."
            ),
            "expected_answer": {
                "spans": [
                    {"start": 0, "end": 3, "label": "person"},
                    {"start": 12, "end": 17, "label": "location"},
                    {"start": 26, "end": 37, "label": "organisation"},
                ]
            },
        },
    },
    {
        "slug": "annotation-priority-ranking",
        "name": "Priority ranking",
        "instructions_md": (
            "Put the items in the order the guideline's severity rule requires, most "
            "urgent first. Every item appears exactly once."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Why the queue needs ordering."},
            },
            "items": [
                "Payment taken twice",
                "App crashes on launch",
                "Typo in the help article",
                "Wrong delivery address",
            ],
        },
        "answer_schema": {
            "type": "object",
            "properties": {
                "order": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "required": ["order"],
        },
        "validator": "ranking",
        "config": {
            "sample": (
                "Sample: money errors first, then blocked access, then wrong delivery, "
                "then documentation."
            ),
            "expected_answer": {
                "order": [
                    "Payment taken twice",
                    "App crashes on launch",
                    "Wrong delivery address",
                    "Typo in the help article",
                ]
            },
        },
    },
    {
        "slug": "annotation-count-numeric",
        "name": "Numeric extraction",
        "instructions_md": (
            "Extract the whole number the guideline asks for. Do not include units, "
            "currency symbols or words. Enter digits only."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The text to read."},
            },
        },
        "answer_schema": {
            "type": "object",
            "properties": {"value": {"type": "integer"}},
            "required": ["value"],
        },
        "validator": "numeric_tolerance",
        "config": {
            "tolerance": 0,
            "sample": "Sample: “The batch contains 24 duplicate rows.” → 24.",
            "expected_answer": {"value": 24},
        },
    },
]

# --- assessment gold tasks ---------------------------------------------------

ASSESSMENT_TASKS: list[dict] = [
    {
        "ordinal": 1,
        "template_slug": "annotation-single-label",
        "points": 1,
        "payload": {
            "prompt": "The export button shows an error and nothing downloads. Which label applies?",
            "options": CLASSIFICATION_OPTIONS,
        },
        "expected_answer": {"key": "C"},
    },
    {
        "ordinal": 2,
        "template_slug": "annotation-multi-label",
        "points": 1,
        "payload": {
            "prompt": (
                "The jacket is excellent and arrived early, but it was more expensive "
                "than the listing first showed."
            ),
            "labels": ["delivery", "packaging", "product quality", "price", "support"],
        },
        "expected_answer": {"labels": ["delivery", "product quality", "price"]},
    },
    {
        "ordinal": 3,
        "template_slug": "annotation-span-tagging",
        "points": 1,
        "payload": {
            "prompt": "Chidi met Ada at Zenith Bank in Lagos.",
            "labels": ["organisation", "person", "location"],
        },
        "expected_answer": {
            "spans": [
                {"start": 0, "end": 5, "label": "person"},
                {"start": 10, "end": 13, "label": "person"},
                {"start": 17, "end": 28, "label": "organisation"},
                {"start": 32, "end": 37, "label": "location"},
            ]
        },
    },
    {
        "ordinal": 4,
        "template_slug": "annotation-priority-ranking",
        "points": 1,
        "payload": {
            "prompt": "Order the queue by the guideline's severity rule, most urgent first.",
            "items": [
                "Label leaks personal data",
                "Two annotators disagree",
                "Guideline missing an example",
                "Dashboard is slow",
            ],
        },
        "expected_answer": {
            "order": [
                "Label leaks personal data",
                "Two annotators disagree",
                "Guideline missing an example",
                "Dashboard is slow",
            ]
        },
    },
    {
        "ordinal": 5,
        "template_slug": "annotation-count-numeric",
        "points": 1,
        "payload": {
            "prompt": "The review queue holds 37 items, of which 12 are gold tasks. How many are live items?",
        },
        "expected_answer": {"value": 25},
    },
]

# --- course content for the Academia screens ---------------------------------

TOPICS: list[str] = [
    "Foundations of annotation",
    "Classification labels",
    "Entity spans",
    "Quality and edge cases",
]

MATERIALS: list[dict] = [
    {
        "title": "AID301 — Annotation Handbook",
        "source": "seed",
        "chunks": [
            (
                "Annotation turns raw text into training examples. A label is correct "
                "only when the guideline's decision rule selects it. When two labels "
                "seem to fit, apply the priority order rather than choosing the one "
                "that feels closer."
            ),
            (
                "Classification labels apply to a whole item. Single-label tasks need "
                "mutually exclusive labels: a support ticket is a billing issue or a bug "
                "report, not both. Multi-label tasks compare the set of labels, so an "
                "extra label is as wrong as a missing one."
            ),
            (
                "A span is a contiguous run of characters with a label, defined by its "
                "start and end offsets. Mark the full entity the guideline names. "
                "Overlapping spans usually mean one annotator marked a phrase and "
                "another marked the word inside it."
            ),
        ],
    },
    {
        "title": "AID301 — Quality Playbook",
        "source": "seed",
        "chunks": [
            (
                "Gold tasks are items with a known answer mixed into the queue. Failing "
                "one is a prompt to reread the guideline, not a punishment. Quality "
                "comes from consistent decisions, not from annotating faster."
            ),
            (
                "Escalate when the guideline does not decide, when the text is "
                "truncated, or when the item is in a language the guideline does not "
                "cover. Improvising a rule hides the gap and teaches the model the wrong "
                "thing at scale."
            ),
            (
                "Inter-annotator disagreement is data about the guideline. Record what "
                "each annotator saw and resolve it with a written rule. A team that "
                "resolves disagreement by seniority gets quieter, not better."
            ),
        ],
    },
    {
        "title": "AID301 — Past Questions",
        "source": "seed",
        "chunks": [
            (
                "Practice question: a customer writes that a parcel arrived late and the "
                "box was crushed but the item works. The applicable labels are delivery "
                "and packaging, not product quality, because the item itself works."
            ),
            (
                "Practice question: text “Ada met the Lagos team at Zenith Bank” contains "
                "a person (Ada), a location (Lagos) and an organisation (Zenith Bank). "
                "The span boundaries are the exact words, not the surrounding sentence."
            ),
        ],
    },
]

QUESTIONS: list[dict] = [
    {
        "topic": "Foundations of annotation",
        "prompt": "What makes an annotation label correct?",
        "options": [
            {"key": "A", "text": "The guideline's decision rule selects it"},
            {"key": "B", "text": "It is the label most annotators would choose"},
            {"key": "C", "text": "It is the most descriptive free-text phrase"},
            {"key": "D", "text": "It matches the annotator's personal judgement"},
        ],
        "correct_key": "A",
        "explanation": "Correctness is defined by the guideline, not by consensus or taste.",
    },
    {
        "topic": "Foundations of annotation",
        "prompt": "Two labels both seem to fit a single-label item. What should you do?",
        "options": [
            {"key": "A", "text": "Pick the closer-sounding label"},
            {"key": "B", "text": "Apply the guideline's priority order, or escalate"},
            {"key": "C", "text": "Submit both labels"},
            {"key": "D", "text": "Skip the item silently"},
        ],
        "correct_key": "B",
        "explanation": (
            "The priority order decides; if there is none, the item is ambiguous and "
            "should be escalated."
        ),
    },
    {
        "topic": "Classification labels",
        "prompt": "For a multi-label task, which submission is correct?",
        "options": [
            {"key": "A", "text": "Exactly the labels that apply, no more and no fewer"},
            {"key": "B", "text": "Every plausible label, to be safe"},
            {"key": "C", "text": "Only the most important label"},
            {"key": "D", "text": "A free-text description of the item"},
        ],
        "correct_key": "A",
        "explanation": "The set is compared; an extra label is as wrong as a missing one.",
    },
    {
        "topic": "Classification labels",
        "prompt": "A parcel arrives late and the box is crushed, but the item works. Which labels apply?",
        "options": [
            {"key": "A", "text": "delivery and packaging"},
            {"key": "B", "text": "product quality only"},
            {"key": "C", "text": "delivery, packaging and product quality"},
            {"key": "D", "text": "support only"},
        ],
        "correct_key": "A",
        "explanation": "The item works, so product quality does not apply; lateness and damage do.",
    },
    {
        "topic": "Entity spans",
        "prompt": "What defines a span?",
        "options": [
            {"key": "A", "text": "Its meaning in the sentence"},
            {"key": "B", "text": "Its start and end offsets plus its label"},
            {"key": "C", "text": "The number of words it contains"},
            {"key": "D", "text": "Whether a reviewer remembers quoting it"},
        ],
        "correct_key": "B",
        "explanation": "Offsets are checkable; a quoted string is not, because it can appear more than once.",
    },
    {
        "topic": "Entity spans",
        "prompt": (
            "The guideline says to mark the full organisation name. Which span is "
            "correct for “Lagos Test University”?"
        ),
        "options": [
            {"key": "A", "text": "Lagos"},
            {"key": "B", "text": "University"},
            {"key": "C", "text": "Lagos Test University"},
            {"key": "D", "text": "Test"},
        ],
        "correct_key": "C",
        "explanation": "The full organisation name is the entity; a part of it is a boundary error.",
    },
    {
        "topic": "Quality and edge cases",
        "prompt": "What is a gold task?",
        "options": [
            {"key": "A", "text": "The hardest item in the batch"},
            {"key": "B", "text": "An item with a known answer mixed into the queue"},
            {"key": "C", "text": "An item nobody has labelled yet"},
            {"key": "D", "text": "A task paid at a higher rate"},
        ],
        "correct_key": "B",
        "explanation": "Gold tasks measure drift against a known answer.",
    },
    {
        "topic": "Quality and edge cases",
        "prompt": "The guideline does not cover an item you have been given. What is the professional move?",
        "options": [
            {"key": "A", "text": "Invent a reasonable rule and continue"},
            {"key": "B", "text": "Escalate the ambiguity"},
            {"key": "C", "text": "Leave the item unlabelled without a note"},
            {"key": "D", "text": "Ask a colleague to choose and copy them"},
        ],
        "correct_key": "B",
        "explanation": "Escalation turns a gap into a written rule; improvising hides it.",
    },
]

PRACTICAL_BRIEF = """# Annotation quality audit

You are given a batch of 20 labelled items and the guideline that was used. Audit
the batch and produce a short report.

## Deliverable

1. The items you believe are mislabelled, with the guideline rule each one breaks.
2. Any guideline gap the batch exposes.
3. One concrete change to the guideline that would prevent the most common error.

Do not relabel the whole batch. The job is the audit: a precise finding is worth
more than a long list.
"""

PRACTICAL_RUBRIC = [
    {
        "name": "Evidence",
        "description": "Every claimed error cites the item and the guideline rule it breaks.",
        "weight": 40,
    },
    {
        "name": "Precision",
        "description": "Findings are real errors, not stylistic preferences.",
        "weight": 30,
    },
    {
        "name": "Guideline insight",
        "description": "The proposed change addresses the root cause of the common error.",
        "weight": 20,
    },
    {
        "name": "Clarity",
        "description": "The report is short, ordered and readable by a reviewer.",
        "weight": 10,
    },
]


def _skill(db: Session) -> tuple[Skill, bool]:
    category = db.scalar(select(SkillCategory).where(SkillCategory.slug == "ai-and-data"))
    if category is None:
        category = SkillCategory(
            slug="ai-and-data",
            name="AI & Data",
            description="Annotation, evaluation and data quality skills.",
            ordinal=1,
        )
        db.add(category)
        db.flush()

    skill = db.scalar(select(Skill).where(Skill.slug == SKILL_SLUG))
    created = skill is None
    if skill is None:
        skill = Skill(
            category_id=category.id,
            slug=SKILL_SLUG,
            name="AI Data Annotation",
            description=(
                "Turn raw text into reliable training data: apply a guideline, label "
                "classification and span tasks, and defend quality decisions."
            ),
            is_active=True,
        )
        db.add(skill)
        db.flush()
    return skill, created


def _lessons(db: Session, skill_id: int) -> tuple[dict[str, Lesson], int]:
    rows: dict[str, Lesson] = {}
    created = 0
    for spec in LESSONS:
        lesson = db.scalar(select(Lesson).where(Lesson.slug == spec["slug"]))
        if lesson is None:
            lesson = Lesson(
                skill_id=skill_id,
                slug=spec["slug"],
                title=spec["title"],
                body_md=spec["body_md"],
                estimated_minutes=spec["estimated_minutes"],
                status=STATUS_PUBLISHED,
            )
            db.add(lesson)
            db.flush()
            created += 1
        rows[spec["slug"]] = lesson
    return rows, created


def _templates(db: Session, skill_id: int) -> tuple[dict[str, TaskTemplate], int]:
    rows: dict[str, TaskTemplate] = {}
    created = 0
    for spec in TEMPLATES:
        template = db.scalar(select(TaskTemplate).where(TaskTemplate.slug == spec["slug"]))
        if template is None:
            template = TaskTemplate(
                skill_id=skill_id,
                slug=spec["slug"],
                name=spec["name"],
                instructions_md=spec["instructions_md"],
                input_schema=spec["input_schema"],
                answer_schema=spec["answer_schema"],
                validator=spec["validator"],
                config=spec["config"],
                version=1,
                status=STATUS_PUBLISHED,
            )
            db.add(template)
            db.flush()
            created += 1
        rows[spec["slug"]] = template
    return rows, created


def _path(
    db: Session,
    skill_id: int,
    lessons: dict[str, Lesson],
    templates: dict[str, TaskTemplate],
) -> tuple[LearningPath, int]:
    path = db.scalar(select(LearningPath).where(LearningPath.slug == PATH_SLUG))
    created = 0
    if path is None:
        path = LearningPath(
            skill_id=skill_id,
            slug=PATH_SLUG,
            title="AI Data Annotation: Foundations",
            summary=(
                "Read a guideline, label classification and span tasks, and defend "
                "quality decisions under review."
            ),
            level="beginner",
            estimated_hours=5,
            status=STATUS_PUBLISHED,
        )
        db.add(path)
        db.flush()
        created = 1

    steps = [
        ("lesson", "What data annotation is", {"lesson": "annotation-why-quality-matters"}),
        ("lesson", "Reading a guideline", {"lesson": "annotation-reading-a-guideline"}),
        ("practice", "Practise: single-label classification", {"template": "annotation-single-label"}),
        ("lesson", "Classifying items", {"lesson": "annotation-classification"}),
        ("practice", "Practise: multi-label classification", {"template": "annotation-multi-label"}),
        ("lesson", "Span tagging", {"lesson": "annotation-span-tagging"}),
        ("practice", "Practise: priority ranking", {"template": "annotation-priority-ranking"}),
        ("lesson", "Edge cases and escalation", {"lesson": "annotation-edge-cases"}),
        ("assessment", "Verification: AI Data Annotation", {}),
    ]
    has_steps = db.scalar(
        select(LearningPathStep.id).where(LearningPathStep.path_id == path.id).limit(1)
    )
    if has_steps is None:
        for ordinal, (kind, title, ref) in enumerate(steps, start=1):
            lesson_id = lessons[ref["lesson"]].id if "lesson" in ref else None
            template_id = templates[ref["template"]].id if "template" in ref else None
            db.add(
                LearningPathStep(
                    path_id=path.id,
                    ordinal=ordinal,
                    kind=kind,
                    title=title,
                    lesson_id=lesson_id,
                    task_template_id=template_id,
                )
            )
        db.flush()
    return path, created


def _assessment(db: Session, skill_id: int) -> tuple[Assessment, int]:
    assessment = db.scalar(select(Assessment).where(Assessment.slug == ASSESSMENT_SLUG))
    created = 0
    if assessment is None:
        assessment = Assessment(
            skill_id=skill_id,
            slug=ASSESSMENT_SLUG,
            title="AI Data Annotation verification",
            pass_threshold=80,
            max_attempts=3,
            task_count=len(ASSESSMENT_TASKS),
            status=STATUS_PUBLISHED,
        )
        db.add(assessment)
        db.flush()
        created = 1

    existing = db.scalar(
        select(AssessmentTask.id).where(AssessmentTask.assessment_id == assessment.id).limit(1)
    )
    if existing is None:
        for task in ASSESSMENT_TASKS:
            template_slug = task["template_slug"]
            # The template rows already exist because `_templates` ran first.
            template = db.scalar(select(TaskTemplate).where(TaskTemplate.slug == template_slug))
            if template is None:
                raise RuntimeError(f"assessment task needs template {template_slug!r}")
            db.add(
                AssessmentTask(
                    assessment_id=assessment.id,
                    ordinal=task["ordinal"],
                    template_id=template.id,
                    payload=task["payload"],
                    expected_answer=task["expected_answer"],
                    points=task["points"],
                )
            )
        db.flush()
    return assessment, created


def _practical(db: Session, skill_id: int) -> int:
    existing = db.scalar(select(PracticalTask).where(PracticalTask.slug == PRACTICAL_SLUG))
    if existing is not None:
        return 0
    db.add(
        PracticalTask(
            skill_id=skill_id,
            slug=PRACTICAL_SLUG,
            title="Annotation quality audit",
            brief_md=PRACTICAL_BRIEF,
            rubric=PRACTICAL_RUBRIC,
            status=STATUS_PUBLISHED,
        )
    )
    db.flush()
    return 1


def _course(db: Session, department_id: int) -> tuple[Course, dict[str, Topic], int, int, int]:
    course = db.scalar(
        select(Course).where(
            Course.department_id == department_id,
            Course.code == COURSE_CODE,
            Course.level == "300",
        )
    )
    created_course = 0
    if course is None:
        course = Course(
            department_id=department_id,
            code=COURSE_CODE,
            title="AI Data Annotation Practice",
            level="300",
        )
        db.add(course)
        db.flush()
        created_course = 1

    topics: dict[str, Topic] = {}
    created_topics = 0
    for ordinal, title in enumerate(TOPICS, start=1):
        topic = db.scalar(
            select(Topic).where(Topic.course_id == course.id, Topic.ordinal == ordinal)
        )
        if topic is None:
            topic = Topic(course_id=course.id, title=title, ordinal=ordinal)
            db.add(topic)
            db.flush()
            created_topics += 1
        topics[title] = topic

    created_materials = 0
    created_questions = 0
    for spec in MATERIALS:
        material = db.scalar(
            select(Material).where(
                Material.course_id == course.id, Material.title == spec["title"]
            )
        )
        if material is None:
            material = Material(course_id=course.id, title=spec["title"], source=spec["source"])
            db.add(material)
            db.flush()
            created_materials += 1
            for ordinal, content in enumerate(spec["chunks"], start=1):
                db.add(
                    MaterialChunk(
                        material_id=material.id,
                        ordinal=ordinal,
                        content=content,
                        token_count=len(content.split()),
                    )
                )

    for spec in QUESTIONS:
        exists = db.scalar(
            select(Question.id).where(
                Question.course_id == course.id, Question.prompt == spec["prompt"]
            )
        )
        if exists is None:
            topic = topics.get(spec["topic"])
            db.add(
                Question(
                    course_id=course.id,
                    topic_id=topic.id if topic else None,
                    prompt=spec["prompt"],
                    options=spec["options"],
                    correct_key=spec["correct_key"],
                    explanation=spec["explanation"],
                    difficulty="medium",
                    source="seed",
                    is_active=True,
                )
            )
            created_questions += 1

    db.flush()
    return course, topics, created_course, created_topics, created_materials + created_questions


def run(db: Session, department_id: int) -> dict[str, int]:
    """Create the curriculum and its matching course. Idempotent."""
    counts = {
        "skills": 0,
        "lessons": 0,
        "task_templates": 0,
        "learning_paths": 0,
        "assessments": 0,
        "practical_tasks": 0,
        "courses": 0,
        "topics": 0,
        "materials_and_questions": 0,
    }

    skill, created = _skill(db)
    counts["skills"] += int(created)

    lessons, created = _lessons(db, skill.id)
    counts["lessons"] += created

    templates, created = _templates(db, skill.id)
    counts["task_templates"] += created

    _, created = _assessment(db, skill.id)
    counts["assessments"] += created

    _, created = _path(db, skill.id, lessons, templates)
    counts["learning_paths"] += created

    counts["practical_tasks"] += _practical(db, skill.id)

    _, _, created_course, created_topics, created_content = _course(db, department_id)
    counts["courses"] += created_course
    counts["topics"] += created_topics
    counts["materials_and_questions"] += created_content

    return counts


__all__ = ["run"]
