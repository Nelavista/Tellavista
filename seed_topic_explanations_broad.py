"""Populates the written explanation (via generate_topic_explanation) for every Topic
that doesn't have one yet. This is the fix for "Nelavista hasn't written an explanation
for this topic yet": seed_topics_broad.py already gave every course a real topic outline,
but the outline alone is just titles -- a student opening any individual topic still saw
this empty state, which is now the default experience across ~92% of topics rather than
the rare exception.

Deliberately text-only, no reference video. Pairing a video (see
routes/admin_academia_routes.py's generate_topic_explanation_draft, which calls
search_youtube_videos first) doesn't scale here: YouTube Data API's default quota is
10,000 units/day and a single search.list call costs 100 units, i.e. ~100 searches/day --
against 59,000+ topics that's not a background job, it's a multi-year one. Video pairing
stays a per-topic, on-demand admin action (or a separately-scoped, quota-budgeted batch
pass); this script only fills in the text.

Every explanation this script writes is content_source='ai_draft' on a Topic whose title
was itself already ai_draft from seed_topics_broad.py -- draft, review-pending content,
same convention throughout. Idempotent: skips any topic that already has a non-empty
explanation, so re-running after a partial run (rate limit, network blip, credit
exhaustion) only fills in what's left.

Requires OPENROUTER_API_KEY and network access -- this calls a real, billed AI API. Does
NOT run automatically; review the dry-run plan, then re-run with --apply.

Usage:
    python seed_topic_explanations_broad.py                    # dry run: prints scope
    python seed_topic_explanations_broad.py --apply             # generate + persist
    python seed_topic_explanations_broad.py --apply --limit 50  # cap this run's count
    python seed_topic_explanations_broad.py --apply --course CSC201   # one course's topics
"""
import sys

APPLY = '--apply' in sys.argv
LIMIT = None
ONLY_COURSE_CODE = None
for i, arg in enumerate(sys.argv):
    if arg == '--limit' and i + 1 < len(sys.argv):
        LIMIT = int(sys.argv[i + 1])
    if arg == '--course' and i + 1 < len(sys.argv):
        ONLY_COURSE_CODE = sys.argv[i + 1].strip().upper()


def main():
    from app import app, db
    from models import Topic, Course
    from services.ai_service import generate_topic_explanation

    with app.app_context():
        query = Topic.query.filter(db.or_(Topic.explanation.is_(None), Topic.explanation == ''))
        if ONLY_COURSE_CODE:
            query = query.join(Course).filter(db.func.upper(Course.code) == ONLY_COURSE_CODE)
        topic_ids = [t.id for t in query.order_by(Topic.course_id, Topic.order).all()]

        if LIMIT:
            topic_ids = topic_ids[:LIMIT]

        print(f"{len(topic_ids)} topic(s) with no explanation yet, in scope for this run.")
        if not APPLY:
            print("\nDry run only -- no AI calls made, no changes written. Re-run with --apply.")
            return

        succeeded = failed = 0
        for i, topic_id in enumerate(topic_ids):
            topic = db.session.get(Topic, topic_id)
            course = topic.course
            code, title, topic_title = course.code, course.title, topic.title
            try:
                content = generate_topic_explanation(code, title, topic_title)
                topic.explanation = content
                if not topic.content_source:
                    topic.content_source = 'ai_draft'
                db.session.commit()
                succeeded += 1
            except Exception as e:
                # Same session-recovery pattern as seed_topics_broad.py: rollback can
                # itself fail after a dropped connection, and code/title/topic_title were
                # captured before the AI call so this print never touches a possibly-
                # detached object.
                try:
                    db.session.rollback()
                except Exception:
                    db.session.remove()
                print(f"[FAIL] {code} / {topic_title}: {e}")
                failed += 1
                continue

            if (i + 1) % 20 == 0:
                print(f"[{i + 1}/{len(topic_ids)}] ok={succeeded} failed={failed} -- last: {code} / {topic_title}")

        print(f"\nDONE. {succeeded} topic(s) seeded with explanations, {failed} failed.")


if __name__ == '__main__':
    main()
