"use client";

import { useCallback, useEffect, useState } from "react";

import { PlatformShell } from "@/components/platform/PlatformShell";
import { LabApiError, neuralNetworkApi } from "@/lib/api-client";
import type {
  ForwardTrace,
  NeuralNetworkSummary,
  TrainingHistory
} from "@/types/neural-network";

import { LossChart } from "./LossChart";
import { NetworkDiagram, type NodeSelection } from "./NetworkDiagram";
import styles from "./NeuralNetworkExplainer.module.css";
import { TraceInspector } from "./TraceInspector";

function formatError(error: unknown) {
  return error instanceof LabApiError
    ? error.message
    : "An unexpected client error interrupted the neural trace.";
}

function Metric({ label, value, detail }: { label: string; value: string; detail: string }) {
  return (
    <article className={styles.metric}>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </article>
  );
}

export function NeuralNetworkExplainer() {
  const [summary, setSummary] = useState<NeuralNetworkSummary | null>(null);
  const [history, setHistory] = useState<TrainingHistory | null>(null);
  const [trace, setTrace] = useState<ForwardTrace | null>(null);
  const [inputs, setInputs] = useState<[number, number]>([0, 1]);
  const [selection, setSelection] = useState<NodeSelection>({ layer: "hidden", index: 0 });
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadEvidence = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [summaryResult, historyResult, traceResult] = await Promise.all([
        neuralNetworkApi.summary(),
        neuralNetworkApi.trainingHistory(),
        neuralNetworkApi.forward([0, 1])
      ]);
      setSummary(summaryResult);
      setHistory(historyResult);
      setTrace(traceResult);
      setInputs([0, 1]);
      setSelection({ layer: "hidden", index: 0 });
    } catch (reason) {
      setError(formatError(reason));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let active = true;
    Promise.all([
      neuralNetworkApi.summary(),
      neuralNetworkApi.trainingHistory(),
      neuralNetworkApi.forward([0, 1])
    ])
      .then(([summaryResult, historyResult, traceResult]) => {
        if (!active) return;
        setSummary(summaryResult);
        setHistory(historyResult);
        setTrace(traceResult);
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

  const toggleInput = (index: 0 | 1) => {
    setInputs((current) => {
      const next: [number, number] = [...current];
      next[index] = current[index] === 0 ? 1 : 0;
      return next;
    });
  };

  const runForward = async () => {
    setRunning(true);
    setError(null);
    try {
      setTrace(await neuralNetworkApi.forward(inputs));
      setSelection({ layer: "hidden", index: 0 });
    } catch (reason) {
      setError(formatError(reason));
    } finally {
      setRunning(false);
    }
  };

  const busy = loading || running;

  return (
    <PlatformShell
      activeModule="neural-trace"
      sprint="Sprint 01"
      title="Neural Network Explainer"
      status={
        error
          ? "Engine unavailable"
          : busy
            ? "Reading evidence…"
            : "Checkpoint connected"
      }
      version={summary?.model_version ?? "xor-mlp-v1"}
      hasError={Boolean(error)}
    >
      <div className={styles.content}>
          {error && (
            <div className={styles.errorBanner} role="alert">
              <span>!</span>
              <div><strong>The trace could not continue</strong><p>{error}</p></div>
              <button type="button" onClick={() => void loadEvidence()}>Retry</button>
            </div>
          )}

          <section className={styles.hero}>
            <div>
              <p className={styles.eyebrow}>REGISTERED PYTORCH EVIDENCE</p>
              <h1>Follow every signal.<br /><em>Understand the network.</em></h1>
              <p>
                Choose an XOR observation and inspect the exact weights,
                preactivations and activations produced by the registered model.
              </p>
              <div className={styles.heroTags}>
                <span>2–4–1 MLP</span><span>tanh</span><span>sigmoid</span><span>17 parameters</span>
              </div>
            </div>
            <div className={styles.heroVisual} aria-hidden="true">
              <span className={styles.orbitOne} /><span className={styles.orbitTwo} />
              <strong>Σ</strong><i /><i /><i />
            </div>
          </section>

          <section id="experiment" className={styles.controlPanel}>
            <div>
              <p className={styles.eyebrow}>CONTROLLED XOR INPUT</p>
              <h2>Select an observation.</h2>
              <p>Input selection is local UI state; every neural value comes from FastAPI.</p>
            </div>
            <div className={styles.inputControls}>
              {inputs.map((value, index) => (
                <button
                  key={index}
                  type="button"
                  className={value === 1 ? styles.binaryOn : styles.binaryOff}
                  aria-label={`Toggle x${index + 1}`}
                  aria-pressed={value === 1}
                  disabled={busy}
                  onClick={() => toggleInput(index as 0 | 1)}
                >
                  <small>x{index + 1}</small>
                  <strong>{value}</strong>
                  <span>{value === 1 ? "active" : "inactive"}</span>
                </button>
              ))}
              <button
                type="button"
                className={styles.runButton}
                disabled={busy}
                onClick={() => void runForward()}
              >
                {running ? "Running forward pass" : "Run forward pass"} <span aria-hidden="true">→</span>
              </button>
            </div>
          </section>

          {loading && (
            <section className={styles.loadingPanel} aria-live="polite">
              <span /><span /><span /><p>Loading registered PyTorch evidence…</p>
            </section>
          )}

          {!loading && summary && history && trace ? (
            <>
              <section className={styles.metrics} aria-label="Registered model result">
                <Metric label="Epoch" value={history.configuration.epochs.toLocaleString()} detail="offline training" />
                <Metric label="Output probability" value={`${(trace.output * 100).toFixed(2)}%`} detail={`target ${trace.target}`} />
                <Metric label="Accuracy" value={`${(history.metrics.accuracy * 100).toFixed(1)}%`} detail="controlled XOR set" />
                <Metric label="Loss" value={trace.loss.toFixed(6)} detail="selected observation" />
              </section>

              <section id="network" className={styles.networkGrid}>
                <article className={styles.networkPanel}>
                  <div className={styles.panelHeading}>
                    <div>
                      <p className={styles.eyebrow}>FORWARD TRACE</p>
                      <h2>Signal flow · [{trace.inputs.join(", ")}]</h2>
                    </div>
                    <span className={styles.liveChip}><i /> contract v1</span>
                  </div>
                  <NetworkDiagram trace={trace} selection={selection} onSelect={setSelection} />
                </article>
                <TraceInspector trace={trace} selection={selection} />
              </section>

              <section id="learning" className={styles.learningSection}>
                <div className={styles.sectionHeading}>
                  <div>
                    <p className={styles.eyebrow}>LEARNING EVIDENCE</p>
                    <h2>Offline training, reproducible artifacts.</h2>
                  </div>
                  <p>
                    {history.configuration.optimizer} · seed {history.seed} ·
                    learning rate {history.configuration.learning_rate}
                  </p>
                </div>
                <div className={styles.learningGrid}>
                  <article className={styles.lossPanel}>
                    <div className={styles.panelHeading}>
                      <div><small>TRAINING HISTORY</small><strong>Loss by epoch</strong></div>
                      <span>{history.points.length} registered points</span>
                    </div>
                    <LossChart points={history.points} />
                  </article>
                  <article className={styles.artifactPanel}>
                    <p className={styles.eyebrow}>CHECKPOINT</p>
                    <h3>{summary.model_version}</h3>
                    <dl>
                      <div><dt>Engine</dt><dd>{summary.engine}</dd></div>
                      <div><dt>File</dt><dd>{summary.checkpoint.file}</dd></div>
                      <div><dt>Size</dt><dd>{summary.checkpoint.bytes.toLocaleString()} bytes</dd></div>
                      <div><dt>SHA-256</dt><dd><code>{summary.checkpoint.sha256.slice(0, 12)}…</code></dd></div>
                    </dl>
                    <span className={styles.verified}><i /> checksum verified by the API</span>
                  </article>
                </div>
              </section>

              <section id="limits" className={styles.limitations}>
                <div>
                  <p className={styles.eyebrow}>EVIDENCE BOUNDARY</p>
                  <h2>Inspectable does not mean causal.</h2>
                  <p>
                    The module exposes values produced by a small educational model.
                    It does not present internal activations as causal explanations.
                  </p>
                </div>
                <ul>
                  {summary.limitations.map((limitation, index) => (
                    <li key={limitation}><span>0{index + 1}</span>{limitation}</li>
                  ))}
                </ul>
              </section>
            </>
          ) : !loading ? (
            <section className={styles.emptyPanel}>
              <strong>No registered evidence is available.</strong>
              <p>Start FastAPI and retry. The frontend will not fabricate a trace.</p>
            </section>
          ) : null}

          <footer>
            <span>Project 02 · Deep Learning Visual Lab Platform</span>
            <span>Next.js → FastAPI → registered PyTorch artifact</span>
          </footer>
      </div>
    </PlatformShell>
  );
}
