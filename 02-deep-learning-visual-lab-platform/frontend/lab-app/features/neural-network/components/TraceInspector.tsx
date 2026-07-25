import type { ForwardTrace } from "@/types/neural-network";

import { selectedLayer, type NodeSelection } from "./NetworkDiagram";
import styles from "./NeuralNetworkExplainer.module.css";

interface TraceInspectorProps {
  trace: ForwardTrace;
  selection: NodeSelection;
}

function signed(value: number) {
  return `${value >= 0 ? "+" : ""}${value.toFixed(4)}`;
}

export function TraceInspector({ trace, selection }: TraceInspectorProps) {
  const layer = selectedLayer(trace, selection);
  const index = selection.index;
  const weights = layer.weights[index];

  return (
    <aside className={styles.inspector} aria-live="polite">
      <p className={styles.eyebrow}>SELECTED NODE</p>
      <div className={styles.inspectorTitle}>
        <span>{selection.layer === "hidden" ? `h${index + 1}` : "ŷ"}</span>
        <div>
          <strong>{selection.layer === "hidden" ? "Hidden neuron" : "Output neuron"}</strong>
          <small>{layer.operation}</small>
        </div>
      </div>
      <dl className={styles.traceValues}>
        {weights.map((weight, weightIndex) => (
          <div key={weightIndex}>
            <dt>w{weightIndex + 1}</dt>
            <dd className={weight >= 0 ? styles.positiveValue : styles.negativeValue}>
              {signed(weight)}
            </dd>
          </div>
        ))}
        <div>
          <dt>bias</dt>
          <dd>{signed(layer.biases[index])}</dd>
        </div>
      </dl>
      <div className={styles.equation}>
        <span>preactivation</span>
        <strong>{signed(layer.preactivations[index])}</strong>
      </div>
      <div className={styles.equation}>
        <span>activation</span>
        <strong>{layer.activations[index].toFixed(6)}</strong>
      </div>
      <p className={styles.inspectorNote}>
        These values come from the registered PyTorch checkpoint. They expose
        the forward computation without claiming a causal explanation.
      </p>
    </aside>
  );
}
