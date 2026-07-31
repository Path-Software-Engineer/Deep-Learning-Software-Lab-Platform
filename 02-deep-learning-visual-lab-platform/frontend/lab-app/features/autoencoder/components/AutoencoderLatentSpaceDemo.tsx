"use client";

import Image from "next/image";
import { useCallback, useEffect, useMemo, useState } from "react";

import { PlatformShell } from "@/components/platform/PlatformShell";
import { autoencoderApi, LabApiError } from "@/lib/api-client";
import type {
  AutoencoderInterpolation,
  AutoencoderLatentPoints,
  AutoencoderReconstruction,
  AutoencoderSample,
  AutoencoderSummary
} from "@/types/autoencoder";

import styles from "./AutoencoderLatentSpaceDemo.module.css";
import { LatentScatterPlot } from "./LatentScatterPlot";

const DEFAULT_START = "latent-08-00";
const DEFAULT_END = "latent-09-00";
const DEFAULT_STEPS = 7;

function formatError(error: unknown) {
  return error instanceof LabApiError
    ? error.message
    : "An unexpected client error interrupted the representation request.";
}

function fetchWorkspace() {
  return Promise.all([
    autoencoderApi.summary(),
    autoencoderApi.samples(),
    autoencoderApi.latentPoints(),
    autoencoderApi.reconstruct(DEFAULT_START),
    autoencoderApi.interpolate(DEFAULT_START, DEFAULT_END, DEFAULT_STEPS)
  ]);
}

function Metric({
  label,
  value,
  detail
}: {
  label: string;
  value: string;
  detail: string;
}) {
  return (
    <article className={styles.metric}>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </article>
  );
}

function EvidenceImage({
  source,
  alt,
  size = 160
}: {
  source: string;
  alt: string;
  size?: number;
}) {
  return (
    <Image
      unoptimized
      src={source}
      width={size}
      height={size}
      alt={alt}
    />
  );
}

