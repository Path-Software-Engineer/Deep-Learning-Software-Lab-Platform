# Building Projects Roadmap — Plan 2

## 🧠 Deep Learning Visual Tools

Esta organización reúne los proyectos del **Plan 2 — Deep Learning Visual Tools** dentro de **Building Projects**.

Este plan acompaña directamente al:

```txt id="bp2-ai-relation"
AI Engineer Plan 2 — Deep Learning Core
```

La idea central es construir herramientas pequeñas, visuales y terminables que expliquen conceptos de Deep Learning de forma clara.

Mientras AI Engineer profundiza en PyTorch, tensores, redes neuronales, CNNs, autoencoders, training loops y fundamentos de Transformers, Building Projects convierte esos conceptos en evidencia visible:

```txt id="bp2-core"
concepto profundo
→ visualización
→ demo pequeña
→ tarjetas explicativas
→ notas técnicas
→ README claro
→ capturas
```

Building Projects no reemplaza los labs profundos de AI Engineer.

Los traduce en herramientas que puedan mostrarse, explicarse y publicarse.

---

# 🎯 Objetivo general

Construir herramientas visuales de Deep Learning capaces de:

* Explicar cómo funciona una red neuronal.
* Mostrar visualmente un forward pass.
* Explicar pesos, bias, activaciones y loss.
* Visualizar filtros y feature maps de CNNs.
* Mostrar reconstrucción y representación latente en autoencoders.
* Convertir conceptos difíciles en tarjetas claras.
* Crear demos pequeñas para GitHub.
* Fortalecer storytelling técnico.
* Acompañar la ruta principal sin inflar el alcance.

---

# 🔗 Regla de match del Plan 2

Building Projects hará match solo con los proyectos impares de AI Engineer.

```txt id="bp2-match-rule"
Proyecto 07 IA → Proyecto 04 Building
Proyecto 08 IA → Nada
Proyecto 09 IA → Proyecto 05 Building
Proyecto 10 IA → Nada
Proyecto 11 IA → Proyecto 06 Building
Proyecto 12 IA → Nada
```

Esto significa que este plan tendrá **3 proyectos**, no 6.

Cada proyecto Building toma como referencia la duración del proyecto IA correspondiente.

---

# 🗺️ Cronograma Plan 2

| Semana Building |                    Proyecto Building | Match IA |  Duración | Objetivo                                             |
| --------------- | -----------------------------------: | -------: | --------: | ---------------------------------------------------- |
| 14-16           | `04-neural-network-visual-explainer` |    IA 07 | 3 semanas | Explicar visualmente redes neuronales básicas        |
| 17-20           |     `05-cnn-feature-map-viewer-lite` |    IA 09 | 4 semanas | Visualizar filtros, convoluciones y feature maps     |
| 21-24           |   `06-autoencoder-latent-space-demo` |    IA 11 | 4 semanas | Mostrar reconstrucción, compresión y espacio latente |

Duración total del Plan 2:

```txt id="bp2-duration"
11 semanas
```

---

# 🧭 Filosofía de trabajo

Deep Learning puede volverse abstracto muy rápido.

Este plan existe para evitar que los conceptos se queden solo en código o fórmulas.

Regla central:

```txt id="bp2-philosophy"
Si no puedo visualizarlo, explicarlo y mostrarlo,
todavía no lo domino completamente.
```

Un Building Project de Deep Learning debe ser:

```txt id="bp2-values"
visual
claro
pequeño
explicable
documentado
terminable
```

No debe convertirse en un framework de Deep Learning.

No debe competir con el proyecto profundo de AI Engineer.

Debe ayudar a explicar lo aprendido.

---

# 🧩 Conceptos base

## Visual Tool

Una visual tool es una herramienta pequeña para mostrar un concepto técnico de forma entendible.

Puede incluir:

* gráficos;
* diagramas;
* tarjetas;
* mini demo;
* notebook visual;
* dashboard ligero;
* imágenes antes/después;
* tablas;
* explicaciones paso a paso.

---

## Demo pequeña

Una demo pequeña muestra un flujo limitado, pero claro.

Ejemplo:

```txt id="bp2-demo-example"
input
→ capa
→ activación
→ predicción
→ loss
→ explicación
```

No necesita ser un sistema grande.

Necesita ser entendible.

---

## Tarjeta explicativa

Una tarjeta explicativa convierte un concepto técnico en una unidad visual.

Ejemplo:

