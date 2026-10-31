import { FacebookLogoIcon } from '@phosphor-icons/react/dist/csr/FacebookLogo';
import { TelegramLogoIcon } from '@phosphor-icons/react/dist/csr/TelegramLogo';
import { WhatsappLogoIcon } from '@phosphor-icons/react/dist/csr/WhatsappLogo';
import * as React from 'react';

const SHARE_TEXT = 'Nelavista: learn it, prove it, get paid for it.';

function shareUrl(): string {
  if (typeof window === 'undefined') return 'https://nelavista.com/';
  return window.location.href;
}

export function SocialLinks({ label = 'Share Nelavista' }: { label?: string }): JSX.Element {
  const url = React.useMemo(shareUrl, []);
  const encoded = encodeURIComponent(url);
  const text = encodeURIComponent(SHARE_TEXT);
  const links = [
    {
      label: 'Share on Facebook',
      href: `https://www.facebook.com/sharer/sharer.php?u=${encoded}`,
      Icon: FacebookLogoIcon,
      network: 'facebook',
    },
    {
      label: 'Share on WhatsApp',
      href: `https://wa.me/?text=${text}%20${encoded}`,
      Icon: WhatsappLogoIcon,
      network: 'whatsapp',
    },
    {
      label: 'Share on Telegram',
      href: `https://t.me/share/url?url=${encoded}&text=${text}`,
      Icon: TelegramLogoIcon,
      network: 'telegram',
    },
  ];

  return (
    <div className="nv-social-links" aria-label={label}>
      {links.map(({ label: itemLabel, href, Icon, network }) => (
        <a
          aria-label={itemLabel}
          className="nv-social-link"
          data-network={network}
          href={href}
          key={itemLabel}
          rel="noreferrer noopener"
          target="_blank"
          title={itemLabel}
        >
          <Icon aria-hidden="true" size={18} weight="fill" />
        </a>
      ))}
    </div>
  );
}
