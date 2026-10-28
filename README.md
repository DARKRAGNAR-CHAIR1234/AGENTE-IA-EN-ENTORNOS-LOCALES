# multiagentes IA en entornos locales.
Este documento registra el diseño, despliegue y validación empírica de un sistema agéntico inteligente ejecutado íntegramente de manera local, sin dependencias de servicios en la nube ni fuga de datos confidenciales


El proyecto abarca desde la configuración del motor de inferencia en hardware dedicado hasta la orquestación de un flujo multi-agente para procesamiento y dictaminación documental.

## 1. Arquitectura de Hardware y Entorno de Ejecución
Para garantizar privacidad absoluta, baja latencia y reproducibilidad operativa en tareas de procesamiento de texto estructurado, el entorno se desplegó sobre la siguiente plataforma:

<img width="792" height="623" alt="image" src="https://github.com/user-attachments/assets/9f6b482d-f3d0-4f98-a3b7-93de0e42daf4" />


## 2. Marco Conceptual: De Modelos Aislados a Sistemas Agénticos
Un Modelo de Lenguaje Grande (LLM) convencional opera como un sistema probabilístico estático: predice la secuencia textual más probable a partir de un contexto dado, pero carece de interacción directa con el sistema de archivos del equipo.

<img width="792" height="623" alt="image" src="https://github.com/user-attachments/assets/cc09f917-719d-4849-8e97-2c22e72e3369" />

El enfoque agéntico implementado se sustenta en tres principios:

Separación de Responsabilidades: El modelo actúa exclusivamente como planificador lógico ("el cerebro"), mientras que el intérprete de Python actúa como efector físico ("las manos").

Definición Estricta de Herramientas (Tool Schemas): Las funciones disponibles se describen mediante esquemas JSON tipificados (name, description, properties, required), permitiendo que el modelo determine de forma determinista qué parámetros enviar.

Control por Roles: Se establece una jerarquía de cuatro roles de comunicación:

"system": Fija las restricciones deontológicas, el idioma operativo y las directivas de comportamiento.

"user": Representa la instrucción o demanda del operador.

"assistant": Registra las deducciones intermedias emitidas por el modelo.

"tool": Devuelve al contexto del modelo la información cruda obtenida físicamente por el script.

## 3. Hitos de Implementación y Validación TécnicaHito
  
  Hito 1: Despliegue del Backend Local y Verificación CUDASe instaló ollama-cuda para garantizar el uso exclusivo de la memoria gráfica dedicada. 
  
  Al descargar y montar qwen2.5:7b, se validó su estado en ejecución mediante el comando ollama ps. Resultado técnico: El modelo fue cargado al 100% dentro de la VRAM (4.8 GB), dejando un remanente libre para el sistema de ventanas y evitando el cuello de botella de transferencia hacia la RAM del sistema.   

  Hito 2: Comunicación Inter-Procesos y Métrica de RendimientoSe desarrolló un puente cliente-servidor mediante un entorno virtual aislado en Python. 
  
  Se configuró una solicitud estructurada para evaluar la velocidad de procesamiento de tensores.   Resultado métrico:Tokens de entrada evaluados: 54.   Tokens de salida generados: 99.   Tiempo total de inferencia: 4.62 segundos.   Velocidad neta de generación: 21.42 tokens/segundo.   Hallazgo: Durante este hito se documentó que la omisión del mensaje con rol "system" provoca deriva idiomática en modelos entrenados sobre corpus multilingües (como Qwen). La inclusión explícita de directivas "system" normalizó el 100% de las respuestas en español técnico formal.  

  Hito 3: Implementación de Tool Calling Unidireccional (Lectura de Expedientes)
Se programó una herramienta de lectura física en disco (leer_archivo) vinculada al esquema JSON del agente. Se le proporcionó al sistema un documento crudo no indexado (documento_prueba.txt) correspondiente al expediente legal EXP-2026-884.

Comportamiento observado:

- Al recibir la orden de análisis, el modelo reconoció no poseer los datos en su memoria previa.   
- Emitió una solicitud estructurada de llamada a función: leer_archivo(nombre_archivo='documento_prueba.txt').   
- El script de Python abrió el archivo, extrajo el texto plano y lo inyectó de vuelta mediante el rol "tool".
- El agente sintetizó los datos duros: partes intervinientes, causas del retraso y acciones requeridas.

Hito 4: Persistencia y Ciclo Autónomo de Autocorrección
Se incorporó una segunda función física: guardar_archivo, permitiendo al agente generar informes y persistirlos en disco. Se diseñó un bucle de ejecución secuencial (for ciclo in range(4)) para permitir tareas de múltiples pasos.

Hallazgo técnico (Capacidad de Autocorrección): 
Durante la prueba empírica, el modelo intentó emitir una respuesta anticipada en el Ciclo 1; no obstante, al contar con un ciclo agéntico cerrado, ejecutó la lectura en el Ciclo 2 y procedió a sobrescribir el archivo en el Ciclo 3, alcanzando una precisión aritmética del 100% ($350,000 \times 0.015 \times 7 = \$36,750\text{ MXN}$) e identificando el expediente legítimo EXP-2026-884







