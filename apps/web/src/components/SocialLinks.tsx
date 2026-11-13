import { FacebookLogoIcon } from '@phosphor-icons/react/dist/csr/FacebookLogo';
import { TelegramLogoIcon } from '@phosphor-icons/react/dist/csr/TelegramLogo';
import { WhatsappLogoIcon } from '@phosphor-icons/react/dist/csr/WhatsappLogo';
import * as React from 'react';
import { useLocation } from 'react-router-dom';

const SHARE_TEXT = 'Nelavista: learn it, prove it, get paid for it.';
const GLIDE_MS = 550;
const DWELL_MS = 1400;
const LOGO_DWELL_MS = 1600;
const FADE_OUT_MS = 400;
const PAUSE_MS = 300;

const BRAND = {
  fb: '#1877F2',
  wa: '#25D366',
  tg: '#229ED9',
} as const;

type Slot = 'fb' | 'wa' | 'tg' | 'logo';
type Step = 0 | 1 | 2 | 3 | 4;

const SLOT: Record<Slot, { x: 0 | 1 | 2; y: 0 | 1 | 2 }> = {
  fb: { x: 0, y: 1 },
  tg: { x: 2, y: 1 },
  wa: { x: 1, y: 2 },
  logo: { x: 1, y: 0 },
};

const STEPS: Array<{ slot: Slot; color: string; hold: number }> = [
  { slot: 'fb', color: BRAND.fb, hold: DWELL_MS },
  { slot: 'wa', color: BRAND.wa, hold: DWELL_MS },
  { slot: 'tg', color: BRAND.tg, hold: DWELL_MS },
  { slot: 'logo', color: 'var(--nv-accent)', hold: LOGO_DWELL_MS },
];

const NETWORKS = [
  {
    label: 'Share on Facebook',
    href: (encoded: string) => `https://www.facebook.com/sharer/sharer.php?u=${encoded}`,
    Icon: FacebookLogoIcon,
    slot: 'fb' as const,
  },
  {
    label: 'Share on WhatsApp',
    href: (encoded: string, text: string) => `https://wa.me/?text=${text}%20${encoded}`,
    Icon: WhatsappLogoIcon,
    slot: 'wa' as const,
  },
  {
    label: 'Share on Telegram',
    href: (encoded: string, text: string) => `https://t.me/share/url?url=${encoded}&text=${text}`,
    Icon: TelegramLogoIcon,
    slot: 'tg' as const,
  },
];

function shareUrl(pathname: string): string {
  if (typeof window === 'undefined') return 'https://nelavista.com/';
  return `${window.location.origin}${pathname}`;
}

function position(slot: Slot): string {
  const coordinates = SLOT[slot];
  return `translate3d(calc(var(--dx) * ${coordinates.x}), calc(var(--dy) * ${coordinates.y}), 0)`;
}

function nextStep(step: Step): Step {
  return step === 4 ? 0 : ((step + 1) as Step);
}

