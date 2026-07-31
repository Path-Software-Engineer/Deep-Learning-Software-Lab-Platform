"use client";

import type { KeyboardEvent } from "react";

import type {
  AutoencoderSample,
  LatentBounds
} from "@/types/autoencoder";

import styles from "./AutoencoderLatentSpaceDemo.module.css";

const COLORS = [
  "#ff8c7a",
  "#f4bd60",
  "#d7db6b",
  "#66ddb1",
  "#59d5f7",
  "#6ea9ff",
  "#9d82ff",
  "#c982e8",
  "#f17fb4",
  "#d2d8e5"
];

function scale(
  value: number,
  domain: [number, number],
  range: [number, number]
) {
  const span = domain[1] - domain[0] || 1;
  return range[0] + ((value - domain[0]) / span) * (range[1] - range[0]);
}

interface LatentScatterPlotProps {
  points: AutoencoderSample[];
  bounds: LatentBounds;
  selectedId: string;
  onSelect: (pointId: string) => void;
}

export function LatentScatterPlot({
  points,
  bounds,
  selectedId,
  onSelect
}: LatentScatterPlotProps) {
  const activate = (
    event: KeyboardEvent<SVGCircleElement>,
    pointId: string
  ) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onSelect(pointId);
    }
  };

  return (
    <div className={styles.plotFrame}>
      <svg
        className={styles.plot}
        viewBox="0 0 720 430"
        role="group"
        aria-label="Registered two-dimensional latent reference points"
      >
        <title>Registered autoencoder latent points</title>
        <desc>
          One hundred Fashion-MNIST reference images positioned by the two
          coordinates returned by the registered PyTorch encoder.
        </desc>
        <g className={styles.grid} aria-hidden="true">
          {[0, 1, 2, 3, 4].map((step) => {
            const x = 54 + step * 156;
            const y = 28 + step * 88;
            return (
              <g key={step}>
                <line x1={x} y1="28" x2={x} y2="380" />
                <line x1="54" y1={y} x2="678" y2={y} />
              </g>
            );
          })}
        </g>
        <line className={styles.axis} x1="54" y1="380" x2="678" y2="380" />
        <line className={styles.axis} x1="54" y1="28" x2="54" y2="380" />
        {points.map((point) => {
          const selected = point.id === selectedId;
          return (
            <circle
              key={point.id}
              className={selected ? styles.selectedPoint : styles.point}
              cx={scale(point.coordinate[0], bounds.x, [54, 678])}
              cy={scale(point.coordinate[1], bounds.y, [380, 28])}
              r={selected ? 8 : 5}
              fill={COLORS[point.label_index]}
              role="button"
              tabIndex={0}
              aria-label={`${point.label}, latent point ${point.id}, coordinates ${point.coordinate[0].toFixed(2)}, ${point.coordinate[1].toFixed(2)}`}
              aria-pressed={selected}
              onClick={() => onSelect(point.id)}
              onKeyDown={(event) => activate(event, point.id)}
            />
          );
        })}
        <text className={styles.axisLabel} x="630" y="412">latent x</text>
        <text className={styles.axisLabel} x="10" y="34">latent y</text>
      </svg>
      <div className={styles.legend} aria-label="Fashion-MNIST class legend">
        {Array.from(new Set(points.map((point) => point.label_index)))
          .sort((a, b) => a - b)
          .map((labelIndex) => {
            const example = points.find(
              (point) => point.label_index === labelIndex
            );
            return (
              <span key={labelIndex}>
                <i style={{ backgroundColor: COLORS[labelIndex] }} />
                {example?.label}
              </span>
            );
          })}
      </div>
    </div>
  );
}
