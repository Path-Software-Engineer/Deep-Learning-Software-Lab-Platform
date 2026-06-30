# 06-autoencoder-latent-space-demo

## 🧠 Descripción

Demo visual para explicar autoencoders, reconstrucción, compresión, denoising y espacio latente.

Este proyecto pertenece a la ruta:

```txt
Building Projects
```

y acompaña directamente al proyecto:

```txt
AI Engineer Proyecto 11 — autoencoder-representation-lab
```

Mientras AI Engineer trabaja arquitectura, entrenamiento, reconstruction loss, latent representation, denoising y anomaly detection, este Building Project convierte esos conceptos en una demo visual clara.

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

Este proyecto no busca crear un sistema avanzado de detección de anomalías.

Busca mostrar cómo un autoencoder aprende a reconstruir y representar datos.

---

## 🎯 Objetivo

Crear una demo visual de autoencoder que muestre input, reconstrucción, representación latente y error.

El objetivo es explicar:

* Encoder.
* Bottleneck.
* Latent vector.
* Decoder.
* Reconstruction.
* Reconstruction error.
* Denoising conceptual.
* Anomalías conceptuales.

---

## 👤 Usuario objetivo

* Estudiante de Deep Learning.
* AI Engineer en formación.
* Persona que quiere entender autoencoders visualmente.
* Reclutador técnico viendo evidencia aplicada.
* Yo mismo como constructor de portafolio visual.

---

## 🧱 Arquitectura esperada

```txt
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

```txt
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

### Módulo 2 — Encoder / Decoder Cards

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

### Módulo 3 — Latent Vector Card

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

### Módulo 4 — Latent Space Viewer

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

### Módulo 5 — Reconstruction Error Notes

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

### Módulo 6 — Denoising Example

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

### Módulo 7 — Anomaly Example

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

### tec-labs

* `tec-input-reconstruction-lab`
* `tec-encoder-decoder-card-lab`
* `tec-latent-vector-card-lab`
* `tec-latent-space-viewer-lab`
* `tec-reconstruction-error-lab`
* `tec-denoising-example-lab`
* `tec-anomaly-reconstruction-lab`

### docs-labs

* `docs-autoencoder-visual-storytelling-lab`
* `docs-representation-learning-explanation-lab`

---

## 📊 Métricas / Evidencia

Este proyecto puede generar:

* Input original.
* Output reconstruido.
* Comparación input vs reconstruction.
* Error de reconstrucción.
* Latent vector card.
* Latent space visualization.
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

```txt
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
* Visualizar latent space.
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
* Latent space viewer.
* Reconstruction error notes.
* Denoising example.
* Anomaly example.
* Labs documentados.
* README profesional.
* Capturas u outputs visibles.
* Conexión clara con `autoencoder-representation-lab`.

---

## 🧭 Regla final

```txt
Un autoencoder no solo comprime.
Aprende una representación que permite reconstruir.

La reconstrucción muestra lo que el modelo entendió.
El error muestra lo que no logró representar bien.
```

Este proyecto debe demostrar que puedo convertir representación profunda en una demo visual entendible.