```txt id="bp2-card-example"
Concepto: Activation Function
Qué hace: transforma la salida de una capa.
Por qué importa: permite aprender relaciones no lineales.
Ejemplo visual: entrada → ReLU → salida.
Limitación: no explica por sí sola todo el entrenamiento.
```

---

## Lab visual

Un lab visual es un experimento pequeño para comparar o mostrar un concepto.

Ejemplo:

```txt id="bp2-lab-example"
Imagen original
→ filtro aplicado
→ feature map
→ explicación
```

Debe dejar evidencia visible.

---

# 📁 Proyectos del Plan 2

---

## 04 — neural-network-visual-explainer

### Match

```txt id="bp04-match"
AI Engineer Proyecto 07 — neural-network-foundations-lab
```

### Duración

```txt id="bp04-duration"
3 semanas
```

---

## 🧠 Descripción

Herramienta visual para explicar los fundamentos de una red neuronal básica.

Este proyecto acompaña al primer proyecto de Deep Learning en AI Engineer, donde se estudian forward pass, pesos, bias, activaciones, loss, gradiente y training loop.

Mientras AI Engineer trabaja el fundamento técnico con más profundidad, este Building Project lo convierte en una explicación visual y publicable.

La idea es mostrar:

```txt id="bp04-core"
input
→ pesos
→ bias
→ activación
→ predicción
→ loss
→ actualización conceptual
```

Este proyecto no busca crear una librería de redes neuronales.

Busca crear una herramienta que ayude a entender qué ocurre dentro de una red simple.

---

## 🎯 Objetivo

Crear un visual explainer que muestre de forma clara cómo una red neuronal procesa una entrada y produce una salida.

El objetivo es explicar:

* input;
* pesos;
* bias;
* neurona;
* activación;
* predicción;
* loss;
* training loop conceptual.

---

## 👤 Usuario objetivo

* Estudiante de Deep Learning.
* AI Engineer en formación.
* Persona que no entiende qué ocurre dentro de una red neuronal.
* Reclutador técnico viendo evidencia de aprendizaje.
* Yo mismo como constructor de portafolio visual.

---

## 🧱 Arquitectura esperada

```txt id="bp04-architecture"
Input simple
      ↓
Neuron / Layer
      ↓
Weights and Bias
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

```txt id="bp04-flow"
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

* una o varias features;
* valores numéricos pequeños;
* explicación del input;
* visualización inicial.

Pregunta central:

```txt id="bp04-q1"
¿Qué recibe una red neuronal antes de hacer una predicción?
```

---

### Módulo 2 — Weight and Bias Cards

Explicar pesos y bias.

Incluye:

* peso;
* bias;
* suma ponderada;
* influencia de cada input;
* tarjetas visuales.

Pregunta central:

```txt id="bp04-q2"
¿Cómo influyen los pesos y bias en la salida de una neurona?
```

---

### Módulo 3 — Activation Viewer

Mostrar una activación simple.

Puede incluir:

* ReLU.
* Sigmoid.
* Tanh conceptual.
* entrada antes de activación;
* salida después de activación.

Pregunta central:

```txt id="bp04-q3"
¿Por qué una red necesita funciones de activación?
```

---

### Módulo 4 — Prediction Card

Mostrar la predicción.

Incluye:

* output de la red;
* interpretación simple;
* diferencia entre valor calculado y significado;
* ejemplo visual.

Pregunta central:

```txt id="bp04-q4"
¿Qué representa la salida de una red neuronal?
```

---

### Módulo 5 — Loss Explanation

Explicar error o pérdida.

Incluye:

* valor real;
* valor predicho;
* diferencia;
* loss simple;
* explicación visual.

Pregunta central:

```txt id="bp04-q5"
¿Cómo sabe la red que se equivocó?
```

---

### Módulo 6 — Training Loop Timeline

Crear una línea visual del entrenamiento.

Incluye:

* forward pass;
* loss;
* backward conceptual;
* actualización;
* nueva predicción;
* repetición.

Pregunta central:

```txt id="bp04-q6"
¿Qué se repite durante el entrenamiento?
```

---

## 🧪 Labs

### tec-labs

#### `tec-forward-pass-visual-lab`

Visualizar un forward pass simple.

---

#### `tec-weight-bias-card-lab`

Crear tarjetas explicativas de pesos y bias.

---

#### `tec-activation-function-viewer-lab`

Comparar activaciones simples.

---

