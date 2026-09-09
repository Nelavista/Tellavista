"""One-off seed: migrates the 52 real LASU campus-map landmarks that used to live
hardcoded in templates/campus-map.html's JS `locations` array into the new
CampusLocation table (see models.py's "University -> Campus -> CampusLocation"
architecture, added for the 10-university expansion). Name/lat/lng/id are copied
verbatim from the template -- this is real, already-live data being relocated to the
database, not new/invented data. `id` is kept only to build image_path (the landmark
photos in templates/images/ are named `<id>.jpeg`, served by routes/core_routes.py's
/images/<filename>) -- it is not stored as its own column. No location rows are created
for any other university; their Campus row (created in migration f2b5d8a03c69) starts
empty until real, sourced location data exists for that school (see
routes/campus_map_routes.py's admin CRUD).

Idempotent -- matches existing rows by (campus_id, name), safe to re-run.

Usage:
    python seed_campus_map.py
"""
from app import app, db
from models import University, Campus, CampusLocation

# (id, name, lat, lng) -- verbatim from templates/campus-map.html's `locations` array.
LASU_LOCATIONS = [
    ("makanjuola", "Aderemi Makanjuola Lecture Theatre", 6.466381, 3.201246),
    ("Agriculture_Society_Building", "Agriculture Society Building", 6.469889, 3.200425),
    ("Abisogun_Leigh_Science_Building", "Abisogun Leigh Science Building", 6.467138, 3.199167),
    ("arcade", "Arcade (Student Commercial Hub)", 6.465718, 3.203115),
    ("bank_arena", "Bank Arena", 6.464388, 3.204019),
    ("bolasciencecomplex", "Bola Ahmed Tinubu Science Complex", 6.466131, 3.200286),
    ("cbt_center", "CBT Center (Exam Hall)", 6.475192, 3.201302),
    ("siwes", "Central industrial liason unit (A.K.A) SIWES", 6.464279, 3.200211),
    ("cessed", "Centre for environmental studies and substanable Development (CESSED)", 6.465832, 3.201125),
    ("Centre-of-General-Nigerian-Studies", "Centre of General Nigerian Studies (C.G.N.S)", 6.464905, 3.200186),
    ("Chapel_Of_Light", "Chapel Of Light", 6.464979, 3.198642),
    ("cheif_s.l._edu_lecture_hall", "Cheif S.L. Edu Lecture Hall", 6.468023, 3.200031),
    ("Department_Of_Fisheries", "Department Of Fisheries Lagos State University", 6.470422, 3.200270),
    ("dsdp", "Directorate of Sandwich Degree Program", 6.470616, 3.201238),
    ("economics_hall", "Economics Hall", 6.475243, 3.199060),
    ("arts", "Faculty of Arts", 6.465115, 3.201104),
    ("education", "Faculty of Education", 6.472996, 3.199889),
    ("it", "Faculty of Computing and information Technology", 6.473991, 3.199653),
    ("law", "Faculty of Law", 6.467394, 3.202010),
    ("management_sciences", "Faculty of Management Sciences", 6.475661, 3.199942),
    ("odlri", "Open and Distance Learning and Research Institution", 6.474928, 3.200071),
    ("sciences", "Faculty of Sciences", 6.467837, 3.200798),
    ("social_sciences", "Faculty of Social Sciences", 6.475243, 3.199060),
    ("gbajabiamila", "Femi Gbajabiamila Conference Centre", 6.474624, 3.199331),
    ("health", "Health Center", 6.465443, 3.202018),
    ("Hussam_okoya_Sports_Complex", "Hussam okoya Sports Complex", 6.468703, 3.203875),
    ("ict", "ICT Building", 6.468753, 3.201230),
    ("innovationhub", "Innovation Hub", 6.465718, 3.200538),
    ("Library_Complex", "Lasu Centre Library", 6.471904, 3.201474),
    ("lasu-radio", "Lasu Radio", 6.472373, 3.199653),
    ("mosque", "LASU Central Mosque", 6.465425, 3.200015),
    ("lasu_football_pitch", "Lasu Football Pitch", 6.467892, 3.203102),
    ("law_clinic", "Law Clinic", 6.466861, 3.202268),
    ("love_garden", "Love Garden", 6.469094, 3.200508),
    ("main_auditorium", "Main Auditorium", 6.473108, 3.201887),
    ("library", "Main Library", 6.464857, 3.200701),
    ("mass_comm_hall", "Mass Communication Lecture Hall", 6.472277, 3.200154),
    ("mba_hall", "MBA Hall", 6.468553, 3.200275),
    ("physicslab", "Physics Lab", 6.465115, 3.201104),
    ("post_graduate_school", "Post Graduate School", 6.468391, 3.201227),
    ("primaryhealth", "Primary Health Center", 6.466038, 3.202061),
    ("SchoolofLibrary,ArchivalandinformationScience", "School of Library, Archival and information Science", 6.464433, 3.200205),
    ("school_of_transport", "School of Transport and Logistics", 6.474193, 3.198038),
    ("sciencecomplex", "Science Complex", 6.466573, 3.200165),
    ("science_library", "Science Library", 6.464526, 3.199186),
    ("science_market", "Science Market", 6.468047, 3.199285),
    ("Sciences_Laboratory", "Sciences Laboratory", 6.467114, 3.199851),
    ("Senate_Building", "Senate Building", 6.471272, 3.199924),
    ("bensonhall", "Shobowale Benson Hall", 6.467796, 3.200227),
    ("sports", "Sports Center", 6.469750, 3.202550),
    ("tetfund", "Tetfund 2019/2020 annual intervention", 6.465070, 3.202305),
    ("wppd", "Works and Physical Planning Department", 6.464092, 3.200205),
]


def _category_for(name):
    """Mirrors templates/campus-map.html's own getCategoryFromLocation() exactly, so a
    migrated row's marker color/grouping on the map doesn't change."""
    n = name.lower()
    if 'arcade' in n or 'commercial' in n:
        return 'commercial'
    if 'mosque' in n:
        return 'religious'
    if 'bank' in n:
        return 'bank'
    if 'sport' in n or 'court' in n:
        return 'sports'
    if 'ict' in n or 'cbt' in n or 'computer' in n:
        return 'ict'
    if 'medical' in n or 'health' in n:
        return 'healthcare'
    if 'faculty' in n or 'school' in n:
        return 'faculty'
    if 'library' in n or 'lab' in n:
        return 'department'
    if 'lecture' in n or 'hall' in n or 'auditorium' in n:
        return 'lecture'
    return 'general'


def seed_campus_map():
    with app.app_context():
        lasu = University.query.filter_by(name='Lagos State University').first()
        if not lasu:
            print("[WARN] Lagos State University not found -- run seed_academia.py first")
            return

        campus = Campus.query.filter_by(university_id=lasu.id, is_main=True).first()
        if not campus:
            print("[WARN] LASU has no main Campus row -- run the campus/campus_location migration first")
            return

        added = skipped = 0
        for loc_id, name, lat, lng in LASU_LOCATIONS:
            exists = CampusLocation.query.filter_by(campus_id=campus.id, name=name).first()
            if exists:
                skipped += 1
                continue
            db.session.add(CampusLocation(
                campus_id=campus.id, name=name, category=_category_for(name),
                latitude=lat, longitude=lng, image_path=f'images/{loc_id}.jpeg',
            ))
            added += 1

        db.session.commit()
        print(f"LASU campus locations -- added: {added}, skipped (already exist): {skipped}")


if __name__ == '__main__':
    seed_campus_map()
