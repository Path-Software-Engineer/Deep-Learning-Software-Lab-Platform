import type { TrainingPoint } from "@/types/neural-network";

import styles from "./NeuralNetworkExplainer.module.css";

interface LossChartProps {
  points: TrainingPoint[];
}

export function LossChart({ points }: LossChartProps) {
  const values = points.map((point) => point.loss);
  const maximum = Math.max(...values);
  const minimum = Math.min(...values);
  const span = maximum - minimum || 1;
  const plotted = points
    .map((point, index) => {
      const x = 24 + (552 * index) / Math.max(points.length - 1, 1);
      const y = 24 + (202 * (maximum - point.loss)) / span;
      return `${x.toFixed(2)},${y.toFixed(2)}`;
    })
    .join(" ");

  return (
    <figure className={styles.chart}>
      <svg
        viewBox="0 0 600 260"
        role="img"
        aria-label={`Loss decreased from ${maximum.toFixed(4)} to ${minimum.toFixed(6)}`}
      >
        <defs>
          <linearGradient id="lossFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#9d82ff" stopOpacity=".3" />
            <stop offset="1" stopColor="#9d82ff" stopOpacity="0" />
          </linearGradient>
        </defs>
        <line x1="24" y1="226" x2="576" y2="226" className={styles.chartAxis} />
        <line x1="24" y1="24" x2="24" y2="226" className={styles.chartAxis} />
        <polygon points={`24,226 ${plotted} 576,226`} fill="url(#lossFill)" />
        <polyline points={plotted} className={styles.chartLine} />
        <circle cx="576" cy="226" r="5" className={styles.chartEnd} />
      </svg>
      <figcaption>
        <span>epoch 0</span>
        <strong>Registered BCELoss</strong>
        <span>epoch {points.at(-1)?.epoch}</span>
      </figcaption>
    </figure>
  );
}