#### `tec-loss-explanation-lab`

Explicar loss con ejemplos numéricos pequeños.

---

#### `tec-training-loop-timeline-lab`

Crear timeline visual del ciclo de entrenamiento.

---

### docs-labs

#### `docs-neural-network-storytelling-lab`

Practicar explicación clara de redes neuronales.

---

## 📊 Métricas / Evidencia

* Número de tarjetas visuales.
* Diagrama de forward pass.
* Comparación antes/después de activación.
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

```txt id="bp04-cycle"
Semana 1 → Input, neurona, pesos, bias y forward pass
Semana 2 → Activación, predicción, loss y tarjetas visuales
Semana 3 → Training loop timeline, labs, README, capturas y cierre
```

---

## 📌 Próximos pasos

* Definir ejemplo simple.
* Crear visual de input.
* Crear tarjetas de pesos y bias.
* Mostrar forward pass.
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
* Explicación de loss.
* Timeline de training loop.
* Labs documentados.
* README profesional.
* Capturas o outputs visibles.
* Conexión clara con `neural-network-foundations-lab`.

---

## 🧭 Regla final

```txt id="bp04-rule"
Una red neuronal no debe quedarse como caja negra.
Debo poder mostrar cómo una entrada se transforma paso a paso.

Visualizar es una forma de dominar.
```

---

# 05 — cnn-feature-map-viewer-lite

### Match

```txt id="bp05-match"
AI Engineer Proyecto 09 — cnn-foundations-image-classifier
```

### Duración

```txt id="bp05-duration"
4 semanas
```

---

## 🧠 Descripción

Visualizador ligero de CNNs enfocado en imágenes, filtros, convoluciones, pooling y feature maps.

Este proyecto acompaña al proyecto de AI Engineer donde se estudian CNNs para clasificación de imágenes.

Mientras AI Engineer trabaja el entrenamiento, evaluación y arquitectura CNN con más profundidad, este Building Project se enfoca en hacer visible lo que una CNN está procesando.

La idea es mostrar:

```txt id="bp05-core"
imagen
→ filtro
→ convolución
→ feature map
→ pooling
→ predicción
→ explicación visual
```

Este proyecto no busca crear un clasificador avanzado.

Busca construir una herramienta visual para entender cómo una CNN transforma imágenes.

---

## 🎯 Objetivo

Crear un visualizador que muestre cómo una imagen pasa por filtros y genera feature maps.

El objetivo es explicar:

* entrada visual;
* filtro;
* convolución;
* feature map;
* pooling;
* predicción;
* errores simples;
* límites de interpretación.

---

## 👤 Usuario objetivo

* Estudiante de Computer Vision.
* AI Engineer en formación.
* Persona que quiere entender CNNs visualmente.
* Reclutador técnico viendo evidencia aplicada.
* Yo mismo como constructor de portafolio visual.

---

## 🧱 Arquitectura esperada

```txt id="bp05-architecture"
Image Input
      ↓
Filter Concept
      ↓
Convolution
      ↓
Feature Map
      ↓
Pooling
      ↓
Prediction Card
      ↓
Error Examples
      ↓
Visual Report
```

---

## 🔁 Flujo técnico

```txt id="bp05-flow"
image
→ preprocess
→ apply filter / explain convolution
→ generate feature map
→ show pooling effect
→ display prediction
→ compare examples
→ export visual report
```

---

## 🧩 Módulos

### Módulo 1 — Image Input

Cargar o seleccionar imágenes pequeñas.

Incluye:

* imagen original;
* tamaño;
* formato;
* preprocesamiento simple;
* vista previa.

Pregunta central:

```txt id="bp05-q1"
¿Qué recibe una CNN como entrada?
```

---

### Módulo 2 — Filter Concept Cards

Explicar filtros visualmente.

Incluye:

* filtro de borde;
* filtro de textura conceptual;
* matriz pequeña;
* efecto esperado;
* tarjeta explicativa.

Pregunta central:

```txt id="bp05-q2"
¿Qué intenta detectar un filtro?
```

---

### Módulo 3 — Feature Map Viewer

Mostrar mapas de características.

Incluye:

* imagen original;
* filtro aplicado;
* feature map resultante;
* comparación visual;
* interpretación.

Pregunta central:

```txt id="bp05-q3"
¿Qué muestra un feature map?
```

---

### Módulo 4 — Pooling Notes

Explicar pooling.

Incluye:

