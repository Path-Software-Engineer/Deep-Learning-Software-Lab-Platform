"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";

import { cnnApi, LabApiError } from "@/lib/api-client";
import type {
  CnnFeatureMaps,
  CnnImageInput,
  CnnSample,
  CnnSummary
} from "@/types/cnn";

import styles from "./CnnFeatureMapViewer.module.css";
import { FeatureMapTile } from "./FeatureMapTile";

const DEFAULT_SAMPLE = "fashion-08";
const DEFAULT_CHANNELS = [0, 1, 2, 3, 4, 5];
const MAX_SELECTED_CHANNELS = 12;

function formatError(error: unknown) {
  return error instanceof LabApiError
    ? error.message
    : "An unexpected client error interrupted the representation request.";
}

function UploadIcon() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24">
      <path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5M5 14v4.5A1.5 1.5 0 0 0 6.5 20h11a1.5 1.5 0 0 0 1.5-1.5V14" />
    </svg>
  );
}

function ArrowIcon() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24">
      <path d="M5 12h13m-5-5 5 5-5 5" />
    </svg>
  );
}

export function CnnFeatureMapViewer() {
  const uploadRef = useRef<HTMLInputElement>(null);
  const [summary, setSummary] = useState<CnnSummary | null>(null);
  const [samples, setSamples] = useState<CnnSample[]>([]);
  const [result, setResult] = useState<CnnFeatureMaps | null>(null);
  const [sourceMode, setSourceMode] = useState<"sample" | "upload">("sample");
  const [sampleId, setSampleId] = useState(DEFAULT_SAMPLE);
  const [upload, setUpload] = useState<File | null>(null);
  const [layer, setLayer] = useState("block1_relu");
  const [channels, setChannels] = useState<number[]>(DEFAULT_CHANNELS);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const requestInput = useMemo<CnnImageInput>(
    () => sourceMode === "upload" ? { file: upload ?? undefined } : { sampleId },
    [sampleId, sourceMode, upload]
  );

  useEffect(() => {
    let active = true;
    Promise.all([
      cnnApi.summary(),
      cnnApi.samples(),
      cnnApi.featureMaps(
        { sampleId: DEFAULT_SAMPLE },
        "block1_relu",
        DEFAULT_CHANNELS
      )
    ])
      .then(([summaryResource, samplesResource, mapsResource]) => {
        if (!active) return;
        setSummary(summaryResource);
        setSamples(samplesResource.samples);
        setResult(mapsResource);
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

  const inspect = async () => {
    if (sourceMode === "upload" && !upload) {
      setError("Choose a PNG or JPEG image before running the inspection.");
      uploadRef.current?.focus();
      return;
    }
    setRunning(true);
    setError(null);
    try {
      setResult(await cnnApi.featureMaps(requestInput, layer, channels));
    } catch (reason) {
      setError(formatError(reason));
    } finally {
      setRunning(false);
    }
  };

  const selectLayer = (nextLayer: string) => {
    setLayer(nextLayer);
    setChannels(DEFAULT_CHANNELS);
  };

  const toggleChannel = (channel: number) => {
    setChannels((current) => {
      if (current.includes(channel)) {
        return current.length === 1
          ? current
          : current.filter((value) => value !== channel);
      }
      if (current.length >= MAX_SELECTED_CHANNELS) return current;
      return [...current, channel].sort((a, b) => a - b);
    });
  };

  const currentLayer = summary?.layers.find((item) => item.id === layer);
  const rankedProbabilities = result
    ? [...result.prediction.probabilities].sort(
        (first, second) => second.probability - first.probability
      )
    : [];
  const busy = loading || running;

  return (
    <div className={styles.shell}>
      <aside className={styles.sidebar}>
        <Link className={styles.brand} href="/" aria-label="Axon platform home">
          <span className={styles.brandMark} aria-hidden="true"><i /><i /><i /></span>
          <span><strong>Axon</strong><small>Neural learning lab</small></span>
        </Link>

        <div className={styles.moduleLabel}>LAB MODULES</div>
        <nav aria-label="Platform modules">
          <Link href="/">
            <span>01</span>
            <div><strong>Neural trace</strong><small>XOR explainer</small></div>
          </Link>
          <Link className={styles.activeNav} href="/cnn" aria-current="page">
            <span>02</span>
            <div><strong>Feature maps</strong><small>Fashion CNN</small></div>
          </Link>
        </nav>

        <div className={styles.sectionNav}>
          <a href="#source">01 / Input source</a>
          <a href="#representation">02 / Representation</a>
          <a href="#evidence">03 / Evidence boundary</a>
        </div>

        <div className={styles.engineCard}>
          <p>OFFICIAL ENGINE</p>
          <strong>PyTorch · checkpoint</strong>
          <span><i /> read-only inference</span>
        </div>
        <div className={styles.profile}>
          <span>JL</span>
          <div><strong>Jean Loa</strong><small>Software engineering path</small></div>
        </div>
      </aside>

      <main className={styles.main}>
        <header className={styles.topbar}>
          <div>
            <small>Project 02 / Sprint 02</small>
            <strong>CNN Feature Map Viewer</strong>
          </div>
          <div className={styles.status}>
            <i className={error ? styles.statusError : ""} />
            {error ? "Engine needs attention" : busy ? "Reading evidence…" : "Checkpoint connected"}
            <code>{summary?.model.version ?? "fashion-cnn-v1"}</code>
          </div>
        </header>

        <div className={styles.content}>
          {error && (
            <div className={styles.errorBanner} role="alert">
              <span aria-hidden="true">!</span>
              <div><strong>The inspection could not continue</strong><p>{error}</p></div>
              <button type="button" onClick={() => void inspect()}>Retry</button>
            </div>
          )}

          <section className={styles.hero}>
            <div>
              <p className={styles.eyebrow}>REGISTERED CNN EVIDENCE</p>
              <h1>See what each channel <em>responds to.</em></h1>
              <p>
                Classify one Fashion-MNIST image, select an observable
                convolution layer and inspect the exact activation maps returned by PyTorch.
              </p>
              <div className={styles.heroTags}>
                <span>Fashion-MNIST</span>
                <span>28 × 28 grayscale</span>
                <span>{summary ? `${(summary.evaluation.accuracy * 100).toFixed(1)}% holdout` : "held-out evidence"}</span>
              </div>
            </div>
            <div className={styles.tensorVisual} aria-hidden="true">
              <div className={styles.tensorBack} />
              <div className={styles.tensorMiddle} />
              <div className={styles.tensorFront}>
                {Array.from({ length: 49 }, (_, index) => <i key={index} />)}
              </div>
              <code>[1, 32, 14, 14]</code>
            </div>
          </section>

          <section id="source" className={styles.workspace}>
            <div className={styles.workspaceHeading}>
              <div>
                <p className={styles.eyebrow}>CONTROLLED INSPECTION</p>
                <h2>Choose the evidence path.</h2>
              </div>
              <ol>
                <li><span>1</span>Input</li>
                <li><span>2</span>Layer</li>
                <li><span>3</span>Channels</li>
              </ol>
            </div>

            <div className={styles.sourceTabs} role="tablist" aria-label="Image source">
              <button
                type="button"
                role="tab"
                aria-selected={sourceMode === "sample"}
                className={sourceMode === "sample" ? styles.selectedTab : ""}
                onClick={() => setSourceMode("sample")}
              >
                Registered samples
              </button>
              <button
                type="button"
                role="tab"
                aria-selected={sourceMode === "upload"}
                className={sourceMode === "upload" ? styles.selectedTab : ""}
                onClick={() => setSourceMode("upload")}
              >
                Temporary upload
              </button>
            </div>

            <div className={styles.workspaceGrid}>
              <article className={styles.sourcePanel}>
                {sourceMode === "sample" ? (
                  <>
                    <div className={styles.panelHeading}>
                      <div><span>ALLOWLIST</span><strong>One sample per class</strong></div>
                      <code>{samples.length}/10 ready</code>
                    </div>
                    <div className={styles.sampleGrid}>
                      {samples.map((sample) => (
                        <button
                          type="button"
                          key={sample.id}
                          className={sample.id === sampleId ? styles.selectedSample : ""}
                          aria-pressed={sample.id === sampleId}
                          onClick={() => setSampleId(sample.id)}
                        >
                          <Image
                            src={sample.image_data_uri}
                            alt={`${sample.label} Fashion-MNIST sample`}
                            width={56}
                            height={56}
                            unoptimized
                          />
                          <span>{sample.label}</span>
                        </button>
                      ))}
                    </div>
                  </>
                ) : (
                  <div className={styles.uploadPanel}>
                    <span className={styles.uploadIcon}><UploadIcon /></span>
                    <h3>Inspect your own image.</h3>
                    <p>PNG or JPEG · up to 1 MB · resized to 28 × 28 · never persisted</p>
                    <input
                      ref={uploadRef}
                      id="cnn-upload"
                      type="file"
                      accept="image/png,image/jpeg"
                      onChange={(event) => setUpload(event.target.files?.[0] ?? null)}
                    />
                    <label htmlFor="cnn-upload">
                      <UploadIcon />
                      {upload ? "Replace image" : "Choose image"}
                    </label>
                    {upload && (
                      <div className={styles.uploadFile}>
                        <span>READY</span>
                        <strong>{upload.name}</strong>
                        <small>{Math.ceil(upload.size / 1024)} KB · {upload.type}</small>
                      </div>
                    )}
                  </div>
                )}
              </article>

              <article className={styles.configurationPanel}>
                <div className={styles.panelHeading}>
                  <div><span>REPRESENTATION</span><strong>Select layer and channels</strong></div>
                  <code>{channels.length}/{MAX_SELECTED_CHANNELS}</code>
                </div>
                <fieldset>
                  <legend>Observable layer</legend>
                  <div className={styles.layerSelector}>
                    {summary?.layers.map((item) => (
                      <button
                        key={item.id}
                        type="button"
                        aria-pressed={item.id === layer}
                        className={item.id === layer ? styles.selectedLayer : ""}
                        onClick={() => selectLayer(item.id)}
                      >
                        <span>{item.id === "block1_relu" ? "L1" : "L2"}</span>
                        <div><strong>{item.label}</strong><small>{item.tensor_shape.join(" × ")}</small></div>
                      </button>
                    ))}
                  </div>
                </fieldset>
                <fieldset>
                  <legend>Channels</legend>
                  <div className={styles.channelSelector}>
                    {Array.from(
                      { length: currentLayer?.channels ?? 16 },
                      (_, channel) => (
                        <button
                          key={channel}
                          type="button"
                          aria-pressed={channels.includes(channel)}
                          className={channels.includes(channel) ? styles.selectedChannel : ""}
                          onClick={() => toggleChannel(channel)}
                        >
                          {String(channel).padStart(2, "0")}
                        </button>
                      )
                    )}
                  </div>
                </fieldset>
                <button
                  type="button"
                  className={styles.inspectButton}
                  disabled={busy}
                  onClick={() => void inspect()}
                >
                  {running ? "Running PyTorch inference…" : "Run feature-map inspection"}
                  <ArrowIcon />
                </button>
              </article>
            </div>
          </section>

          {loading && (
            <section className={styles.loadingPanel} aria-live="polite">
              <span /><span /><span />
              <p>Loading registered Fashion-MNIST evidence…</p>
            </section>
          )}

          {!loading && result && summary && (
            <>
              <section id="representation" className={styles.resultOverview}>
                <article className={styles.inputCard}>
                  <div className={styles.cardLabel}>PREPROCESSED INPUT</div>
                  <Image
                    src={result.input.image_data_uri}
                    alt="Image submitted to the registered CNN"
                    width={148}
                    height={148}
                    unoptimized
                  />
                  <div>
                    <strong>{result.input.registered_label ?? "Temporary upload"}</strong>
                    <span>{result.input.tensor_shape.join(" × ")}</span>
                  </div>
                </article>

                <article className={styles.predictionCard}>
                  <div className={styles.cardLabel}>MODEL OUTPUT</div>
                  <div className={styles.predictionHeadline}>
                    <div>
                      <small>PREDICTED CLASS</small>
                      <strong>{result.prediction.predicted_class}</strong>
                    </div>
                    <div className={styles.confidenceRing} style={{
                      "--confidence": `${result.prediction.confidence * 360}deg`
                    } as React.CSSProperties}>
                      <span>{(result.prediction.confidence * 100).toFixed(1)}%</span>
                    </div>
                  </div>
                  <div className={styles.probabilities}>
                    {rankedProbabilities.slice(0, 4).map((probability) => (
                      <div key={probability.class_index}>
                        <span>{probability.class_name}</span>
                        <i><b style={{ width: `${probability.probability * 100}%` }} /></i>
                        <code>{(probability.probability * 100).toFixed(1)}%</code>
                      </div>
                    ))}
                  </div>
                </article>

                <article className={styles.tensorCard}>
                  <div className={styles.cardLabel}>TENSOR CONTEXT</div>
                  <strong>{result.representation.layer.label}</strong>
                  <p>{result.representation.layer.operation}</p>
                  <dl>
                    <div><dt>Activation</dt><dd>{result.representation.activation_tensor_shape.join(" × ")}</dd></div>
                    <div><dt>Selected</dt><dd>{result.representation.maps.length} channels</dd></div>
                    <div><dt>Display</dt><dd>independent min–max</dd></div>
                  </dl>
                </article>
              </section>

              <section className={styles.mapsSection}>
                <div className={styles.sectionHeading}>
                  <div>
                    <p className={styles.eyebrow}>FEATURE-MAP MATRIX</p>
                    <h2>{result.representation.layer.label}</h2>
                  </div>
                  <p>{result.representation.comparison_rule}</p>
                </div>
                <div className={styles.mapsGrid}>
                  {result.representation.maps.map((featureMap) => (
                    <FeatureMapTile
                      key={`${featureMap.layer}-${featureMap.channel}`}
                      featureMap={featureMap}
                    />
                  ))}
                </div>
              </section>

              <section id="evidence" className={styles.evidenceSection}>
                <div>
                  <p className={styles.eyebrow}>EVIDENCE BOUNDARY</p>
                  <h2>Activation is not explanation.</h2>
                  <p>
                    Feature maps show where a registered channel responds after a forward pass.
                    They do not establish causality, feature importance or production readiness.
                  </p>
                  <div className={styles.evidenceMetric}>
                    <span>HELD-OUT EVALUATION</span>
                    <strong>{summary.evaluation.correct}/{summary.evaluation.samples}</strong>
                    <small>{(summary.evaluation.accuracy * 100).toFixed(2)}% accuracy · curated 900-image source</small>
                  </div>
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
            </>
          )}

          {!loading && !result && (
            <section className={styles.emptyPanel}>
              <strong>No registered CNN evidence is available.</strong>
              <p>Start FastAPI and retry. The frontend will not fabricate feature maps.</p>
            </section>
          )}

          <footer>
            <span>Project 02 · Deep Learning Visual Lab Platform</span>
            <span>Next.js → FastAPI → registered PyTorch checkpoint</span>
          </footer>
        </div>
      </main>
    </div>
  );
}
