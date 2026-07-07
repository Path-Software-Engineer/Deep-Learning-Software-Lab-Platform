# Path Software Engineer Roadmap — Plan 2

## 🧠 Deep Learning Software Lab Platform

Esta organización reúne el proyecto del **Plan 2 — Deep Learning Software Lab Platform**.

Este plan pertenece a la ruta mayor:

```txt
Path Software Engineer
```

El objetivo de este segundo plan es convertir los fundamentos de Deep Learning en una aplicación de software visual, robusta y documentada.

Este plan no busca entrenar redes neuronales profundas como objetivo principal.

Ese trabajo profundo pertenece a:

```txt
Path AI Engineer — Plan 2 — Deep Learning Core
```

Path Software Engineer toma esos conceptos y los convierte en una plataforma visual capaz de explicar cómo funcionan:

```txt
redes neuronales básicas
→ CNNs
→ autoencoders
→ representaciones latentes
→ visualizaciones
→ tarjetas explicativas
→ demos
→ dashboard
→ documentación profesional
```

La idea central es construir software aplicado que ayude a entender Deep Learning de forma visual, progresiva y presentable.

---

## 🎯 Objetivo general

Construir una plataforma visual de software para explicar fundamentos de Deep Learning.

Al terminar este plan, la plataforma debe permitir:

* Explicar una red neuronal básica paso a paso.
* Mostrar inputs, pesos, bias, suma ponderada y activaciones.
* Explicar predicción, loss y training loop conceptual.
* Visualizar imágenes, filtros, convoluciones, pooling y feature maps.
* Mostrar cómo una CNN transforma imágenes en señales visuales.
* Explicar autoencoders, encoder, decoder, reconstrucción y error.
* Mostrar representaciones latentes de forma simple.
* Crear demos visuales entendibles para usuarios no expertos.
* Documentar sprints, historias, decisiones y evidencias.
* Construir una aplicación presentable, no solo scripts sueltos.

---

## 🧭 Filosofía de trabajo

Este plan trabaja con la lógica de **Path Software Engineer**.

Cada plan contiene una aplicación robusta.

Cada aplicación está dividida en sprints.

Cada sprint toma un antiguo Building Project y lo convierte en un módulo de software integrado.

```txt
Antes:
Building Project 4
Building Project 5
Building Project 6

Ahora:
Software Engineer Project 2
├── Sprint 1 — Neural Network Visual Explainer
├── Sprint 2 — CNN Feature Map Viewer
└── Sprint 3 — Autoencoder Latent Space Demo
```

La regla central es:

```txt
Path AI Engineer = profundidad técnica.
Path Software Engineer = software aplicado que convierte esa profundidad en producto.
```

Este plan no construye software vacío.

Construye software para explicar, visualizar y presentar conceptos de Deep Learning.

---

## 🔗 Relación con Path AI Engineer

Este plan acompaña proyectos impares del **Plan 2 de Path AI Engineer — Deep Learning Core**.

```txt
Path AI Engineer Proyecto 07
→ neural-network-foundations-lab
→ Software Engineer Plan 2 / Sprint 1

Path AI Engineer Proyecto 09
→ cnn-foundations-image-classifier
→ Software Engineer Plan 2 / Sprint 2

Path AI Engineer Proyecto 11
→ autoencoder-representation-lab
→ Software Engineer Plan 2 / Sprint 3
```

Mientras Path AI Engineer profundiza en arquitectura, entrenamiento, tensores, backpropagation y evaluación, Path Software Engineer construye una plataforma visual que permite explicar esos conceptos con claridad.

---

## 🧩 Conceptos base

### Proyecto principal

Un proyecto principal en Path Software Engineer es una aplicación robusta de software.

Debe poder incluir, según corresponda:

* Frontend.
* Backend.
* AI services.
* Datos o ejemplos.
* Visualizaciones.
* Reportes.
* Demos.
* Tests mínimos.
* Documentación funcional.
* Documentación técnica.
* Historias de usuario.
* Historias técnicas.
* Sprints.
* Evidencia visible.

En este plan, el proyecto principal es:

```txt
02-deep-learning-visual-lab-platform
```

---

