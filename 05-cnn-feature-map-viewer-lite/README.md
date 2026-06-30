# 05-cnn-feature-map-viewer-lite

## 🧠 Descripción

Visualizador ligero de CNNs enfocado en imágenes, filtros, convoluciones, pooling y feature maps.

Este proyecto pertenece a la ruta:

```txt
Building Projects
```

y acompaña directamente al proyecto:

```txt
AI Engineer Proyecto 09 — cnn-foundations-image-classifier
```

Mientras AI Engineer trabaja el entrenamiento, evaluación y arquitectura CNN con más profundidad, este Building Project se enfoca en hacer visible lo que una CNN procesa internamente.

La idea es mostrar:

```txt
imagen
→ filtro
→ convolución
→ feature map
→ pooling
→ predicción
→ explicación visual
```

Este proyecto no busca crear un clasificador avanzado.

Busca construir una herramienta visual para entender cómo una CNN transforma imágenes en señales útiles.

---

## 🎯 Objetivo

Crear un visualizador que muestre cómo una imagen pasa por filtros y genera feature maps.

El objetivo es explicar:

* Entrada visual.
* Preprocesamiento.
* Filtros.
* Convolución.
* Feature maps.
* Pooling.
* Predicción.
* Ejemplos de error.
* Límites de interpretación.

---

## 👤 Usuario objetivo

* Estudiante de Computer Vision.
* AI Engineer en formación.
* Persona que quiere entender CNNs visualmente.
* Reclutador técnico viendo evidencia aplicada.
* Yo mismo como constructor de portafolio visual.

---

## 🧱 Arquitectura esperada

```txt
Image Input
      ↓
Preprocessing
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

```txt
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

### Módulo 2 — Image Preprocessing

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

### Módulo 3 — Filter Concept Cards

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

### Módulo 4 — Feature Map Viewer

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

### Módulo 5 — Pooling Notes

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

### Módulo 6 — Prediction Card

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

### Módulo 7 — Error Examples

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

## 🧪 Labs

### tec-labs

* `tec-image-input-preprocessing-lab`
* `tec-filter-visualization-lab`
* `tec-feature-map-viewer-lab`
* `tec-pooling-effect-lab`
* `tec-prediction-card-lab`
* `tec-cnn-error-example-lab`

### docs-labs

* `docs-cnn-visual-storytelling-lab`
* `docs-computer-vision-result-explanation-lab`

---

## 📊 Métricas / Evidencia

Este proyecto puede generar:

* Imágenes originales.
* Imágenes preprocesadas.
* Filtros visualizados.
* Feature maps.
* Ejemplos de pooling.
* Prediction cards.
* Error examples.
* Visual report.
* Capturas.
* README visual.
* Mini demo local.

---

## 🚀 Estado actual

Pendiente / por iniciar.

---

## 🧭 Ciclo de trabajo

```txt
Semana 1 → Imagen, preprocesamiento y filtros visuales
Semana 2 → Convolución, feature maps y pooling
Semana 3 → Prediction cards, ejemplos de error y visual report
Semana 4 → Labs, README, capturas y cierre
```

---

## 📌 Próximos pasos

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
* Cerrar labs.
* Agregar capturas.
* Publicar repo.

---

## ✅ Entregable final

Al terminar este proyecto debe existir:

* Visualizador CNN.
* Imágenes de ejemplo.
* Visual de preprocesamiento.
* Filtros visualizados.
* Feature maps.
* Notas de pooling.
* Prediction cards.
* Error examples.
* Labs documentados.
* README profesional.
* Capturas u outputs visibles.
* Conexión clara con `cnn-foundations-image-classifier`.

---

## 🧭 Regla final

```txt
Una CNN no solo predice una clase.
Transforma una imagen en señales visuales.

Si veo las transformaciones,
entiendo mejor la arquitectura.
```

Este proyecto debe demostrar que puedo explicar visión computacional con evidencia visual, no solo entrenar un modelo.
