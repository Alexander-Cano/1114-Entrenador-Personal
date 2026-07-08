# ENTRENAMIENTO PERSONAL




1. Descripción del Proyecto <br>


el Señor Alexander quiere mejorar su condición física sin salir de casa, pero no sabe qué ejercicios realizar ni cómo organizar sus entrenamientos. Actualmente intenta hacer ejercicio viendo videos en internet, pero no lleva un control de lo que hace, se desmotiva fácilmente y abandona las rutinas. <br>


El sistema debe permitir: <br>
• Mostrar rutinas de ejercicio organizadas por nivel (principiante, intermedio, avanzado) <br>
• Guiar al usuario paso a paso durante cada entrenamiento <br>
• Registrar los ejercicios realizados (repeticiones, tiempo) <br>
• Llevar control del progreso diario del usuario <br>
• Enviar recordatorios para mantener la constancia <br>




USUARIO (Entrenante) <br>



Realiza ejercicios en casa: selecciona rutinas, completa ejercicios y registra su progreso <br>





ENTRENADOR (Aplicación) <br>



Proporciona rutinas, guía los ejercicios y organiza el entrenamiento <br>





ADMINISTRADOR <br>



Gestiona los ejercicios, rutinas y contenido del sistema <br>






<br>
<br>
<br>




2. Requisitos Funcionales (¿Qué debe hacer?)<br>

El sistema DEBE permitir: <br>



• Registrar un usuario: nombre, edad, nivel físico <br>

• Mostrar rutinas según el nivel del usuario <br>

• Iniciar una rutina con lista de ejercicios paso a paso <br>

• Registrar cada ejercicio realizado: repeticiones y tiempo <br>

• Guardar el historial de entrenamientos del usuario <br>

• Mostrar resumen del progreso (días entrenados, rutinas completadas) <br>




<br>
<br>
<br>




3. Requisitos No Funcionales (¿Cómo debe funcionar?) <br>

• Fácil de usar: cualquier persona sin experiencia debe entenderla <br>

• Rápido: iniciar una rutina en menos de 3 segundos<br>

• Seguro: la información no se pierde al cerrar la aplicación <br>

• Confiable: los datos se guardan correctamente sin errores <br>

• Atractivo: interfaz visual que motive al usuario a entrenar <br>






<br>
<br>
<br>




4. Casos de Uso (Escenarios reales) <br>

Caso 1: Inicio de entrenamiento <br>

El usuario selecciona: “Rutina nivel principiante”. El sistema muestra una lista de ejercicios (sentadillas, flexiones, abdominales) y guía el entrenamiento paso a paso. <br>



Caso 2: Registro de progreso <br>

El usuario completa la rutina y registra: “20 sentadillas, 15 flexiones, 10 minutos de cardio”. El sistema guarda esta información como entrenamiento del día. <br>






<br>
<br>
<br>








5. Datos principales<br>
Qué información guardaremos: <br>


DATO         -     TIPO       -      EJEMPLO        <br>    
Usuario      -     Texto      -      "Laura Gomez" <br>
Edad         -     Numero     -      18             <br>
Nivel        -     Opciones   -      Intermedio     <br>
Ejercicio    -     Texto      -      Flexiones       <br>
Repeticiones -     Numero     -      15              <br>
Tiempo       -     Numero     -      20 Min           <br>




<br>
<br>
<br>




 




6. Criterios de Éxito (¿Cómo sabemos que funciona?) <br>
•  Se puede registrar un usuario sin errores <br>
•  Se puede iniciar y completar una rutina <br>
•  El sistema guarda correctamente el progreso <br>
•  Se pueden consultar entrenamientos anteriores <br>
•  La información se mantiene al cerrar y abrir la app <br>
•  El usuario puede usar la app durante varios días sin fallos <br>





<br>
<br>
<br>


7. Limitaciones (¿Qué NO hace?) <br>
• NO incluye entrenadores personales en tiempo real <br>
• NO genera planes de alimentación o dietas <br>