### Sprint

Un sprint es una etapa funcional dentro del proyecto principal.

Cada sprint tiene:

* Sprint Goal.
* User Stories.
* Technical Stories.
* Acceptance Criteria.
* Definition of Done.
* Sprint Review.
* Sprint Retrospective.
* Evidencia visible.

En este plan, los sprints son:

```txt
Sprint 1 — Neural Network Visual Explainer
Sprint 2 — CNN Feature Map Viewer
Sprint 3 — Autoencoder Latent Space Demo
```

---

### Módulo

Un módulo es una parte funcional dentro de un sprint.

Ejemplo:

```txt
Módulo: Weighted Sum Viewer
```

Significa:

```txt
Mostrar cómo los inputs se multiplican por pesos,
se suman,
se combina el bias,
y se obtiene el valor antes de activación.
```

---

### Lab

Un lab es un experimento pequeño y cerrado.

En este plan, los labs ayudan a probar y documentar conceptos visuales de Deep Learning.

Regla:

```txt
Un lab no debe quedar suelto.
Debe reforzar una decisión del sprint o mejorar la explicación visual.
```

---

## 🧪 Tipos de labs

### tec-labs

Laboratorios técnicos para probar conceptos visuales.

Ejemplos:

* Forward pass visual.
* Weight and bias cards.
* Weighted sum viewer.
* Activation function viewer.
* Feature map viewer.
* Pooling effect.
* Input vs reconstruction.
* Latent vector card.
* Reconstruction error.

---

### docs-labs

Laboratorios de explicación y storytelling técnico.

Ejemplos:

* Neural network storytelling.
* Visual Deep Learning explanation.
* CNN visual storytelling.
* Computer Vision result explanation.
* Autoencoder visual storytelling.
* Representation learning explanation.

---

### product-labs

Laboratorios para mejorar la experiencia visual del usuario.

Ejemplos:

* Card layout.
* Visual explanation flow.
* Dashboard navigation.
* User-facing terminology.
* Error and limitation language.

---

## ☁️ Criterio de despliegue

En este plan, el despliegue no es el primer objetivo.

Primero se construye una demo local clara.

Después se puede preparar una versión desplegable.

La regla será:

```txt
Primero visual local funcionando.
Luego dashboard simple.
Luego integración frontend/backend si aplica.
Luego Docker o deploy simple.
Después mejoras de plataforma.
```

Opciones posibles:

```txt
Frontend → Vercel / Firebase Hosting / Cloud Storage
Backend → Cloud Run / Render
AI service → Cloud Run / local service
Reports → carpeta reports/ o Cloud Storage
```

El foco principal del Plan 2 es:

```txt
visualización clara
→ explicación técnica
→ experiencia de usuario
→ documentación
→ evidencia visual
```

---

## 🗺️ Cronograma Plan 2

| Semana | Sprint | Módulo | Objetivo |
| ------ | ------ | ------ | -------- |
| 1-3 | Sprint 1 | Neural Network Visual Explainer | Explicar red neuronal básica, forward pass, activación, predicción, loss y training loop conceptual |
| 4-7 | Sprint 2 | CNN Feature Map Viewer | Visualizar imagen, filtros, convolución, feature maps, pooling, prediction cards y errores |
| 8-11 | Sprint 3 | Autoencoder Latent Space Demo | Explicar encoder, decoder, latent space, reconstrucción, error, denoising y anomalías conceptuales |

Duración total aproximada:

```txt
11 semanas
```

---

# 📁 Proyecto del Plan 2

## 02 — deep-learning-visual-lab-platform

### Objetivo

Crear una plataforma visual para explicar fundamentos de Deep Learning mediante módulos interactivos, tarjetas, diagramas, outputs y documentación.

El proyecto integra:

```txt
neural network visual explainer
→ CNN feature map viewer
→ autoencoder latent space demo
```

---

### Flujo general

```txt
ejemplos simples
→ procesamiento visual
→ cálculo conceptual
→ representación gráfica
→ explicación paso a paso
→ tarjetas visuales
→ reportes
→ dashboard
→ documentación
```

---

### Arquitectura esperada

