"""Academia taxonomy: University › Faculty › Department › Course › Material (PRD §3).

Minimal skeleton mirroring V1's taxonomy (audit §2.3) so seeds and health checks
exercise a real chain. Full academia modelling is V2 feature work (M1).
"""
from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class University(Base, TimestampMixin):
    __tablename__ = "universities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)


class Faculty(Base, TimestampMixin):
    __tablename__ = "faculties"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(ForeignKey("universities.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    __table_args__ = (UniqueConstraint("university_id", "name", name="uq_faculty_university_name"),)


class Department(Base, TimestampMixin):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    __table_args__ = (UniqueConstraint("faculty_id", "name", name="uq_department_faculty_name"),)


class Course(Base, TimestampMixin):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id", ondelete="CASCADE"))
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    level: Mapped[str] = mapped_column(String(10), nullable=False)
    __table_args__ = (UniqueConstraint("department_id", "code", "level", name="uq_course_dept_level_code"),)

    materials: Mapped[list[Material]] = relationship(back_populates="course")


class Material(Base, TimestampMixin):
    __tablename__ = "materials"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int | None] = mapped_column(ForeignKey("courses.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str | None] = mapped_column(String(1024))
    source: Mapped[str] = mapped_column(String(30), default="local", nullable=False)

    course: Mapped[Course | None] = relationship(back_populates="materials")