export function SocialLinks({ label = 'Share Nelavista' }: { label?: string }): JSX.Element {
  const { pathname } = useLocation();
  const url = shareUrl(pathname);
  const encoded = encodeURIComponent(url);
  const text = encodeURIComponent(SHARE_TEXT);
  const rootRef = React.useRef<HTMLDivElement | null>(null);
  const timeoutRef = React.useRef<number | null>(null);
  const resetFrameRef = React.useRef<number | null>(null);
  const revealFrameRef = React.useRef<number | null>(null);
  const [step, setStep] = React.useState<Step>(0);
  const [paused, setPaused] = React.useState(false);
  const [hidden, setHidden] = React.useState(false);
  const [inView, setInView] = React.useState(true);
  const [reducedMotion, setReducedMotion] = React.useState(false);
  const [hoverSlot, setHoverSlot] = React.useState<Slot | null>(null);
  const [resetting, setResetting] = React.useState(false);

  React.useEffect(() => {
    // Older embedded browsers and test environments can omit matchMedia; the
    // default is motion on, so a missing query is not an error.
    if (typeof window.matchMedia !== 'function') return undefined;
    const media = window.matchMedia('(prefers-reduced-motion: reduce)');
    const update = () => setReducedMotion(media.matches);
    update();
    media.addEventListener('change', update);
    return () => media.removeEventListener('change', update);
  }, []);

  React.useEffect(() => {
    const onVisibilityChange = () => {
      setHidden(document.hidden);
      setPaused(false);
      setHoverSlot(null);
    };
    const onWindowBlur = () => {
      setPaused(false);
      setHoverSlot(null);
    };
    document.addEventListener('visibilitychange', onVisibilityChange);
    window.addEventListener('blur', onWindowBlur);
    return () => {
      document.removeEventListener('visibilitychange', onVisibilityChange);
      window.removeEventListener('blur', onWindowBlur);
    };
  }, []);

  React.useEffect(() => {
    return () => {
      if (timeoutRef.current !== null) window.clearTimeout(timeoutRef.current);
      if (resetFrameRef.current !== null) window.cancelAnimationFrame(resetFrameRef.current);
      if (revealFrameRef.current !== null) window.cancelAnimationFrame(revealFrameRef.current);
    };
  }, []);

  React.useEffect(() => {
    const root = rootRef.current;
    if (!root || typeof IntersectionObserver === 'undefined') return undefined;
    const observer = new IntersectionObserver(([entry]) => setInView(entry?.isIntersecting ?? false));
    observer.observe(root);
    return () => observer.disconnect();
  }, []);

  React.useEffect(() => {
    if (reducedMotion || paused || hidden || !inView) return undefined;

    if (step === 4) {
      timeoutRef.current = window.setTimeout(() => {
        setResetting(true);
        setStep(0);
        resetFrameRef.current = window.requestAnimationFrame(() => {
          revealFrameRef.current = window.requestAnimationFrame(() => {
            setResetting(false);
          });
        });
      }, FADE_OUT_MS + PAUSE_MS);
      return () => {
        if (timeoutRef.current !== null) window.clearTimeout(timeoutRef.current);
        if (resetFrameRef.current !== null) window.cancelAnimationFrame(resetFrameRef.current);
        if (revealFrameRef.current !== null) window.cancelAnimationFrame(revealFrameRef.current);
      };
    }

    timeoutRef.current = window.setTimeout(() => setStep(nextStep(step)), STEPS[step]?.hold ?? DWELL_MS);
    return () => {
      if (timeoutRef.current !== null) window.clearTimeout(timeoutRef.current);
    };
  }, [hidden, inView, paused, reducedMotion, step]);

  const animatedStep = (step === 4 ? STEPS[3] : STEPS[step])!;
  const activeSlot = hoverSlot ?? animatedStep.slot;
  const highlightVisible = reducedMotion
    ? hoverSlot !== null
    : hoverSlot !== null || (!resetting && step !== 4);
  const logoVisible = !reducedMotion && step === 3;
  const highlightColor = hoverSlot
    ? hoverSlot === 'fb'
      ? BRAND.fb
      : hoverSlot === 'wa'
        ? BRAND.wa
        : BRAND.tg
    : animatedStep.color;
  const rootStyle: React.CSSProperties & {
    '--nv-social-glide': string;
    '--nv-social-fade': string;
  } = {
    '--nv-social-glide': `${GLIDE_MS}ms`,
    '--nv-social-fade': `${FADE_OUT_MS}ms`,
  };

  return (
    <div
      ref={rootRef}
      className="nv-social-links"
      role="group"
      aria-label={label}
      style={rootStyle}
      onBlur={(event) => {
        if (!event.currentTarget.contains(event.relatedTarget)) {
          setHoverSlot(null);
          setPaused(false);
        }
      }}
      onPointerLeave={(event) => {
        if (event.pointerType === 'mouse') {
          setHoverSlot(null);
          setPaused(false);
        }
      }}
    >
      <span
        aria-hidden="true"
        className={`nv-social-highlight${resetting ? ' nv-social-highlight--resetting' : ''}`}
        data-visible={highlightVisible}
        style={{ backgroundColor: highlightColor, transform: position(activeSlot) }}
      />
      {NETWORKS.map(({ label: itemLabel, href, Icon, slot }) => (
        <a
          aria-label={itemLabel}
          className="nv-social-link"
          data-active={highlightVisible && activeSlot === slot}
          data-network={slot}
          href={href(encoded, text)}
          key={slot}
          rel="noopener noreferrer"
          style={{ transform: position(slot) }}
          target="_blank"
          onFocus={() => {
            const target = document.activeElement;
            if (target instanceof HTMLElement && target.matches(':focus-visible')) {
              setHoverSlot(slot);
              setPaused(true);
            }
          }}
          onBlur={(event) => {
            if (!event.currentTarget.contains(event.relatedTarget)) setHoverSlot(null);
          }}
          onPointerEnter={(event) => {
            if (event.pointerType === 'mouse') {
              setHoverSlot(slot);
              setPaused(true);
            }
          }}
          onPointerLeave={(event) => {
            if (event.pointerType === 'mouse') setHoverSlot(null);
          }}
        >
          <Icon aria-hidden="true" size={18} weight="fill" />
        </a>
      ))}
      <span
        aria-hidden="true"
        className="nv-social-logo"
        data-visible={logoVisible}
        style={{ transform: position('logo') }}
      >
        <img alt="" decoding="async" src="/brand/nelavista-logo.png" />
      </span>
    </div>
  );
}
