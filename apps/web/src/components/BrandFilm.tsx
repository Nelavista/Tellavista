import { BrandMark } from '@nelavista/ui';
import { useReducedMotion } from 'motion/react';
import * as React from 'react';

export function BrandFilm(): JSX.Element {
  const reduce = useReducedMotion();
  const [failed, setFailed] = React.useState(false);

  return (
    <section className="nv-brand-film" aria-label="Nelavista brand animation">
      {reduce || failed ? (
        <div className="nv-brand-film__still">
          <BrandMark size={56} />
          <span>Nelavista</span>
        </div>
      ) : (
        <video
          aria-hidden="true"
          autoPlay
          className="nv-brand-film__video"
          height={1080}
          loop
          muted
          onError={() => setFailed(true)}
          playsInline
          preload="metadata"
          src="/media/animation3_color_exchange.mp4"
          tabIndex={-1}
          width={1920}
        />
      )}
    </section>
  );
}
