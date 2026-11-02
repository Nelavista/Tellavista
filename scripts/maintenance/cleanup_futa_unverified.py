"""Remove FUTA taxonomy rows that FUTA's own website doesn't list (follow-up to
scripts/seed/seed_futa_official.py): the seed_ccmas_core.py departments FUTA has no such
department for, and faculties that seed left empty.

A department is removed only when NOTHING refers to it -- no FUTA student or material names it,
and none of its courses has topics, enrollments, CBT questions/attempts, materials or tutor
conversations. Anything still in use is listed with its counts and kept (e.g. a student who
picked "Botany" keeps a valid profile until they choose FUTA's real department). Deleting a
department takes its unused CCMAS course rows with it (Department.courses cascade).

Default is a DRY RUN. Pass --apply to delete.

Usage:
    python -m scripts.maintenance.cleanup_futa_unverified
    python -m scripts.maintenance.cleanup_futa_unverified --apply
"""
import sys

from app import app, db
from app.models import (CBTAttempt, CBTQuestion, Course, Department, Enrollment, Faculty, Material,
                        Topic, TutorConversation, University, User)
from scripts.seed.seed_futa_official import FUTA, SCHOOLS


def _usage(dept, uni):
    course_ids = [c.id for c in Course.query.filter_by(department_id=dept.id)]
    by_course = lambda model: model.query.filter(model.course_id.in_(course_ids)).count() if course_ids else 0
    usage = {
        'students': User.query.filter_by(university=uni.name, department=dept.name).count(),
        'materials': Material.query.filter(db.or_(Material.department_id == dept.id,
                                                  db.and_(Material.university == uni.name,
                                                          Material.department == dept.name))).count()
                     + by_course(Material),
        'topics': by_course(Topic),
        'enrollments': by_course(Enrollment),
        'cbt_questions': CBTQuestion.query.filter_by(department_id=dept.id).count() + by_course(CBTQuestion),
        'cbt_attempts': by_course(CBTAttempt),
        'tutor_conversations': by_course(TutorConversation),
    }
    return {k: v for k, v in usage.items() if v}, len(course_ids)


def cleanup(apply):
    with app.app_context():
        uni = University.query.filter_by(name=FUTA).first()
        if not uni:
            sys.exit(f'{FUTA} not found')
        official_depts = {name.lower() for depts in SCHOOLS.values() for name in depts}

        removed = 0
        for dept in Department.query.join(Faculty).filter(Faculty.university_id == uni.id).order_by(Department.name):
            if dept.name.lower() in official_depts:
                continue
            usage, n_courses = _usage(dept, uni)
            if usage:
                print(f'KEEP   {dept.name} ({dept.faculty.name}) -- in use: '
                      + ', '.join(f'{k} {v}' for k, v in usage.items()))
                continue
            print(f'REMOVE {dept.name} ({dept.faculty.name}) with its {n_courses} unused courses')
            db.session.delete(dept)
            removed += 1
        db.session.flush()

        for fac in Faculty.query.filter_by(university_id=uni.id).order_by(Faculty.name):
            if fac.name in SCHOOLS or Department.query.filter_by(faculty_id=fac.id).count():
                continue
            if CBTQuestion.query.filter_by(faculty_id=fac.id).count():
                print(f'KEEP   faculty {fac.name} -- referenced by CBT questions')
                continue
            print(f'REMOVE faculty {fac.name} (no departments left)')
            db.session.delete(fac)
            removed += 1

        print(f'{"APPLY" if apply else "DRY RUN"}: {removed} rows to remove')
        if apply:
            db.session.commit()
        else:
            db.session.rollback()


if __name__ == '__main__':
    cleanup('--apply' in sys.argv)
