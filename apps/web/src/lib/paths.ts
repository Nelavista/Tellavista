/**
 * The four student spaces and the dashboard each one opens.
 *
 * The API is the source of truth for the stored value. This module keeps the
 * labels, descriptions and destinations in one place so onboarding, Home and
 * the shell cannot drift into four different ideas of what "Skills" means.
 */
import type { PreferredPath } from '@nelavista/contracts';

export interface PathOption {
  value: PreferredPath;
  label: string;
  summary: string;
  detail: string;
  destination: string;
}

export const PATH_OPTIONS: PathOption[] = [
  {
    value: 'academia',
    label: 'Academia',
    summary: 'Your courses, materials and CBT practice.',
    detail: 'Built around the university and courses you are enrolled in.',
    destination: '/academia',
  },
  {
    value: 'skills',
    label: 'Skills',
    summary: 'Short lessons, practice and a path you can finish.',
    detail: 'Learn a skill in order, then prove it through verification.',
    destination: '/skills',
  },
  {
    value: 'opportunities',
    label: 'Opportunities',
    summary: 'Work that fits what you have proved.',
    detail: 'See open roles, why you qualify and what is still missing.',
    destination: '/opportunities',
  },
  {
    value: 'campus',
    label: 'Campus',
    summary: 'Your university information and map points.',
    detail: 'A quiet utility for the campus you actually study on.',
    destination: '/campus',
  },
];

const BY_VALUE = new Map(PATH_OPTIONS.map((option) => [option.value, option]));

export function isPreferredPath(value: string | null | undefined): value is PreferredPath {
  return value === 'academia' || value === 'skills' || value === 'opportunities' || value === 'campus';
}

export function pathOption(value: string | null | undefined): PathOption | null {
  return isPreferredPath(value) ? (BY_VALUE.get(value) ?? null) : null;
}

export function pathDestination(value: string | null | undefined, fallback = '/home'): string {
  return pathOption(value)?.destination ?? fallback;
}

export function pathNeedsStudies(value: string | null | undefined): boolean {
  return value === 'academia' || value === 'campus';
}
