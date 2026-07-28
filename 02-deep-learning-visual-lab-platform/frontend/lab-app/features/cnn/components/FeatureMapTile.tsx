import type { CnnFeatureMap } from "@/types/cnn";

import styles from "./CnnFeatureMapViewer.module.css";

function displayColor(value: number) {
  const bounded = Math.max(0, Math.min(1, value));
  const red = Math.round(10 + bounded * 115);
  const green = Math.round(16 + bounded * 185);
  const blue = Math.round(31 + bounded * 224);
  return `rgb(${red} ${green} ${blue})`;
}

export function FeatureMapTile({ featureMap }: { featureMap: CnnFeatureMap }) {
  const [height, width] = featureMap.map_shape;
  return (
    <article className={styles.mapCard}>
      <div className={styles.mapHeading}>
        <div>
          <span>CHANNEL</span>
          <strong>{String(featureMap.channel).padStart(2, "0")}</strong>
        </div>
        <code>{height} × {width}</code>
      </div>
      <svg
        className={styles.mapVisual}
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label={`${featureMap.layer_label}, channel ${featureMap.channel}, normalized feature map`}
        preserveAspectRatio="none"
      >
        {featureMap.values.flatMap((row, rowIndex) =>
          row.map((value, columnIndex) => (
            <rect
              key={`${rowIndex}-${columnIndex}`}
              x={columnIndex}
              y={rowIndex}
              width="1.02"
              height="1.02"
              fill={displayColor(value)}
            />
          ))
        )}
      </svg>
      <dl className={styles.mapStats}>
        <div><dt>min</dt><dd>{featureMap.raw_min.toFixed(3)}</dd></div>
        <div><dt>mean</dt><dd>{featureMap.raw_mean.toFixed(3)}</dd></div>
        <div><dt>max</dt><dd>{featureMap.raw_max.toFixed(3)}</dd></div>
      </dl>
    </article>
  );
}
