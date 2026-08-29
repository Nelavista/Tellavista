"""Fills in full per-topic explanation + reference video for EVERY topic of EVERY
course that already has a topic outline (see seed_topics_broad.py) -- the broad,
all-courses version of seed_topic_content_for_course.py's single-course pass.

Idempotent and resumable: only processes topics with explanation IS NULL, commits
after each topic, and can be killed/re-run at any point without redoing finished work
or duplicating anything. A single topic/course failure (AI timeout, transient network
error, YouTube quota) is caught, logged, and skipped -- it never aborts the run.

Requires OPENROUTER_API_KEY and YOUTUBE_API_KEY, and network access -- calls two real,
billed/quota'd APIs per topic. Does NOT run automatically.

Usage:
    python seed_topic_content_all_courses.py            # dry run -- shows scope only
    python seed_topic_content_all_courses.py --apply     # generate + persist, all courses
    python seed_topic_content_all_courses.py --apply --limit 50   # first 50 courses only
"""
import sys
import time

APPLY = '--apply' in sys.argv
LIMIT = None
SHARD_INDEX = None
SHARD_COUNT = None
for i, arg in enumerate(sys.argv):
    if arg == '--limit' and i + 1 < len(sys.argv):
        LIMIT = int(sys.argv[i + 1])
    if arg == '--shard' and i + 1 < len(sys.argv):
        # "2/6" = this is worker 2 of 6 -- each worker takes every 6th course by id,
        # offset by its index, so N parallel invocations can safely split the work with
        # zero overlap (courses, not topics, are the sharding unit -- one course is never
        # touched by two workers). Purely a wall-clock speedup: this doesn't raise
        # YouTube's daily quota ceiling, it just spends it faster across workers.
        SHARD_INDEX, SHARD_COUNT = (int(x) for x in sys.argv[i + 1].split('/'))


def main():
    from sqlalchemy import func
    from app import app, db
    from models import Course, Topic
    from services.ai_service import generate_topic_explanation
    from services.youtube_service import search_youtube_videos, build_topic_video_query

    with app.app_context():
        # Every course with >=1 topic missing an explanation, ordered so partially-done
        # courses (from an earlier interrupted run) are picked up before untouched ones.
        course_ids = [
            row[0] for row in
            db.session.query(Topic.course_id)
            .filter(Topic.explanation.is_(None))
            .distinct()
            .all()
        ]
        courses = Course.query.filter(Course.id.in_(course_ids)).order_by(Course.id).all()
        if SHARD_COUNT:
            courses = [c for c in courses if c.id % SHARD_COUNT == SHARD_INDEX]
        if LIMIT:
            courses = courses[:LIMIT]

        total_topics_remaining = (
            db.session.query(func.count(Topic.id))
            .filter(Topic.course_id.in_([c.id for c in courses]), Topic.explanation.is_(None))
            .scalar()
        )
        print(f"{len(courses)} courses, {total_topics_remaining} topics still need content.")

        if not APPLY:
            print("Dry run only. Re-run with --apply.")
            return

        done_courses = 0
        done_topics = 0
        failed_topics = 0
        t_start = time.time()

        for ci, course in enumerate(courses):
            topics = course.topics.order_by(Topic.order).filter(Topic.explanation.is_(None)).all()
            for topic in topics:
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
                    done_topics += 1
                except Exception as e:
                    db.session.rollback()
                    failed_topics += 1
                    print(f"  [FAIL] {course.code} / {topic.title}: {e}")
                time.sleep(0.2)

            done_courses += 1
            elapsed = time.time() - t_start
            print(f"[{ci + 1}/{len(courses)}] {course.code} ({course.department.name}) done "
                  f"-- {done_topics} topics ok, {failed_topics} failed, {elapsed:.0f}s elapsed")

        print(f"\nDONE. {done_courses} courses processed, {done_topics} topics filled, "
              f"{failed_topics} failed, {time.time() - t_start:.0f}s total.")


if __name__ == '__main__':
    main()
