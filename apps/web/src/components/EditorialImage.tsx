import * as React from 'react';

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(' ');
}

export function EditorialImage({
  name,
  alt,
  width = 1536,
  height = 1024,
  priority = false,
  caption,
  className,
}: {
  name: string;
  alt: string;
  width?: number;
  height?: number;
  priority?: boolean;
  caption?: React.ReactNode;
  className?: string;
}): JSX.Element {
  return (
    <figure className={cx('nv-figure', className)}>
      <img
        alt={alt}
        className="nv-editorial-image"
        decoding="async"
        height={height}
        loading={priority ? 'eager' : 'lazy'}
        src={`/images/${name}.webp`}
        style={{ aspectRatio: `${width} / ${height}` }}
        width={width}
      />
      {caption ? <figcaption className="nv-figure__caption">{caption}</figcaption> : null}
    </figure>
  );
}