export function AutoencoderLatentSpaceDemo() {
  const [summary, setSummary] = useState<AutoencoderSummary | null>(null);
  const [samples, setSamples] = useState<AutoencoderSample[]>([]);
  const [latent, setLatent] = useState<AutoencoderLatentPoints | null>(null);
  const [reconstruction, setReconstruction] =
    useState<AutoencoderReconstruction | null>(null);
  const [interpolation, setInterpolation] =
    useState<AutoencoderInterpolation | null>(null);
  const [selectedId, setSelectedId] = useState(DEFAULT_START);
  const [startId, setStartId] = useState(DEFAULT_START);
  const [endId, setEndId] = useState(DEFAULT_END);
  const [steps, setSteps] = useState(DEFAULT_STEPS);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadWorkspace = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [
        summaryResource,
        samplesResource,
        pointsResource,
        reconstructionResource,
        interpolationResource
      ] = await fetchWorkspace();
      setSummary(summaryResource);
      setSamples(samplesResource.samples);
      setLatent(pointsResource);
      setReconstruction(reconstructionResource);
      setInterpolation(interpolationResource);
      setSelectedId(DEFAULT_START);
      setStartId(DEFAULT_START);
      setEndId(DEFAULT_END);
      setSteps(DEFAULT_STEPS);
    } catch (reason) {
      setError(formatError(reason));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let active = true;
    fetchWorkspace()
      .then(([
        summaryResource,
        samplesResource,
        pointsResource,
        reconstructionResource,
        interpolationResource
      ]) => {
        if (!active) return;
        setSummary(summaryResource);
        setSamples(samplesResource.samples);
        setLatent(pointsResource);
        setReconstruction(reconstructionResource);
        setInterpolation(interpolationResource);
      })
      .catch((reason: unknown) => {
        if (active) setError(formatError(reason));
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const selectPoint = async (pointId: string) => {
    setSelectedId(pointId);
    setRunning(true);
    setError(null);
    try {
      setReconstruction(await autoencoderApi.reconstruct(pointId));
    } catch (reason) {
      setError(formatError(reason));
    } finally {
      setRunning(false);
    }
  };

  const runInterpolation = async () => {
    setRunning(true);
    setError(null);
    try {
      setInterpolation(
        await autoencoderApi.interpolate(startId, endId, steps)
      );
    } catch (reason) {
      setError(formatError(reason));
    } finally {
      setRunning(false);
    }
  };

  const selectablePoints = useMemo(() => latent?.points ?? [], [latent]);
  const selectedPoint = useMemo(
    () => selectablePoints.find((point) => point.id === selectedId),
    [selectablePoints, selectedId]
  );
  const busy = loading || running;

  return (
    <PlatformShell
      activeModule="latent-space"
      sprint="Sprint 03"
      title="Autoencoder Latent Space Demo"
      status={
        error
          ? "Engine needs attention"
          : busy
            ? "Decoding evidence…"
            : "Checkpoint connected"
      }
      version={summary?.model.version ?? "fashion-autoencoder-2d-v1"}
      hasError={Boolean(error)}
    >
      <div className={styles.content}>
          {error && (
            <div className={styles.errorBanner} role="alert">
              <span aria-hidden="true">!</span>
              <div>
                <strong>The latent workspace could not continue</strong>
                <p>{error}</p>
              </div>
              <button type="button" onClick={() => void loadWorkspace()}>
                Retry
              </button>
            </div>
          )}

          <section className={styles.hero}>
            <div>
              <p className={styles.eyebrow}>REGISTERED REPRESENTATION EVIDENCE</p>
              <h1>Compress the image.<br /><em>Navigate the representation.</em></h1>
              <p>
                Compare a Fashion-MNIST image with its reconstruction, select a
                registered 2D coordinate and decode a controlled interpolation.
              </p>
              <div className={styles.heroTags}>
                <span>2D bottleneck</span>
                <span>100 reference points</span>
                <span>decoder-backed interpolation</span>
              </div>
            </div>
            <div className={styles.latentVisual} aria-hidden="true">
              <span /><span /><span /><span /><span />
              <strong>z</strong>
              <code>[z₁, z₂]</code>
            </div>
          </section>

          {summary && (
            <section className={styles.metrics} aria-label="Registered autoencoder evidence">
              <Metric
                label="Held-out MSE"
                value={summary.evaluation.mean_squared_error.toFixed(4)}
                detail={`${summary.evaluation.samples} images`}
              />
              <Metric
                label="Held-out MAE"
                value={summary.evaluation.mean_absolute_error.toFixed(4)}
                detail="pixel scale 0–1"
              />
              <Metric
                label="Latent width"
                value="2D"
                detail="direct visualization"
              />
              <Metric
                label="Parameters"
                value={summary.model.parameter_count.toLocaleString()}
                detail="registered checkpoint"
              />
            </section>
          )}

          {loading && (
            <section className={styles.loadingPanel} aria-live="polite">
              <span /><span /><span />
              <p>Loading registered reconstruction evidence…</p>
            </section>
          )}

          {!loading && reconstruction && latent && (
            <>
              <section id="reconstruction" className={styles.reconstructionSection}>
                <div className={styles.sectionHeading}>
                  <div>
                    <p className={styles.eyebrow}>ENCODE → DECODE</p>
                    <h2>Compare source and reconstruction.</h2>
                  </div>
                  <p>
                    Choose one representative sample or any point in the plot.
                    Error values are returned by FastAPI.
                  </p>
                </div>

                <div className={styles.reconstructionGrid}>
                  <article className={styles.samplePanel}>
                    <div className={styles.panelHeading}>
                      <div><small>REGISTERED SAMPLES</small><strong>One per class</strong></div>
                      <code>{samples.length}/10</code>
                    </div>
                    <div className={styles.sampleGrid}>
                      {samples.map((sample) => (
                        <button
                          key={sample.id}
                          type="button"
                          className={sample.id === selectedId ? styles.selectedSample : ""}
                          aria-pressed={sample.id === selectedId}
                          disabled={busy}
                          onClick={() => void selectPoint(sample.id)}
                        >
                          <EvidenceImage
                            source={sample.image_data_uri}
                            alt={`${sample.label} registered sample`}
                            size={58}
                          />
                          <span>{sample.label}</span>
                        </button>
                      ))}
                    </div>
                  </article>

                  <article className={styles.comparisonPanel}>
                    <div className={styles.comparisonImages}>
                      <div>
                        <span>ORIGINAL</span>
                        <EvidenceImage
                          source={reconstruction.original.image_data_uri}
                          alt={`Original ${reconstruction.sample.label}`}
                        />
                      </div>
                      <div className={styles.encodeArrow} aria-hidden="true">
                        <span>encode</span><i>→</i><code>
                          {reconstruction.latent_coordinate.map((value) => value.toFixed(2)).join(", ")}
                        </code><i>→</i><span>decode</span>
                      </div>
                      <div>
                        <span>RECONSTRUCTION</span>
                        <EvidenceImage
                          source={reconstruction.reconstruction.image_data_uri}
                          alt={`Reconstructed ${reconstruction.sample.label}`}
                        />
                      </div>
                    </div>
                    <dl className={styles.errorMetrics}>
                      <div><dt>Selected point</dt><dd>{reconstruction.sample.id}</dd></div>
                      <div><dt>Reference label</dt><dd>{reconstruction.sample.label}</dd></div>
                      <div><dt>Mean squared error</dt><dd>{reconstruction.reconstruction.mean_squared_error.toFixed(6)}</dd></div>
                      <div><dt>Mean absolute error</dt><dd>{reconstruction.reconstruction.mean_absolute_error.toFixed(6)}</dd></div>
                    </dl>
                  </article>
                </div>
              </section>

              <section id="latent-space" className={styles.latentSection}>
                <div className={styles.sectionHeading}>
                  <div>
                    <p className={styles.eyebrow}>TWO-DIMENSIONAL BOTTLENECK</p>
                    <h2>Select a registered coordinate.</h2>
                  </div>
                  <p>{latent.interpretation}</p>
                </div>
                <div className={styles.latentGrid}>
                  <article className={styles.plotPanel}>
                    <LatentScatterPlot
                      points={latent.points}
                      bounds={latent.bounds}
                      selectedId={selectedId}
                      onSelect={(pointId) => void selectPoint(pointId)}
                    />
                  </article>
                  <aside className={styles.pointInspector}>
                    <p className={styles.eyebrow}>SELECTED REPRESENTATION</p>
                    {selectedPoint && (
                      <>
                        <EvidenceImage
                          source={selectedPoint.image_data_uri}
                          alt={`${selectedPoint.label} selected point`}
                          size={112}
                        />
                        <h3>{selectedPoint.label}</h3>
                        <code>{selectedPoint.id}</code>
                        <dl>
                          <div><dt>z₁</dt><dd>{selectedPoint.coordinate[0].toFixed(4)}</dd></div>
                          <div><dt>z₂</dt><dd>{selectedPoint.coordinate[1].toFixed(4)}</dd></div>
                          <div><dt>Point MSE</dt><dd>{selectedPoint.reconstruction_error.toFixed(5)}</dd></div>
                        </dl>
                      </>
                    )}
                    <h4>Nearest registered points</h4>
                    <div className={styles.neighborList}>
                      {reconstruction.neighbors.map((neighbor) => (
                        <button
                          key={neighbor.id}
                          type="button"
                          onClick={() => void selectPoint(neighbor.id)}
                        >
                          <EvidenceImage
                            source={neighbor.image_data_uri}
                            alt={`${neighbor.label} neighbor`}
                            size={40}
                          />
                          <span><strong>{neighbor.label}</strong><small>d {neighbor.distance.toFixed(3)}</small></span>
                        </button>
                      ))}
                    </div>
                  </aside>
                </div>
              </section>
            </>
          )}

          {!loading && interpolation && latent && (
            <section id="interpolation" className={styles.interpolationSection}>
              <div className={styles.sectionHeading}>
                <div>
                  <p className={styles.eyebrow}>DECODER PATH</p>
                  <h2>Interpolate between two registered points.</h2>
                </div>
                <p>
                  React sends endpoint IDs and step count. PyTorch decodes every
                  coordinate returned in the sequence.
                </p>
              </div>
              <div className={styles.interpolationControls}>
                <label>
                  Start point
                  <select value={startId} onChange={(event) => setStartId(event.target.value)}>
                    {latent.points.map((point) => (
                      <option key={point.id} value={point.id}>
                        {point.label} · {point.id}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  End point
                  <select value={endId} onChange={(event) => setEndId(event.target.value)}>
                    {latent.points.map((point) => (
                      <option key={point.id} value={point.id}>
                        {point.label} · {point.id}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  Steps <strong>{steps}</strong>
                  <input
                    type="range"
                    min={3}
                    max={12}
                    value={steps}
                    onChange={(event) => setSteps(Number(event.target.value))}
                  />
                </label>
                <button
                  type="button"
                  disabled={busy || startId === endId}
                  onClick={() => void runInterpolation()}
                >
                  {running ? "Decoding path…" : "Decode interpolation"}
                  <span aria-hidden="true">→</span>
                </button>
              </div>
              <div className={styles.interpolationStrip}>
                {interpolation.steps.map((step) => (
                  <article key={step.index}>
                    <EvidenceImage
                      source={step.image_data_uri}
                      alt={`Decoded interpolation at ${(step.alpha * 100).toFixed(0)} percent`}
                      size={104}
                    />
                    <strong>{(step.alpha * 100).toFixed(0)}%</strong>
                    <code>{step.coordinate.map((value) => value.toFixed(2)).join(", ")}</code>
                  </article>
                ))}
              </div>
              <p className={styles.interpretation}>{interpolation.interpretation}</p>
            </section>
          )}

          {summary && (
            <section id="limits" className={styles.evidenceSection}>
              <div>
                <p className={styles.eyebrow}>EVIDENCE BOUNDARY</p>
                <h2>Representation is observable. Meaning remains bounded.</h2>
                <p>
                  The interface exposes registered computation and metrics without
                  upgrading proximity or visual smoothness into explanation.
                </p>
              </div>
              <ol>
                {summary.limitations.map((limitation, index) => (
                  <li key={limitation}>
                    <span>{String(index + 1).padStart(2, "0")}</span>
                    {limitation}
                  </li>
                ))}
              </ol>
            </section>
          )}

          <footer>
            <span>AXON / DEEP LEARNING VISUAL LAB</span>
            <span>SPRINT 03 · REGISTERED PYTORCH EVIDENCE</span>
          </footer>
      </div>
    </PlatformShell>
  );
}