```txt
02-deep-learning-visual-lab-platform/
│
├── frontend/
│   └── visual-dashboard/
│
├── backend/
│   └── api/
│
├── ai-services/
│   └── deep-learning-visual-service/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── reports/
│   ├── figures/
│   ├── summaries/
│   ├── visual-cards/
│   └── outputs/
│
├── docs/
│   ├── architecture.md
│   ├── decisions.md
│   ├── user-stories.md
│   ├── technical-stories.md
│   ├── sprint-01-neural-network-explainer.md
│   ├── sprint-02-cnn-feature-map-viewer.md
│   └── sprint-03-autoencoder-latent-space-demo.md
│
├── labs/
│   ├── tec-labs/
│   ├── docs-labs/
│   └── product-labs/
│
├── tests/
├── scripts/
└── deployment/
```

---

# 🚀 Sprint 1 — Neural Network Visual Explainer

## Match

```txt
Path AI Engineer Proyecto 07 — neural-network-foundations-lab
```

## Base anterior

```txt
04-neural-network-visual-explainer
```

## Objetivo

Construir el primer módulo visual de la plataforma para explicar los fundamentos de una red neuronal básica.

Debe mostrar cómo una entrada pasa por:

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

## Aprendizajes principales

* Input vector.
* Pesos.
* Bias.
* Neurona.
* Weighted sum.
* Función de activación.
* Predicción.
* Loss conceptual.
* Forward pass.
* Training loop conceptual.
* Explicación visual.
* Storytelling técnico.

## Módulos

* Input Example.
* Weight and Bias Cards.
* Weighted Sum Viewer.
* Activation Viewer.
* Prediction Card.
* Loss Explanation.
* Training Loop Timeline.

## Labs

* `tec-forward-pass-visual-lab`
* `tec-weight-bias-card-lab`
* `tec-weighted-sum-viewer-lab`
* `tec-activation-function-viewer-lab`
* `tec-loss-explanation-lab`
* `tec-training-loop-timeline-lab`
* `docs-neural-network-storytelling-lab`
* `docs-visual-deep-learning-explanation-lab`

## Entregable del sprint

* Visual explainer de red neuronal.
* Tarjetas de input, pesos y bias.
* Diagrama de forward pass.
* Visual de suma ponderada.
* Visual de activación.
* Tarjeta de predicción.
* Explicación de loss.
* Timeline de training loop.
* README del sprint.
* Capturas u outputs visibles.

---

# 🖼️ Sprint 2 — CNN Feature Map Viewer

## Match

```txt
Path AI Engineer Proyecto 09 — cnn-foundations-image-classifier
```

## Base anterior

```txt
05-cnn-feature-map-viewer-lite
```

## Objetivo

Agregar un módulo visual para explicar cómo una CNN transforma imágenes usando filtros, convoluciones, feature maps y pooling.

Debe mostrar el flujo:

```txt
imagen
→ preprocesamiento
→ filtro
→ convolución
→ feature map
→ pooling
→ predicción
→ ejemplos de error
→ visual report
```

## Aprendizajes principales

* Image input.
* Preprocessing.
* Canales de color.
* Filtros.
* Convolución conceptual.
* Feature maps.
* Pooling.
* Prediction cards.
* Ejemplos de error.
* Limitaciones de interpretación.
* Visualización técnica.

## Módulos

* Image Input.
* Image Preprocessing.
* Filter Concept Cards.
* Feature Map Viewer.
* Pooling Notes.
* Prediction Card.
* Error Examples.

## Labs

* `tec-image-input-preprocessing-lab`
* `tec-filter-visualization-lab`
* `tec-feature-map-viewer-lab`
* `tec-pooling-effect-lab`
* `tec-prediction-card-lab`
* `tec-cnn-error-example-lab`
* `docs-cnn-visual-storytelling-lab`
* `docs-computer-vision-result-explanation-lab`

## Entregable del sprint

* Visualizador CNN.
* Imágenes de ejemplo.
* Visual de preprocesamiento.
* Filtros visualizados.
* Feature maps.
* Notas de pooling.
* Prediction cards.
* Error examples.
* Visual report.
* README del sprint.
* Capturas u outputs visibles.

---

