import type { KeyboardEvent } from "react";

import type { ForwardTrace, LayerTrace } from "@/types/neural-network";

import styles from "./NeuralNetworkExplainer.module.css";

export interface NodeSelection {
  layer: "hidden" | "output";
  index: number;
}

interface NetworkDiagramProps {
  trace: ForwardTrace;
  selection: NodeSelection;
  onSelect: (selection: NodeSelection) => void;
}

const inputPositions = [
  { x: 80, y: 125 },
  { x: 80, y: 275 }
];
const outputPosition = { x: 650, y: 210 };

function edgeClass(weight: number) {
  return weight >= 0 ? styles.positiveEdge : styles.negativeEdge;
}

function selectOnKeyboard(
  event: KeyboardEvent<SVGGElement>,
  selection: NodeSelection,
  onSelect: (selection: NodeSelection) => void
) {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    onSelect(selection);
  }
}

export function NetworkDiagram({ trace, selection, onSelect }: NetworkDiagramProps) {
  const hidden = trace.layers[0];
  const output = trace.layers[1];
  const hiddenPositions = hidden.activations.map((_, index) => ({
    x: 360,
    y: 55 + (310 * index) / Math.max(hidden.activations.length - 1, 1)
  }));

  return (
    <div className={styles.networkStage}>
      <div className={styles.layerLabels} aria-hidden="true">
        <span>INPUT · 2</span>
        <span>HIDDEN · {hidden.activations.length}</span>
        <span>OUTPUT · 1</span>
      </div>
      <svg viewBox="0 0 730 420" role="img" aria-label="Interactive two-layer neural network">
        <g aria-hidden="true">
          {hidden.weights.map((weights, hiddenIndex) =>
            weights.map((weight, inputIndex) => (
              <line
                key={`input-${inputIndex}-hidden-${hiddenIndex}`}
                x1={inputPositions[inputIndex].x}
                y1={inputPositions[inputIndex].y}
                x2={hiddenPositions[hiddenIndex].x}
                y2={hiddenPositions[hiddenIndex].y}
                className={edgeClass(weight)}
                strokeWidth={1 + Math.min(Math.abs(weight) * 1.2, 5)}
              />
            ))
          )}
          {output.weights[0].map((weight, hiddenIndex) => (
            <line
              key={`hidden-${hiddenIndex}-output`}
              x1={hiddenPositions[hiddenIndex].x}
              y1={hiddenPositions[hiddenIndex].y}
              x2={outputPosition.x}
              y2={outputPosition.y}
              className={edgeClass(weight)}
              strokeWidth={1 + Math.min(Math.abs(weight) * 1.2, 5)}
            />
          ))}
        </g>
        <g className={styles.inputNodes} aria-hidden="true">
          {inputPositions.map((position, index) => (
            <g key={index} transform={`translate(${position.x} ${position.y})`}>
              <circle r="37" />
              <text y="-3" textAnchor="middle">x{index + 1}</text>
              <text y="17" textAnchor="middle" className={styles.nodeValue}>
                {trace.inputs[index].toFixed(2)}
              </text>
            </g>
          ))}
        </g>
        <g className={styles.computedNodes}>
          {hiddenPositions.map((position, index) => {
            const selected = selection.layer === "hidden" && selection.index === index;
            const nodeSelection: NodeSelection = { layer: "hidden", index };
            return (
              <g
                key={`hidden-${index}`}
                transform={`translate(${position.x} ${position.y})`}
                className={selected ? styles.selectedNode : styles.node}
                role="button"
                tabIndex={0}
                aria-label={`Hidden neuron ${index + 1}, activation ${hidden.activations[index].toFixed(4)}`}
                onClick={() => onSelect(nodeSelection)}
                onKeyDown={(event) => selectOnKeyboard(event, nodeSelection, onSelect)}
              >
                <circle r="32" />
                <text y="-3" textAnchor="middle">h{index + 1}</text>
                <text y="16" textAnchor="middle" className={styles.nodeValue}>
                  {hidden.activations[index].toFixed(2)}
                </text>
              </g>
            );
          })}
          <g
            transform={`translate(${outputPosition.x} ${outputPosition.y})`}
            className={selection.layer === "output" ? styles.selectedOutput : styles.outputNode}
            role="button"
            tabIndex={0}
            aria-label={`Output neuron, probability ${trace.output.toFixed(4)}`}
            onClick={() => onSelect({ layer: "output", index: 0 })}
            onKeyDown={(event) =>
              selectOnKeyboard(event, { layer: "output", index: 0 }, onSelect)
            }
          >
            <circle r="44" />
            <text y="-4" textAnchor="middle">ŷ</text>
            <text y="18" textAnchor="middle" className={styles.nodeValue}>
              {trace.output.toFixed(3)}
            </text>
          </g>
        </g>
      </svg>
      <div className={styles.edgeLegend}>
        <span><i className={styles.positiveSwatch} /> positive weight</span>
        <span><i className={styles.negativeSwatch} /> negative weight</span>
        <span>line width = magnitude</span>
      </div>
    </div>
  );
}

export function selectedLayer(trace: ForwardTrace, selection: NodeSelection): LayerTrace {
  return selection.layer === "hidden" ? trace.layers[0] : trace.layers[1];
}
