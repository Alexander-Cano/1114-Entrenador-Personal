# NOMBRE DEL PROYECTO: KINESIS

**Proyecto:** Entrenador Personal 
**Stack:** HTML, CSS, Python

<hr>

## 1. Resumen Ejecutivo

Aplicación web ligera diseñada para ayudar al usuario a realizar rutinas de ejercicio guiadas desde casa, mantener el registro de sus sesiones y visualizar su progreso diario para asegurar la constancia.

<hr>

## 2. Definición de Roles

* **Usuario (Entrenante):** Selecciona su nivel, realiza rutinas paso a paso y registra sus datos al finalizar cada sesión.

* **Entrenador (Aplicación):** Organiza el catálogo de rutinas, presenta la secuencia de ejercicios durante la rutina y calcula los resúmenes de avance.

* **Administrador:** Gestiona y actualiza el contenido de ejercicios y rutinas disponibles.


<hr>

## 3. Alcance del Sistema

### Incluido

* Registro básico de datos del usuario.

* Catálogo de rutinas agrupadas por nivel (Principiante, Intermedio, Avanzado).

* Módulo de entrenamiento con flujo paso a paso por ejercicio.

* Captura de datos por sesión (ejercicios, repeticiones y tiempo invertido).

* Historial de entrenamientos y resumen de días completados.

* Recordatorios básicos para entrenar.

### Fuera de Alcance

* Asesoría o clases con entrenadores en vivo.

* Planes alimenticios, dietas o cálculo nutricional.


<hr>

## 4. Especificación de Datos del Dominio

Definición de las entidades principales que maneja la aplicación y sus atributos:

* **Información del Usuario:**
  - Nombre completo (texto)
  - Edad (número entero)
  - Nivel físico actual (opciones: Principiante, Intermedio, Avanzado)

* **Información del Ejercicio:**
  - Nombre del ejercicio (texto, ej: Flexiones, Sentadillas)
  - Tipo de actividad (texto, ej: Fuerza, Cardio)

* **Información de la Rutina:**
  - Nombre de la rutina (texto)
  - Nivel asignado (opciones: Principiante, Intermedio, Avanzado)
  - Lista ordenada de ejercicios incluidos

* **Registro de Sesión (Progreso):**
  - Fecha de entrenamiento (fecha)
  - Ejercicio realizado (texto)
  - Repeticiones completadas (número entero)
  - Tiempo de duración (número entero en minutos)

  <hr>

## 5. Casos de Uso y Criterios de Aceptación

### Caso 1: Inicio y ejecución de entrenamiento

* **Dado que** el usuario entra a la app y elige "Rutina nivel principiante",
* **Cuando** presiona "Iniciar rutina",
* **Entonces** la interfaz muestra la secuencia ordenada de ejercicios (Sentadillas, Flexiones, Cardio) y permite avanzar hasta concluir la sesión.

### Caso 2: Registro de progreso diario

* **Dado que** el usuario termina su rutina del día,
* **Cuando** ingresa los datos completados ("20 sentadillas, 15 flexiones, 10 min cardio") y confirma el guardado,
* **Entonces** el sistema almacena la sesión con la fecha actual y suma la rutina al total de días entrenados.


<hr>

## 6. Criterios de Calidad Técnicos

* **Facilidad de Uso:** Interfaz limpia e intuitiva que no requiere entrenamiento previo para el usuario.

* **Desempeño:** Iniciar una rutina de ejercicios toma menos de 3 segundos desde la selección.

* **Persistencia:** La información del usuario y su historial se conservan correctamente al recargar la página o cerrar el navegador.

* **Confiabilidad:** Exactitud en la acumulación de estadísticas diarias y registro de ejercicios sin perdida de datos.

<hr>

---

## 7. DISEÑO E INTERFAZ VISUAL

* **Colores:** Fondo verde claro (`#f0f4f2`), detalles en blanco y botones principales en verde esmeralda (`#059669`).
* **Estilo:** Interfaz limpia con texturas sutiles de cuadrícula y alto contraste para fácil lectura durante el ejercicio.
* **Componentes:**
  * Tarjetas de resumen para estadísticas (días entrenados y rutinas completadas).
  * Vista de entrenamiento con barra de progreso superior, temporizador y tarjeta central para el ejercicio actual.
  * Botones grandes de alta visibilidad para avanzar paso a paso.