# 🧬 Sprint 3 — Autoencoder Latent Space Demo

## Match

```txt
Path AI Engineer Proyecto 11 — autoencoder-representation-lab
```

## Base anterior

```txt
06-autoencoder-latent-space-demo
```

## Objetivo

Agregar una demo visual para explicar autoencoders, reconstrucción, compresión, denoising, error y espacio latente.

Debe mostrar el flujo:

```txt
input
→ encoder
→ latent vector
→ decoder
→ reconstruction
→ reconstruction error
→ denoising example
→ anomaly example
→ visual demo
```

## Aprendizajes principales

* Encoder.
* Decoder.
* Bottleneck.
* Latent vector.
* Latent space.
* Reconstrucción.
* Reconstruction error.
* Denoising conceptual.
* Anomalías conceptuales.
* Representación visual.

## Módulos

* Input vs Reconstruction.
* Encoder / Decoder Cards.
* Latent Vector Card.
* Latent Space Viewer.
* Reconstruction Error Notes.
* Denoising Example.
* Anomaly Example.

## Labs

* `tec-input-reconstruction-lab`
* `tec-encoder-decoder-card-lab`
* `tec-latent-vector-card-lab`
* `tec-latent-space-viewer-lab`
* `tec-reconstruction-error-lab`
* `tec-denoising-example-lab`
* `tec-anomaly-reconstruction-lab`
* `docs-autoencoder-visual-storytelling-lab`
* `docs-representation-learning-explanation-lab`

## Entregable del sprint

* Demo visual de autoencoder.
* Input vs reconstruction.
* Encoder / decoder cards.
* Latent vector card.
* Latent space viewer.
* Reconstruction error notes.
* Denoising example.
* Anomaly example.
* README del sprint.
* Capturas u outputs visibles.

---

# 📊 Nivel esperado al terminar Plan 2

| Área | Nivel esperado |
| ---- | -------------: |
| Explicación visual de redes neuronales | 8.5/10 |
| Forward pass conceptual | 8.5/10 |
| Pesos, bias y suma ponderada | 8.5/10 |
| Activaciones conceptuales | 8/10 |
| Loss conceptual | 8/10 |
| Training loop storytelling | 8/10 |
| Visualización de CNNs | 8/10 |
| Filtros y convoluciones conceptuales | 8/10 |
| Feature maps | 8/10 |
| Pooling | 7.5/10 |
| Prediction cards | 8/10 |
| Autoencoder explanation | 8/10 |
| Latent space explanation | 7.5/10 |
| Reconstruction error | 8/10 |
| Denoising conceptual | 7.5/10 |
| Anomaly explanation conceptual | 7.5/10 |
| Frontend visual para IA | 8/10 |
| AI services para visualización | 7.5/10 |
| Documentación técnica | 9/10 |
| Storytelling visual | 9/10 |

---

# 🧠 Resultado esperado del Plan 2

Al completar este plan, podré decir:

```txt
Sé construir una plataforma visual para explicar Deep Learning.
Sé mostrar cómo una red neuronal transforma una entrada.
Sé explicar pesos, bias, suma ponderada, activación, predicción y loss.
Sé visualizar cómo una CNN procesa imágenes mediante filtros y feature maps.
Sé explicar pooling y limitaciones visuales.
Sé mostrar cómo un autoencoder comprime, reconstruye y genera error de reconstrucción.
Sé convertir conceptos profundos en módulos visuales entendibles.
Sé documentar sprints, historias, decisiones y evidencias.
Sé construir software aplicado a IA, no solo notebooks o scripts.
```

---

# 🧭 Regla final

```txt
No construiré software vacío.
Construiré software que explique inteligencia artificial.

No dejaré Deep Learning como caja negra.
Lo convertiré en visuales, tarjetas, demos y documentación.

Path AI Engineer me da profundidad técnica.
Path Software Engineer convierte esa profundidad en producto visual.
```

---

# 👤 Autor

**Jean Franck Loa Rojas**

Path Software Engineer Builder  
Deep Learning Visual Systems • Neural Networks • CNN Visualization • Autoencoders • Visual Storytelling • AI Software Platforms • Technical Documentation