* reducción de tamaño;
* max pooling conceptual;
* información conservada;
* información perdida;
* visual comparativo.

Pregunta central:

```txt id="bp05-q4"
¿Por qué una CNN reduce dimensiones?
```

---

### Módulo 5 — Prediction Card

Mostrar una predicción simple.

Incluye:

* clase predicha;
* confianza si aplica;
* imagen;
* explicación corta;
* limitación.

Pregunta central:

```txt id="bp05-q5"
¿Cómo conecto la salida visual con una predicción entendible?
```

---

### Módulo 6 — Error Examples

Mostrar ejemplos donde el modelo puede confundirse.

Incluye:

* imagen difícil;
* predicción incorrecta;
* posible causa;
* limitación visual;
* advertencia.

Pregunta central:

```txt id="bp05-q6"
¿Qué tipo de errores puede cometer una CNN?
```

---

## 🧪 Labs

### tec-labs

#### `tec-image-input-preprocessing-lab`

Mostrar cómo cambia una imagen al prepararla para una CNN.

---

#### `tec-filter-visualization-lab`

Visualizar filtros simples.

---

#### `tec-feature-map-viewer-lab`

Generar y comparar feature maps.

---

#### `tec-pooling-effect-lab`

Mostrar el efecto de pooling.

---

#### `tec-cnn-error-example-lab`

Documentar ejemplos de error.

---

### docs-labs

#### `docs-cnn-visual-storytelling-lab`

Practicar explicación visual de CNNs.

---

## 📊 Métricas / Evidencia

* Imágenes originales.
* Filtros visualizados.
* Feature maps.
* Ejemplos de pooling.
* Prediction cards.
* Error examples.
* Capturas.
* README visual.
* Mini demo local.

---

## 🚀 Estado actual

Pendiente / por iniciar.

---

## 🧭 Ciclo de trabajo

```txt id="bp05-cycle"
Semana 1 → Imagen, preprocesamiento y filtros visuales
Semana 2 → Convolución, feature maps y pooling
Semana 3 → Prediction cards, ejemplos de error y visual report
Semana 4 → Labs, README, capturas y cierre
```

---

## 📌 Próximos pasos

* Elegir imágenes pequeñas.
* Crear módulo de carga visual.
* Crear tarjetas de filtros.
* Aplicar filtros simples.
* Mostrar feature maps.
* Explicar pooling.
* Crear prediction cards.
* Documentar errores.
* Preparar visual report.
* Cerrar labs.
* Agregar capturas.
* Publicar repo.

---

## ✅ Entregable final

Al terminar este proyecto debe existir:

* Visualizador CNN.
* Imágenes de ejemplo.
* Filtros visualizados.
* Feature maps.
* Notas de pooling.
* Prediction cards.
* Error examples.
* Labs documentados.
* README profesional.
* Capturas o outputs visibles.
* Conexión clara con `cnn-foundations-image-classifier`.

---

## 🧭 Regla final

```txt id="bp05-rule"
Una CNN no solo predice una clase.
Transforma una imagen en señales visuales.

Si veo las transformaciones,
entiendo mejor la arquitectura.
```

---

# 06 — autoencoder-latent-space-demo

### Match

```txt id="bp06-match"
AI Engineer Proyecto 11 — autoencoder-representation-lab
```

### Duración

```txt id="bp06-duration"
4 semanas
```

---

## 🧠 Descripción

Demo visual para explicar autoencoders, reconstrucción, compresión, denoising y espacio latente.

Este proyecto acompaña al proyecto de AI Engineer donde se estudian autoencoders y representación.

Mientras AI Engineer trabaja arquitectura, entrenamiento, reconstruction loss, latent representation, denoising y anomaly detection, este Building Project convierte esos conceptos en una demo visual clara.

La idea es mostrar:

```txt id="bp06-core"
input
→ encoder
→ latent space
→ decoder
→ reconstruction
→ error
→ visual explanation
```

Este proyecto no busca crear un sistema avanzado de detección de anomalías.

Busca mostrar cómo un autoencoder aprende a reconstruir y representar datos.

---

## 🎯 Objetivo

Crear una demo visual de autoencoder que muestre input, reconstrucción, representación latente y error.

El objetivo es explicar:

* encoder;
* bottleneck;
* latent vector;
* decoder;
* reconstruction;
* reconstruction error;
* denoising conceptual;
* anomalías conceptuales.

---

## 👤 Usuario objetivo

