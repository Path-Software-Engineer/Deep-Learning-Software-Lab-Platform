# 02-deep-learning-visual-lab-platform

## 🧠 Descripción

**Deep Learning Visual Lab Platform** es una aplicación de software aplicada a Deep Learning para explicar visualmente cómo funcionan redes neuronales básicas, CNNs y autoencoders.

Este proyecto pertenece a la ruta:

```txt
Path Software Engineer
```

y forma parte de:

```txt
Plan 2 — Deep Learning Software Lab Platform
```

Este proyecto acompaña directamente al:

```txt
Path AI Engineer
Plan 2 — Deep Learning Core
```

Mientras Path AI Engineer trabaja la profundidad técnica de redes neuronales, CNNs, entrenamiento, tensores, backpropagation, pérdida y representación latente, este proyecto convierte esos conceptos en una plataforma visual, clara, documentada y orientada a producto.

La idea es integrar tres antiguos Building Projects dentro de una sola aplicación robusta:

```txt
04-neural-network-visual-explainer
05-cnn-feature-map-viewer-lite
06-autoencoder-latent-space-demo
```

Ahora esos proyectos ya no viven como repositorios separados.

Se convierten en **3 sprints principales** dentro de una sola plataforma visual de Deep Learning.

---

## 🎯 Objetivo

Crear una plataforma visual que permita explicar conceptos fundamentales de Deep Learning mediante módulos interactivos, tarjetas, diagramas, visualizaciones y reportes.

El objetivo es explicar:

* Input.
* Pesos.
* Bias.
* Neurona.
* Activación.
* Predicción.
* Loss.
* Training loop conceptual.
* Imagen de entrada.
* Filtros.
* Convolución.
* Feature maps.
* Pooling.
* Encoder.
* Decoder.
* Latent vector.
* Reconstruction.
* Reconstruction error.
* Denoising conceptual.
* Anomalías conceptuales.

Este proyecto no busca entrenar modelos avanzados.

Busca construir una aplicación visual que ayude a entender qué ocurre dentro de modelos profundos simples.

---

## 👤 Usuario objetivo

* Estudiante de Deep Learning.
* AI Engineer en formación.
* Persona que quiere entender redes neuronales visualmente.
* Persona que quiere entender CNNs visualmente.
* Persona que quiere entender autoencoders visualmente.
* Reclutador técnico viendo evidencia aplicada.
* Yo mismo como constructor de portafolio visual.

---

## 🧱 Arquitectura esperada

```txt
Deep Learning Visual Lab Platform
│
├── Frontend
│   └── Visual dashboard / explainer UI
│
├── Backend
│   └── API para módulos, ejemplos y resultados visuales
│
├── AI Services
│   └── lógica de cálculos, visualizaciones y ejemplos conceptuales
│
├── Reports
│   └── tarjetas, figuras, outputs y notas visuales
│
└── Docs
    └── historias, decisiones, sprints y metodología visual
```

---

## 🔁 Flujo general de la plataforma

```txt
concepto
→ ejemplo pequeño
→ cálculo o transformación
→ visualización
→ explicación
→ tarjeta visual
→ reporte
→ dashboard
→ documentación
```

El proyecto debe convertir conceptos internos de Deep Learning en evidencia visual entendible.

---

## 🧩 Sprints principales

## Sprint 1 — Neural Network Explainer

### Match

```txt
Path AI Engineer Proyecto 07 — neural-network-foundations-lab
```

### Base anterior

```txt
04-neural-network-visual-explainer
```

### Objetivo

Crear el primer módulo de la plataforma para explicar visualmente cómo una red neuronal básica procesa una entrada y genera una salida.

La idea es mostrar:

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

### Módulos

#### Módulo 1 — Input Example

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

#### Módulo 2 — Weight and Bias Cards

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

#### Módulo 3 — Weighted Sum Viewer

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

#### Módulo 4 — Activation Viewer

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

#### Módulo 5 — Prediction Card

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

#### Módulo 6 — Loss Explanation

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

#### Módulo 7 — Training Loop Timeline

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

## Sprint 2 — CNN Feature Map Viewer

### Match

```txt
Path AI Engineer Proyecto 09 — cnn-foundations-image-classifier
```

### Base anterior

```txt
05-cnn-feature-map-viewer-lite
```

### Objetivo

Agregar un módulo visual para mostrar cómo una imagen pasa por filtros y genera feature maps.

La idea es mostrar:

```txt
imagen
→ preprocesamiento
→ filtro
→ convolución
→ feature map
→ pooling
→ predicción
→ explicación visual
```

### Módulos

#### Módulo 1 — Image Input

Cargar o seleccionar imágenes pequeñas.

Incluye:

* Imagen original.
* Tamaño.
* Formato.
* Vista previa.
* Descripción del input.

Pregunta central:

```txt
¿Qué recibe una CNN como entrada?
```

---

