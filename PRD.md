# ENTRENAMIENTO PERSONAL




1. Descripción del Proyecto


el Señor Alexander quiere mejorar su condición física sin salir de casa, pero no sabe qué ejercicios realizar ni cómo organizar sus entrenamientos. Actualmente intenta hacer ejercicio viendo videos en internet, pero no lleva un control de lo que hace, se desmotiva fácilmente y abandona las rutinas.


El sistema debe permitir:
• Mostrar rutinas de ejercicio organizadas por nivel (principiante, intermedio, avanzado)
• Guiar al usuario paso a paso durante cada entrenamiento
• Registrar los ejercicios realizados (repeticiones, tiempo)
• Llevar control del progreso diario del usuario
• Enviar recordatorios para mantener la constancia




USUARIO (Entrenante)


Realiza ejercicios en casa: selecciona rutinas, completa ejercicios y registra su progreso




ENTRENADOR (Aplicación)


Proporciona rutinas, guía los ejercicios y organiza el entrenamiento




ADMINISTRADOR


Gestiona los ejercicios, rutinas y contenido del sistema










2. Requisitos Funcionales (¿Qué debe hacer?)
El sistema DEBE permitir:


• Registrar un usuario: nombre, edad, nivel físico
• Mostrar rutinas según el nivel del usuario
• Iniciar una rutina con lista de ejercicios paso a paso
• Registrar cada ejercicio realizado: repeticiones y tiempo
• Guardar el historial de entrenamientos del usuario
• Mostrar resumen del progreso (días entrenados, rutinas completadas)








3. Requisitos No Funcionales (¿Cómo debe funcionar?)
• Fácil de usar: cualquier persona sin experiencia debe entenderla
• Rápido: iniciar una rutina en menos de 3 segundos
• Seguro: la información no se pierde al cerrar la aplicación
• Confiable: los datos se guardan correctamente sin errores
• Atractivo: interfaz visual que motive al usuario a entrenar










4. Casos de Uso (Escenarios reales)
Caso 1: Inicio de entrenamiento
El usuario selecciona: “Rutina nivel principiante”. El sistema muestra una lista de ejercicios (sentadillas, flexiones, abdominales) y guía el entrenamiento paso a paso.


Caso 2: Registro de progreso
El usuario completa la rutina y registra: “20 sentadillas, 15 flexiones, 10 minutos de cardio”. El sistema guarda esta información como entrenamiento del día.














5. Datos principales
Qué información guardaremos:


DATO            TIPO        EJEMPLO
Usuario         Texto       "Laura Gómez"
Edad            Número      30
Nivel           Opciones    Intermedio
Ejercicio       Texto       "Flexiones"
Repeticiones    Número      15
Tiempo          Número      20 min






 




6. Criterios de Éxito (¿Cómo sabemos que funciona?)
•  Se puede registrar un usuario sin errores
•  Se puede iniciar y completar una rutina
•  El sistema guarda correctamente el progreso
•  Se pueden consultar entrenamientos anteriores
•  La información se mantiene al cerrar y abrir la app
•  El usuario puede usar la app durante varios días sin fallos








7. Limitaciones (¿Qué NO hace?)
• NO incluye entrenadores personales en tiempo real
• NO genera planes de alimentación o dietas
