/**
 * Public-page metadata.
 *
 * The marketing pages are server-rendered by nobody, so the browser owns the
 * title, description, canonical URL and social card. One map keeps those facts
 * beside the routes instead of scattering document.head edits through screens.
 */
import * as React from 'react';
import { useLocation } from 'react-router-dom';

const SITE = 'https://nelavista.com';
const SOCIAL_IMAGE = `${SITE}/og/og-main.jpg`;

interface PageMeta {
  title: string;
  description: string;
  noindex?: boolean;
}

const PAGES: Record<string, PageMeta> = {
  '/': {
    title: 'Nelavista - Learn it, prove it, get paid for it',
    description:
      'A working record for Nigerian university students: courses, CBT practice, verified skills and paid work in one place.',
  },
  '/features': {
    title: 'Features',
    description:
      'See how Nelavista connects learning, CBT practice, verification, paid work and a transcript that proves what you can do.',
  },
  '/how-it-works': {
    title: 'How it works',
    description:
      'From your first course to a verified skill and a paid brief: the path through Nelavista, step by step.',
  },
  '/pricing': {
    title: 'Pricing',
    description:
      'Students learn for free at launch. Employers pay for scoped, managed work. University partnerships are quoted after a pilot scoping call.',
  },
  '/about': {
    title: 'About',
    description:
      'Why Nelavista exists, who it is for, and the standards behind a working record for African university students.',
  },
  '/contact': {
    title: 'Contact',
    description:
      'Reach the Nelavista team about your account, a partnership or a question that is not in the FAQ.',
  },
  '/faq': {
    title: 'FAQ',
    description:
      'Straight answers about eligibility, verification, paid work, privacy and what Nelavista does not do.',
  },
  '/legal/privacy': {
    title: 'Privacy',
    description: 'How Nelavista collects, uses and protects personal data.',
  },
  '/legal/terms': {
    title: 'Terms',
    description: 'The terms for using Nelavista, including eligibility, accounts, acceptable use and payments.',
  },
  '/legal/contributor-terms': {
    title: 'Contributor terms',
    description: 'The terms for students who contribute work through Nelavista.',
  },
  '/offline': {
    title: 'Offline',
    description: 'Nelavista is offline. Reconnect to continue where you stopped.',
    noindex: true,
  },
};

const AUTH: Record<string, PageMeta> = {
  '/login': {
    title: 'Sign in',
    description: 'Sign in to your Nelavista working record.',
    noindex: true,
  },
  '/signup': {
    title: 'Create account',
    description: 'Create a Nelavista account and start building a working record.',
    noindex: true,
  },
  '/auth/verify': {
    title: 'Verify your email',
    description: 'Confirm the email address on your Nelavista account.',
    noindex: true,
  },
  '/auth/reset': {
    title: 'Reset password',
    description: 'Request a password reset for your Nelavista account.',
    noindex: true,
  },
};

function upsertMeta(attribute: 'name' | 'property', key: string, content: string): void {
  let tag = document.head.querySelector<HTMLMetaElement>(`meta[${attribute}="${key}"]`);
  if (!tag) {
    tag = document.createElement('meta');
    tag.setAttribute(attribute, key);
    document.head.appendChild(tag);
  }
  tag.setAttribute('content', content);
}

function upsertLink(rel: string, href: string): void {
  let tag = document.head.querySelector<HTMLLinkElement>(`link[rel="${rel}"]`);
  if (!tag) {
    tag = document.createElement('link');
    tag.setAttribute('rel', rel);
    document.head.appendChild(tag);
  }
  tag.setAttribute('href', href);
}

function removeLink(rel: string): void {
  document.head.querySelector<HTMLLinkElement>(`link[rel="${rel}"]`)?.remove();
}

/** Apply metadata for the current public or auth route. */
export function usePageMeta(): void {
  const { pathname } = useLocation();

  React.useEffect(() => {
    const isShare = pathname.startsWith('/share/');
    const page = isShare
      ? {
          title: 'Shared profile',
          description: 'A verified Nelavista working record shared by a student.',
          noindex: true,
        }
      : (PAGES[pathname] ??
        AUTH[pathname] ?? {
          title: 'Page not found',
          description: 'That page does not exist on Nelavista.',
          noindex: true,
        });
    const fullTitle = page.title.includes('Nelavista') ? page.title : `${page.title} | Nelavista`;
    const canonical = `${SITE}${pathname === '/' ? '/' : pathname}`;

    document.title = fullTitle;
    upsertMeta('name', 'description', page.description);
    upsertMeta('name', 'robots', page.noindex ? 'noindex, nofollow' : 'index, follow');
    if (isShare) removeLink('canonical');
    else upsertLink('canonical', canonical);

    upsertMeta('property', 'og:type', 'website');
    upsertMeta('property', 'og:site_name', 'Nelavista');
    upsertMeta('property', 'og:title', fullTitle);
    upsertMeta('property', 'og:description', page.description);
    upsertMeta('property', 'og:url', isShare ? SITE : canonical);
    upsertMeta('property', 'og:image', SOCIAL_IMAGE);
    upsertMeta('property', 'og:image:width', '1200');
    upsertMeta('property', 'og:image:height', '630');
    upsertMeta('property', 'og:image:alt', 'Nelavista working record illustration');

    upsertMeta('name', 'twitter:card', 'summary_large_image');
    upsertMeta('name', 'twitter:title', fullTitle);
    upsertMeta('name', 'twitter:description', page.description);
    upsertMeta('name', 'twitter:image', SOCIAL_IMAGE);
    upsertMeta('name', 'twitter:image:alt', 'Nelavista working record illustration');
  }, [pathname]);
}