#### Módulo 2 — Image Preprocessing

Mostrar cómo se prepara una imagen antes de entrar al modelo.

Incluye:

* Resize.
* Normalización conceptual.
* Conversión a tensor conceptual.
* Canales de color.
* Comparación antes/después.

Pregunta central:

```txt
¿Por qué una imagen debe prepararse antes de pasar por una CNN?
```

---

#### Módulo 3 — Filter Concept Cards

Explicar filtros visualmente.

Incluye:

* Filtro de borde.
* Filtro de textura conceptual.
* Matriz pequeña.
* Efecto esperado.
* Tarjeta explicativa.

Pregunta central:

```txt
¿Qué intenta detectar un filtro?
```

---

#### Módulo 4 — Feature Map Viewer

Mostrar mapas de características.

Incluye:

* Imagen original.
* Filtro aplicado.
* Feature map resultante.
* Comparación visual.
* Interpretación.

Pregunta central:

```txt
¿Qué muestra un feature map?
```

---

#### Módulo 5 — Pooling Notes

Explicar pooling.

Incluye:

* Reducción de tamaño.
* Max pooling conceptual.
* Información conservada.
* Información perdida.
* Visual comparativo.

Pregunta central:

```txt
¿Por qué una CNN reduce dimensiones?
```

---

#### Módulo 6 — Prediction Card

Mostrar una predicción simple.

Incluye:

* Imagen.
* Clase predicha.
* Confianza si aplica.
* Explicación corta.
* Limitación.

Pregunta central:

```txt
¿Cómo conecto la salida visual con una predicción entendible?
```

---

#### Módulo 7 — Error Examples

Mostrar ejemplos donde el modelo puede confundirse.

Incluye:

* Imagen difícil.
* Predicción incorrecta.
* Posible causa.
* Limitación visual.
* Advertencia.

Pregunta central:

```txt
¿Qué tipo de errores puede cometer una CNN?
```

---

## Sprint 3 — Autoencoder Latent Space Demo

### Match

```txt
Path AI Engineer Proyecto 11 — autoencoder-representation-lab
```

### Base anterior

```txt
06-autoencoder-latent-space-demo
```

### Objetivo

Agregar una demo visual para explicar autoencoders, reconstrucción, compresión, denoising y espacio latente.

La idea es mostrar:

```txt
input
→ encoder
→ latent space
→ decoder
→ reconstruction
→ error
→ visual explanation
```

### Módulos

#### Módulo 1 — Input vs Reconstruction

Mostrar entrada y reconstrucción.

Incluye:

* Input original.
* Output reconstruido.
* Comparación visual.
* Diferencia.
* Explicación.

Pregunta central:

```txt
¿Qué tan bien el autoencoder puede reconstruir la entrada?
```

---

#### Módulo 2 — Encoder / Decoder Cards

Explicar las dos partes principales.

Incluye:

* Encoder.
* Bottleneck.
* Decoder.
* Compresión.
* Reconstrucción.
* Tarjetas visuales.

Pregunta central:

```txt
¿Qué hace el encoder y qué hace el decoder?
```

---

#### Módulo 3 — Latent Vector Card

Mostrar la representación latente.

Incluye:

* Vector latente.
* Dimensión reducida.
* Compresión.
* Significado conceptual.
* Limitación.

Pregunta central:

```txt
¿Qué representa el espacio latente?
```

---

#### Módulo 4 — Latent Space Viewer

Visualizar el espacio latente de forma simple.

Puede incluir:

* Puntos en 2D.
* Representaciones comprimidas.
* Agrupaciones visuales.
* Comparación entre ejemplos.
* Interpretación limitada.

Pregunta central:

```txt
¿Qué puedo observar cuando reduzco datos a una representación latente?
```

---

#### Módulo 5 — Reconstruction Error Notes

Explicar error de reconstrucción.

Incluye:

* Diferencia input vs output.
* Error promedio.
* Zonas de mayor error.
* Interpretación.
* Limitaciones.

Pregunta central:

```txt
¿Qué me dice el error de reconstrucción?
```

---

#### Módulo 6 — Denoising Example

Mostrar reducción de ruido conceptual.

Incluye:

* Input con ruido.
* Reconstrucción limpia.
* Comparación visual.
* Explicación.
* Advertencia.

Pregunta central:

```txt
¿Cómo puede un autoencoder ayudar a reconstruir señales con ruido?
```

---

#### Módulo 7 — Anomaly Example

Mostrar anomalías de forma conceptual.

Incluye:

* Ejemplo normal.
* Ejemplo extraño.
* Error más alto.
* Tarjeta de interpretación.
* Límites.

Pregunta central:

```txt
¿Por qué una anomalía puede tener mayor error de reconstrucción?
```

---

## 🧪 Labs

### Sprint 1 — Neural Network Explainer Labs

#### tec-labs

