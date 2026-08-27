"""Convert skill_categories.icon, skills.icon and career_tracks.icon from single emoji
characters to Remix Icon class names (e.g. "ri-code-s-slash-line"), matching the icon font
already used everywhere else in Nelavista Skills (see templates/components/skills_sidebar.html).
Widens the column from String(10) to String(40) since class names run longer than one
emoji glyph, then backfills any emoji already saved via the admin "Icon" field to their
closest Remix equivalent. Anything not in the known map falls back to a sane default
per table so no row is left holding a value the templates can no longer render.

Revision ID: c2a8f4e91d67
Revises: 1901b06cab42
Create Date: 2026-08-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'c2a8f4e91d67'
down_revision = '1901b06cab42'
branch_labels = None
depends_on = None

# Emoji -> Remix Icon class, covering every value seed_skills.py has ever written plus the
# common picks an admin would reach for in the "Icon (single emoji)" field.
_EMOJI_TO_REMIX = {
    '\U0001F4BB': 'ri-code-s-slash-line',   # 💻 Tech
    '\U0001F3A8': 'ri-palette-line',        # 🎨 Design / UI/UX
    '\U0001F4BC': 'ri-briefcase-line',      # 💼 Business
    '\U0001F3AC': 'ri-movie-2-line',        # 🎬 Creative / Content Creation
    '\U0001F680': 'ri-rocket-line',         # 🚀 Career
    '\U0001F40D': 'ri-terminal-box-line',   # 🐍 Python
    '\U0001F310': 'ri-global-line',         # 🌐 Web Development
    '\U0001F4C8': 'ri-line-chart-line',     # 📈 Digital Marketing
    '\U0001F4C4': 'ri-file-text-line',      # 📄 CV & Interview Prep
    '\U0001F9ED': 'ri-route-line',          # 🧭 Career track
    '\U0001F4C1': 'ri-folder-line',         # 📁 Category (generic)
    '\U0001F9E9': 'ri-puzzle-line',         # 🧩 Skill (generic)
}

_CATEGORY_DEFAULT = 'ri-folder-line'
_SKILL_DEFAULT = 'ri-puzzle-line'
_TRACK_DEFAULT = 'ri-route-line'


def _backfill(table, default_icon):
    conn = op.get_bind()
    rows = conn.execute(sa.text(f'SELECT id, icon FROM {table} WHERE icon IS NOT NULL')).fetchall()
    for row_id, icon in rows:
        new_icon = _EMOJI_TO_REMIX.get(icon, default_icon if not icon.startswith('ri-') else icon)
        if new_icon != icon:
            conn.execute(sa.text(f'UPDATE {table} SET icon = :icon WHERE id = :id'),
                         {'icon': new_icon, 'id': row_id})


def upgrade():
    with op.batch_alter_table('skill_categories', schema=None) as batch_op:
        batch_op.alter_column('icon', existing_type=sa.String(10), type_=sa.String(40))
    with op.batch_alter_table('skills', schema=None) as batch_op:
        batch_op.alter_column('icon', existing_type=sa.String(10), type_=sa.String(40))
    with op.batch_alter_table('career_tracks', schema=None) as batch_op:
        batch_op.alter_column('icon', existing_type=sa.String(10), type_=sa.String(40))

    _backfill('skill_categories', _CATEGORY_DEFAULT)
    _backfill('skills', _SKILL_DEFAULT)
    _backfill('career_tracks', _TRACK_DEFAULT)


def downgrade():
    # Emoji -> Remix is lossy in reverse (many emoji can map to the same icon class), so
    # downgrade only restores the column width; it does not attempt to un-map icon values.
    with op.batch_alter_table('career_tracks', schema=None) as batch_op:
        batch_op.alter_column('icon', existing_type=sa.String(40), type_=sa.String(10))
    with op.batch_alter_table('skills', schema=None) as batch_op:
        batch_op.alter_column('icon', existing_type=sa.String(40), type_=sa.String(10))
    with op.batch_alter_table('skill_categories', schema=None) as batch_op:
        batch_op.alter_column('icon', existing_type=sa.String(40), type_=sa.String(10))