* Estudiante de Deep Learning.
* AI Engineer en formación.
* Persona que quiere entender autoencoders visualmente.
* Reclutador técnico viendo evidencia aplicada.
* Yo mismo como constructor de portafolio visual.

---

## 🧱 Arquitectura esperada

```txt id="bp06-architecture"
Input Data
      ↓
Encoder
      ↓
Latent Vector
      ↓
Decoder
      ↓
Reconstruction
      ↓
Reconstruction Error
      ↓
Denoising Example
      ↓
Anomaly Example
      ↓
Visual Demo
```

---

## 🔁 Flujo técnico

```txt id="bp06-flow"
input example
→ encode
→ show latent representation
→ decode
→ compare reconstruction
→ calculate error
→ show denoising / anomaly notes
→ export visual demo
```

---

## 🧩 Módulos

### Módulo 1 — Input vs Reconstruction

Mostrar entrada y reconstrucción.

Incluye:

* input original;
* output reconstruido;
* comparación visual;
* diferencia;
* explicación.

Pregunta central:

```txt id="bp06-q1"
¿Qué tan bien el autoencoder puede reconstruir la entrada?
```

---

### Módulo 2 — Encoder / Decoder Cards

Explicar las dos partes principales.

Incluye:

* encoder;
* bottleneck;
* decoder;
* compresión;
* reconstrucción;
* tarjetas visuales.

Pregunta central:

```txt id="bp06-q2"
¿Qué hace el encoder y qué hace el decoder?
```

---

### Módulo 3 — Latent Vector Card

Mostrar la representación latente.

Incluye:

* vector latente;
* dimensión reducida;
* compresión;
* significado conceptual;
* limitación.

Pregunta central:

```txt id="bp06-q3"
¿Qué representa el espacio latente?
```

---

### Módulo 4 — Reconstruction Error Notes

Explicar error de reconstrucción.

Incluye:

* diferencia input vs output;
* error promedio;
* zonas de mayor error;
* interpretación;
* limitaciones.

Pregunta central:

```txt id="bp06-q4"
¿Qué me dice el error de reconstrucción?
```

---

### Módulo 5 — Denoising Example

Mostrar reducción de ruido conceptual.

Incluye:

* input con ruido;
* reconstrucción limpia;
* comparación visual;
* explicación;
* advertencia.

Pregunta central:

```txt id="bp06-q5"
¿Cómo puede un autoencoder ayudar a reconstruir señales con ruido?
```

---

### Módulo 6 — Anomaly Example

Mostrar anomalías de forma conceptual.

Incluye:

* ejemplo normal;
* ejemplo extraño;
* error más alto;
* tarjeta de interpretación;
* límites.

Pregunta central:

```txt id="bp06-q6"
¿Por qué una anomalía puede tener mayor error de reconstrucción?
```

---

## 🧪 Labs

### tec-labs

#### `tec-input-reconstruction-lab`

Comparar entrada original contra reconstrucción.

---

#### `tec-latent-vector-card-lab`

Explicar representación latente.

---

#### `tec-reconstruction-error-lab`

Calcular y visualizar error de reconstrucción.

---

#### `tec-denoising-example-lab`

Mostrar ejemplo de denoising conceptual.

---

#### `tec-anomaly-reconstruction-lab`

Mostrar error mayor en ejemplos anómalos.

---

### docs-labs

#### `docs-autoencoder-visual-storytelling-lab`

Practicar explicación visual de autoencoders.

---

## 📊 Métricas / Evidencia

* Input original.
* Output reconstruido.
* Error de reconstrucción.
* Latent vector card.
* Denoising example.
* Anomaly example.
* Visual comparison.
* Capturas.
* README profesional.
* Demo local.

---

## 🚀 Estado actual

Pendiente / por iniciar.

---

## 🧭 Ciclo de trabajo

```txt id="bp06-cycle"
Semana 1 → Input, encoder, decoder y reconstrucción básica
Semana 2 → Latent space, reconstruction error y tarjetas visuales
Semana 3 → Denoising, anomaly example y visual demo
Semana 4 → Labs, README, capturas y cierre
```

---

## 📌 Próximos pasos

* Elegir dataset pequeño o ejemplos simples.
* Crear comparación input vs reconstruction.
* Crear tarjetas encoder/decoder.
* Mostrar latent vector.
* Calcular reconstruction error.
* Crear ejemplo de denoising.
* Crear ejemplo de anomalía.
* Preparar visual demo.
* Documentar labs.
* Agregar capturas.
* Publicar repo.