* `tec-forward-pass-visual-lab`
* `tec-weight-bias-card-lab`
* `tec-weighted-sum-viewer-lab`
* `tec-activation-function-viewer-lab`
* `tec-loss-explanation-lab`
* `tec-training-loop-timeline-lab`

#### docs-labs

* `docs-neural-network-storytelling-lab`
* `docs-visual-deep-learning-explanation-lab`

---

### Sprint 2 — CNN Feature Map Viewer Labs

#### tec-labs

* `tec-image-input-preprocessing-lab`
* `tec-filter-visualization-lab`
* `tec-feature-map-viewer-lab`
* `tec-pooling-effect-lab`
* `tec-prediction-card-lab`
* `tec-cnn-error-example-lab`

#### docs-labs

* `docs-cnn-visual-storytelling-lab`
* `docs-computer-vision-result-explanation-lab`

---

### Sprint 3 — Autoencoder Latent Space Demo Labs

#### tec-labs

* `tec-input-reconstruction-lab`
* `tec-encoder-decoder-card-lab`
* `tec-latent-vector-card-lab`
* `tec-latent-space-viewer-lab`
* `tec-reconstruction-error-lab`
* `tec-denoising-example-lab`
* `tec-anomaly-reconstruction-lab`

#### docs-labs

* `docs-autoencoder-visual-storytelling-lab`
* `docs-representation-learning-explanation-lab`

---

## 📊 Métricas / Evidencia

Este proyecto no se mide principalmente por accuracy.

Se mide por claridad visual, explicación técnica y evidencia publicable.

Evidencia esperada:

* Diagrama de forward pass.
* Tarjetas de input, pesos y bias.
* Visual de suma ponderada.
* Comparación antes/después de activación.
* Ejemplo de predicción.
* Ejemplo de loss.
* Timeline de training loop.
* Imágenes originales.
* Imágenes preprocesadas.
* Filtros visualizados.
* Feature maps.
* Ejemplos de pooling.
* Prediction cards.
* Error examples.
* Input vs reconstruction.
* Encoder / decoder cards.
* Latent vector card.
* Latent space viewer.
* Reconstruction error notes.
* Denoising example.
* Anomaly example.
* Capturas.
* README profesional.
* Demo local.

---

## 🚀 Estado actual

Pendiente / por iniciar.

---

## 🧭 Ciclo de trabajo

```txt
Sprint 1 → Neural Network Explainer
Sprint 2 → CNN Feature Map Viewer
Sprint 3 → Autoencoder Latent Space Demo
```

Cada sprint debe cerrar con:

* módulo funcional;
* explicación visual;
* labs documentados;
* outputs o capturas;
* README actualizado;
* Sprint Review;
* Sprint Retrospective;
* conexión clara con Path AI Engineer.

---

## 📌 Próximos pasos

### Sprint 1

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

### Sprint 2

* Elegir imágenes pequeñas.
* Crear módulo de carga visual.
* Crear paso de preprocesamiento.
* Crear tarjetas de filtros.
* Aplicar filtros simples.
* Mostrar feature maps.
* Explicar pooling.
* Crear prediction cards.
* Documentar errores.
* Preparar visual report.

### Sprint 3

* Elegir dataset pequeño o ejemplos simples.
* Crear comparación input vs reconstruction.
* Crear tarjetas encoder/decoder.
* Mostrar latent vector.
* Visualizar latent space.
* Calcular reconstruction error.
* Crear ejemplo de denoising.
* Crear ejemplo de anomalía.
* Preparar visual demo.

---

## ✅ Entregable final

Al terminar este proyecto debe existir:

* Plataforma visual de Deep Learning.
* Visual explainer de red neuronal básica.
* Visualizador CNN.
* Demo visual de autoencoder.
* Tarjetas de input, pesos, bias y activación.
* Diagrama de forward pass.
* Explicación de weighted sum.
* Explicación de loss.
* Timeline de training loop.
* Visual de preprocesamiento de imágenes.
* Filtros visualizados.
* Feature maps.
* Notas de pooling.
* Prediction cards.
* Error examples.
* Input vs reconstruction.
* Encoder / decoder cards.
* Latent vector card.
* Latent space viewer.
* Reconstruction error notes.
* Denoising example.
* Anomaly example.
* Labs documentados.
* README profesional.
* Capturas u outputs visibles.
* Conexión clara con Deep Learning Core de Path AI Engineer.

---

## 🧭 Regla final

```txt
Un modelo profundo no debe quedarse como caja negra.

Debo poder mostrar cómo una entrada se transforma paso a paso.

Visualizar es una forma de dominar.
```

Este proyecto debe demostrar que puedo explicar Deep Learning con evidencia visual, no solo entrenar modelos.

---

## 👤 Autor

**Jean Franck Loa Rojas**

Path Software Engineer Builder  
Deep Learning Visual Tools • Neural Networks • CNNs • Autoencoders • Visual Explanations • AI Software Products • Technical Documentation
