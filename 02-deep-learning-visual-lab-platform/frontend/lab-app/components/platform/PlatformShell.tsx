import Link from "next/link";
import type { ReactNode } from "react";

import styles from "./PlatformShell.module.css";

export type PlatformModule = "neural-trace" | "feature-maps" | "latent-space";

const MODULES: Array<{
  id: PlatformModule;
  number: string;
  title: string;
  description: string;
  href: string;
}> = [
  {
    id: "neural-trace",
    number: "01",
    title: "Neural trace",
    description: "XOR explainer",
    href: "/"
  },
  {
    id: "feature-maps",
    number: "02",
    title: "Feature maps",
    description: "Fashion CNN",
    href: "/cnn"
  },
  {
    id: "latent-space",
    number: "03",
    title: "Latent space",
    description: "Autoencoder 2D",
    href: "/autoencoder"
  }
];

type PlatformShellProps = {
  activeModule: PlatformModule;
  sprint: string;
  title: string;
  status: string;
  version: string;
  hasError?: boolean;
  children: ReactNode;
};

export function PlatformShell({
  activeModule,
  sprint,
  title,
  status,
  version,
  hasError = false,
  children
}: PlatformShellProps) {
  return (
    <div className={styles.shell} data-module={activeModule}>
      <a className={styles.skipLink} href="#main-content">
        Skip to module content
      </a>

      <aside className={styles.sidebar}>
        <Link className={styles.brand} href="/" aria-label="Axon platform home">
          <span className={styles.brandMark} aria-hidden="true">
            <i />
            <i />
            <i />
          </span>
          <span>
            <strong>Axon</strong>
            <small>Deep learning visual lab</small>
          </span>
        </Link>

        <div className={styles.navigationHeading}>
          <span>Platform modules</span>
          <small>03 registered labs</small>
        </div>

        <nav className={styles.moduleNavigation} aria-label="Platform modules">
          {MODULES.map((module) => {
            const isActive = module.id === activeModule;

            return (
              <Link
                key={module.id}
                className={isActive ? styles.activeModule : undefined}
                href={module.href}
                aria-current={isActive ? "page" : undefined}
              >
                <span className={styles.moduleNumber}>{module.number}</span>
                <span className={styles.moduleCopy}>
                  <strong>{module.title}</strong>
                  <small>{module.description}</small>
                </span>
                <span className={styles.moduleState} aria-hidden="true" />
              </Link>
            );
          })}
        </nav>

        <div className={styles.sidebarFooter}>
          <div className={styles.engineCard}>
            <p>Official engine</p>
            <strong>PyTorch · checkpoint</strong>
            <span>
              <i aria-hidden="true" />
              Read-only inference
            </span>
          </div>

          <div className={styles.profile}>
            <span aria-hidden="true">JL</span>
            <div>
              <strong>Jean Loa</strong>
              <small>Software engineering path</small>
            </div>
          </div>
        </div>
      </aside>

      <main id="main-content" className={styles.main}>
        <header className={styles.topbar}>
          <div className={styles.moduleIdentity}>
            <small>Project 02 / {sprint}</small>
            <strong>{title}</strong>
          </div>
          <div className={styles.status} data-error={hasError || undefined}>
            <i aria-hidden="true" />
            <span>{status}</span>
            <code>{version}</code>
          </div>
        </header>

        <div className={styles.contentFrame}>{children}</div>
      </main>
    </div>
  );
}