---

## ✅ Entregable final

Al terminar este proyecto debe existir:

* Demo visual de autoencoder.
* Input vs reconstruction.
* Encoder / decoder cards.
* Latent vector card.
* Reconstruction error notes.
* Denoising example.
* Anomaly example.
* Labs documentados.
* README profesional.
* Capturas o outputs visibles.
* Conexión clara con `autoencoder-representation-lab`.

---

## 🧭 Regla final

```txt id="bp06-rule"
Un autoencoder no solo comprime.
Aprende una representación que permite reconstruir.

La reconstrucción muestra lo que el modelo entendió.
El error muestra lo que no logró representar bien.
```

---

# 🧱 Ciclo general de cada proyecto

Cada proyecto del Plan 2 sigue este ciclo:

```txt id="bp2-cycle-general"
1. Definir concepto visual.
2. Definir usuario.
3. Definir qué debe entenderse.
4. Elegir ejemplo pequeño.
5. Crear README inicial.
6. Crear estructura mínima.
7. Crear primera visualización.
8. Agregar tarjetas explicativas.
9. Crear labs pequeños.
10. Probar si aplica.
11. Documentar decisiones.
12. Agregar capturas.
13. Preparar demo o evidencia.
14. Escribir aprendizajes.
15. Definir limitaciones.
16. Definir siguiente paso.
17. Publicar en GitHub.
18. Conectar con el proyecto IA correspondiente.
```

---

# 🗂️ Estructura recomendada del repositorio

```txt id="bp2-repo-structure"
Deep-Learning-Visual-Tools/
├── 04-neural-network-visual-explainer/
│   ├── data/
│   ├── src/
│   ├── reports/
│   ├── visuals/
│   ├── docs/
│   ├── labs/
│   ├── scripts/
│   └── README.md
│
├── 05-cnn-feature-map-viewer-lite/
│   ├── data/
│   ├── src/
│   ├── reports/
│   ├── visuals/
│   ├── docs/
│   ├── labs/
│   └── README.md
│
├── 06-autoencoder-latent-space-demo/
│   ├── data/
│   ├── src/
│   ├── reports/
│   ├── visuals/
│   ├── docs/
│   ├── labs/
│   └── README.md
│
└── README.md
```

---

# 📊 Nivel esperado al terminar Plan 2

| Área                                   | Nivel esperado |
| -------------------------------------- | -------------: |
| Explicación visual de redes neuronales |         8.5/10 |
| Forward pass conceptual                |           8/10 |
| Pesos, bias y activaciones             |           8/10 |
| Loss y training loop conceptual        |           8/10 |
| Visualización de CNNs                  |           8/10 |
| Feature maps                           |           8/10 |
| Filtros y convoluciones                |         7.5/10 |
| Pooling conceptual                     |         7.5/10 |
| Autoencoders                           |           8/10 |
| Latent space                           |           8/10 |
| Reconstruction error                   |           8/10 |
| Denoising conceptual                   |         7.5/10 |
| Storytelling técnico visual            |         8.5/10 |
| README profesional                     |         8.5/10 |
| Evidencia visual de aprendizaje        |           9/10 |

---

# 🧠 Resultado esperado del Plan 2

Al completar este plan, podré decir:

```txt id="bp2-result"
Sé convertir conceptos de Deep Learning en herramientas visuales.
Sé explicar una red neuronal paso a paso.
Sé mostrar qué ocurre en un forward pass.
Sé explicar activaciones y loss con claridad.
Sé visualizar feature maps de una CNN.
Sé explicar filtros, convoluciones y pooling.
Sé mostrar input vs reconstruction en autoencoders.
Sé explicar latent space y reconstruction error.
Sé convertir aprendizaje profundo en evidencia visual.
```

---

# 🧭 Regla final de avance

```txt id="bp2-final-rule"
No basta con entrenar.
Debo saber mostrar qué ocurre.

Deep Learning se entiende mejor cuando puedo visualizar sus transformaciones.
```

Frase guía:

```txt id="bp2-final-phrase"
AI Engineer me enseña la profundidad del modelo.
Building Projects me obliga a explicarlo visualmente.
```

---

# 👤 Autor

**Jean Franck Loa Rojas**

Building Projects Path Builder
Deep Learning Visual Tools • Neural Networks • CNNs • Autoencoders • Visual Storytelling • Technical Evidence
