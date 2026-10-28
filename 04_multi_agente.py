import os
import json
import ollama

# ==============================================================================
# 1. HERRAMIENTAS FÍSICAS (Python en tu equipo)
# ==============================================================================

def leer_expediente(nombre_archivo: str) -> str:
    """Lee el archivo del caso desde el disco duro."""
    print(f"\n>> [SISTEMA]: Agente 1 está leyendo físicamente '{nombre_archivo}'...")
    if not os.path.exists(nombre_archivo):
        return f"Error: El archivo '{nombre_archivo}' no existe."
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        return f.read()

def archivar_resolucion(nombre_archivo: str, contenido: str) -> str:
    """Guarda la resolución final auditada en el disco."""
    print(f"\n>> [SISTEMA]: Agente 2 está archivando físicamente '{nombre_archivo}'...")
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        return f"Éxito: Archivo '{nombre_archivo}' guardado correctamente."
    except Exception as e:
        return f"Error al guardar: {str(e)}"

# ==============================================================================
# 2. DEFINICIÓN DE HERRAMIENTAS POR ROL
# ==============================================================================

# El Agente 1 solo tiene permiso de LEER
herramientas_agente_1 = [
    {
        "type": "function",
        "function": {
            "name": "leer_expediente",
            "description": "Lee el contenido de un expediente o documento del sistema.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_archivo": {"type": "string", "description": "Nombre del archivo a revisar."}
                },
                "required": ["nombre_archivo"],
            },
        },
    }
]

# El Agente 2 solo tiene permiso de ARCHIVAR/GUARDAR
herramientas_agente_2 = [
    {
        "type": "function",
        "function": {
            "name": "archivar_resolucion",
            "description": "Guarda la resolución final redactada en un archivo de texto.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_archivo": {"type": "string", "description": "Nombre del archivo de salida."},
                    "contenido": {"type": "string", "description": "Texto formal de la resolución."},
                },
                "required": ["nombre_archivo", "contenido"],
            },
        },
    }
]

# ==============================================================================
# 3. EJECUCIÓN COORDINADA DE AMBOS AGENTES
# ==============================================================================

def flujo_de_trabajo_completo(archivo_origen: str, archivo_destino: str):
    print("=" * 70)
    print("INICIANDO FLUJO DE TRABAJO MULTI-AGENTE")
    print("=" * 70)

    # --------------------------------------------------------------------------
    # FASE 1: AGENTE 1 (INVESTIGADOR / EXTRACTOR)
    # --------------------------------------------------------------------------
    print("\n>>> FASE 1: AGENTE EXTRACTOR ENTRANDO EN ACCIÓN...")
    
    mensajes_agente_1 = [
        {
            "role": "system",
            "content": (
                "Eres el Agente Investigador. Tu trabajo es leer expedientes y extraer "
                "únicamente los datos duros: número de expediente, empresa, días de retraso, "
                "monto y cláusulas de penalización. No tomes decisiones, solo extrae los hechos."
            ),
        },
        {
            "role": "user",
            "content": f"Revisa el expediente en '{archivo_origen}' y entrega un informe con los datos clave.",
        },
    ]

    # Agente 1 solicita la lectura del archivo
    respuesta_1 = ollama.chat(
        model="qwen2.5:7b",
        messages=mensajes_agente_1,
        tools=herramientas_agente_1,
    )
    mensajes_agente_1.append(respuesta_1["message"])

    # Ejecutamos la herramienta física para el Agente 1
    if respuesta_1["message"].get("tool_calls"):
        for llamada in respuesta_1["message"]["tool_calls"]:
            if llamada["function"]["name"] == "leer_expediente":
                args = llamada["function"]["arguments"]
                texto_leido = leer_expediente(**args)
                mensajes_agente_1.append({"role": "tool", "content": texto_leido})

        # Agente 1 genera su informe con los datos ya leídos
        informe_agente_1 = ollama.chat(
            model="qwen2.5:7b",
            messages=mensajes_agente_1,
        )["message"]["content"]
    else:
        informe_agente_1 = respuesta_1["message"]["content"]

    print("\n[RESULTADO DEL AGENTE 1 - DATOS EXTRAÍDOS]:")
    print(informe_agente_1)

    # --------------------------------------------------------------------------
    # FASE 2: AGENTE 2 (AUDITOR / RESOLUTIVO)
    # --------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print(">>> FASE 2: AGENTE AUDITOR RECIBE LOS DATOS Y DICTAMINA...")
    print("=" * 70)

    mensajes_agente_2 = [
        {
            "role": "system",
            "content": (
                "Eres el Agente Auditor y Dictaminador. Recibes un reporte de hechos "
                "preparado por el Investigador. Tu trabajo es aplicar la regla de negocio: "
                "calcular la penalización exacta del 1.5% diario sobre el monto por los días "
                "de retraso aplicables, redactar un dictamen formal y guardarlo en disco."
            ),
        },
        {
            "role": "user",
            "content": (
                f"A continuación tienes los hechos encontrados por el Investigador:\n\n"
                f"{informe_agente_1}\n\n"
                f"Redacta el dictamen de sanción y guárdalo en '{archivo_destino}'."
            ),
        },
    ]

    respuesta_2 = ollama.chat(
        model="qwen2.5:7b",
        messages=mensajes_agente_2,
        tools=herramientas_agente_2,
    )
    mensajes_agente_2.append(respuesta_2["message"])

    if respuesta_2["message"].get("tool_calls"):
        for llamada in respuesta_2["message"]["tool_calls"]:
            if llamada["function"]["name"] == "archivar_resolucion":
                args = llamada["function"]["arguments"]
                resultado_guardado = archivar_resolucion(**args)
                mensajes_agente_2.append({"role": "tool", "content": resultado_guardado})

        # Cierre final del Agente 2
        conclusion_final = ollama.chat(
            model="qwen2.5:7b",
            messages=mensajes_agente_2,
        )["message"]["content"]
    else:
        conclusion_final = respuesta_2["message"]["content"]

    print("\n[RESOLUCIÓN FINAL DEL AGENTE 2]:")
    print(conclusion_final)

if __name__ == "__main__":
    flujo_de_trabajo_completo("documento_prueba.txt", "dictamen_final_auditado.txt")
