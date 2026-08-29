"""Fills in full per-topic explanation + reference video for every topic of ONE course
that already has a topic outline (see seed_topics_broad.py) -- the deeper, more
expensive pass beyond just titles. Reuses the exact same functions the admin UI's
per-topic "Fetch YouTube video" / "Generate explanation draft" buttons call
(routes/admin_academia_routes.py), just scripted across a whole course instead of one
topic at a time by hand.

Every topic keeps content_source='ai_draft' -- draft, review-pending content, same as
the admin UI's own generated drafts. This script does NOT mark anything 'reviewed';
that stays an explicit admin action (editing/saving in /admin/academia/courses/<id>).

Requires OPENROUTER_API_KEY and YOUTUBE_API_KEY, and network access -- calls two real,
billed/quota'd APIs per topic. Does NOT run automatically.

Usage:
    python seed_topic_content_for_course.py --course-id 91           # dry run
    python seed_topic_content_for_course.py --course-id 91 --apply    # generate + persist
"""
import sys
import time

APPLY = '--apply' in sys.argv
FORCE = '--force' in sys.argv  # regenerate explanations even if one already exists
COURSE_ID = None
for i, arg in enumerate(sys.argv):
    if arg == '--course-id' and i + 1 < len(sys.argv):
        COURSE_ID = int(sys.argv[i + 1])

if not COURSE_ID:
    print("Usage: python seed_topic_content_for_course.py --course-id <id> [--apply]")
    sys.exit(1)


def main():
    from app import app, db
    from models import Course, Topic
    from services.ai_service import generate_topic_explanation
    from services.youtube_service import search_youtube_videos, build_topic_video_query

    with app.app_context():
        course = Course.query.get(COURSE_ID)
        if not course:
            print(f"Course id={COURSE_ID} not found")
            return

        topics = course.topics.order_by(Topic.order).all()
        todo = topics if FORCE else [t for t in topics if not t.explanation]
        print(f"{course.code} ({course.department.name}) — {course.title}: "
              f"{len(topics)} topics, {len(todo)} still need an explanation.")

        if not APPLY:
            for t in todo:
                print(f"  would generate: {t.title}")
            print("\nDry run only. Re-run with --apply.")
            return

        for i, topic in enumerate(todo):
            try:
                if topic.videos is None:
                    query = build_topic_video_query(course.code, course.title, topic.title)
                    result = search_youtube_videos(query)
                    if result is not None:
                        topic.videos = result
                        db.session.commit()

                video = topic.videos[0] if topic.videos else None
                content = generate_topic_explanation(course.code, course.title, topic.title, video=video)
                topic.explanation = content
                db.session.commit()
                print(f"[{i + 1}/{len(todo)}] {topic.title} -- video: {'yes' if video else 'no'}")
            except Exception as e:
                print(f"[FAIL] {topic.title}: {e}")
            time.sleep(0.3)

        print("\nDONE.")


if __name__ == '__main__':
    main()
