# 04-neural-network-visual-explainer

## 🧠 Descripción

Herramienta visual para explicar los fundamentos de una red neuronal básica.

Este proyecto pertenece a la ruta:

```txt
Building Projects
```

y acompaña directamente al proyecto:

```txt
AI Engineer Proyecto 07 — neural-network-foundations-lab
```

Mientras AI Engineer trabaja el fundamento técnico de redes neuronales con más profundidad, este Building Project convierte esos conceptos en una explicación visual, clara y publicable.

La idea es mostrar de forma sencilla cómo una entrada pasa por una red:

```txt
input
→ pesos
→ bias
→ suma ponderada
→ activación
→ predicción
→ loss
→ training loop conceptual
```

Este proyecto no busca crear una librería de redes neuronales.

Busca crear una herramienta visual que ayude a entender qué ocurre dentro de una red simple.

---

## 🎯 Objetivo

Crear un visual explainer que muestre paso a paso cómo una red neuronal procesa una entrada y genera una salida.

El objetivo es explicar:

* Input.
* Pesos.
* Bias.
* Neurona.
* Activación.
* Predicción.
* Loss.
* Training loop conceptual.

---

## 👤 Usuario objetivo

* Estudiante de Deep Learning.
* AI Engineer en formación.
* Persona que quiere entender redes neuronales visualmente.
* Reclutador técnico viendo evidencia de aprendizaje.
* Yo mismo como constructor de portafolio visual.

---

## 🧱 Arquitectura esperada

```txt
Input simple
      ↓
Neuron / Layer
      ↓
Weights and Bias
      ↓
Weighted Sum
      ↓
Activation
      ↓
Prediction
      ↓
Loss Explanation
      ↓
Training Loop Timeline
      ↓
Visual Explanation
```

---

## 🔁 Flujo técnico

```txt
data example
→ define neuron
→ calculate weighted sum
→ apply activation
→ generate prediction
→ calculate loss
→ show training step
→ export visual explanation
```

---

## 🧩 Módulos

### Módulo 1 — Input Example

Crear entradas simples para explicar la red.

Incluye:

* Una o varias features.
* Valores numéricos pequeños.
* Explicación del input.
* Visualización inicial.

Pregunta central:

```txt
¿Qué recibe una red neuronal antes de hacer una predicción?
```

---

### Módulo 2 — Weight and Bias Cards

Explicar pesos y bias.

Incluye:

* Peso.
* Bias.
* Suma ponderada.
* Influencia de cada input.
* Tarjetas visuales.

Pregunta central:

```txt
¿Cómo influyen los pesos y bias en la salida de una neurona?
```

---

### Módulo 3 — Weighted Sum Viewer

Mostrar el cálculo interno de una neurona.

Incluye:

* Multiplicación input × peso.
* Suma de valores.
* Adición del bias.
* Resultado antes de activación.

Pregunta central:

```txt
¿Qué ocurre antes de aplicar una función de activación?
```

---

### Módulo 4 — Activation Viewer

Mostrar una activación simple.

Puede incluir:

* ReLU.
* Sigmoid.
* Tanh conceptual.
* Entrada antes de activación.
* Salida después de activación.

Pregunta central:

```txt
¿Por qué una red necesita funciones de activación?
```

---

### Módulo 5 — Prediction Card

Mostrar la predicción de la red.

Incluye:

* Output.
* Interpretación.
* Diferencia entre valor calculado y significado.
* Ejemplo visual.

Pregunta central:

```txt
¿Qué representa la salida de una red neuronal?
```

---

### Módulo 6 — Loss Explanation

Explicar error o pérdida.

Incluye:

* Valor real.
* Valor predicho.
* Diferencia.
* Loss simple.
* Explicación visual.

Pregunta central:

```txt
¿Cómo sabe la red que se equivocó?
```

---

### Módulo 7 — Training Loop Timeline

Crear una línea visual del entrenamiento.

Incluye:

* Forward pass.
* Loss.
* Backward conceptual.
* Actualización.
* Nueva predicción.
* Repetición.

Pregunta central:

```txt
¿Qué se repite durante el entrenamiento?
```

---

## 🧪 Labs

### tec-labs

* `tec-forward-pass-visual-lab`
* `tec-weight-bias-card-lab`
* `tec-weighted-sum-viewer-lab`
* `tec-activation-function-viewer-lab`
* `tec-loss-explanation-lab`
* `tec-training-loop-timeline-lab`

### docs-labs

* `docs-neural-network-storytelling-lab`
* `docs-visual-deep-learning-explanation-lab`

---

## 📊 Métricas / Evidencia

Este proyecto no se mide principalmente por accuracy.

Se mide por claridad visual y comprensión.

Evidencia esperada:

* Diagrama de forward pass.
* Tarjetas de input, pesos y bias.
* Visual de suma ponderada.
* Comparación antes/después de activación.
* Ejemplo de predicción.
* Ejemplo de loss.
* Timeline de training loop.
* Capturas.
* README visual.
* Mini demo local.

---

## 🚀 Estado actual

Pendiente / por iniciar.

---

## 🧭 Ciclo de trabajo

```txt
Semana 1 → Input, neurona, pesos, bias y forward pass
Semana 2 → Activación, predicción, loss y tarjetas visuales
Semana 3 → Training loop timeline, labs, README, capturas y cierre
```

---

## 📌 Próximos pasos

* Definir ejemplo numérico simple.
* Crear visual de input.
* Crear tarjetas de pesos y bias.
* Mostrar weighted sum.
* Agregar activación.
* Explicar predicción.
* Explicar loss.
* Crear timeline de entrenamiento.
* Documentar labs.
* Preparar capturas.
* Publicar repo.

---

## ✅ Entregable final

Al terminar este proyecto debe existir:

* Visual explainer de red neuronal.
* Tarjetas de input, pesos, bias y activación.
* Diagrama de forward pass.
* Explicación de weighted sum.
* Explicación de loss.
* Timeline de training loop.
* Labs documentados.
* README profesional.
* Capturas u outputs visibles.
* Conexión clara con `neural-network-foundations-lab`.

---

## 🧭 Regla final

```txt
Una red neuronal no debe quedarse como caja negra.
Debo poder mostrar cómo una entrada se transforma paso a paso.

Visualizar es una forma de dominar.
```

Este proyecto debe demostrar que puedo explicar una red neuronal básica de forma visual, no solo escribir código que entrena.
