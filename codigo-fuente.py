"""
Sistema Multi-Agente Documental Autónomo
Ejecución local mediante Ollama y Function Calling.
Autor: Antonio
Plataforma: Linux x86_64 / CachyOS (CUDA Runtime)
"""

import os
import json
import ollama

# ==============================================================================
# 1. CAPA DE INTERACCIÓN FÍSICA (HERRAMIENTAS DEL SISTEMA)
# ==============================================================================

def leer_expediente(nombre_archivo: str) -> str:
    """Lee el texto plano de un documento existente en el almacenamiento local."""
    if not os.path.exists(nombre_archivo):
        return f"Error de I/O: El archivo '{nombre_archivo}' no existe."
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Excepción al leer: {str(e)}"

def archivar_resolucion(nombre_archivo: str, contenido: str) -> str:
    """Crea y almacena el dictamen formal resultante en el disco local."""
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        return f"Éxito: Documento persistido como '{nombre_archivo}'."
    except Exception as e:
        return f"Excepción al escribir: {str(e)}"

# ==============================================================================
# 2. ESQUEMAS DE HERRAMIENTAS SEGREGADOS POR ROL
# ==============================================================================

TOOLS_EXTRACTOR = [
    {
        "type": "function",
        "function": {
            "name": "leer_expediente",
            "description": "Lee el contenido íntegro de un expediente local para extraer datos fácticos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_archivo": {
                        "type": "string",
                        "description": "Ruta o nombre del archivo a procesar."
                    }
                },
                "required": ["nombre_archivo"],
            },
        },
    }
]

TOOLS_AUDITOR = [
    {
        "type": "function",
        "function": {
            "name": "archivar_resolucion",
            "description": "Guarda el dictamen emitido dentro de un archivo de texto en disco.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_archivo": {
                        "type": "string",
                        "description": "Nombre del archivo de destino (ej: dictamen.txt)."
                    },
                    "contenido": {
                        "type": "string",
                        "description": "Cuerpo íntegro de la resolución redactada."
                    },
                },
                "required": ["nombre_archivo", "contenido"],
            },
        },
    }
]

# ==============================================================================
# 3. PIPELINE DE EJECUCIÓN MULTI-AGENTE
# ==============================================================================

def ejecutar_pipeline(archivo_entrada: str, archivo_salida: str, modelo: str = "qwen2.5:7b"):
    # ---------------------------------------------------------
    # AGENTE 1: INVESTIGADOR / EXTRACTOR DE HECHOS
    # ---------------------------------------------------------
    mensajes_agente_1 = [
        {
            "role": "system",
            "content": (
                "Eres un agente técnico extractor de datos. "
                "Tu único rol es leer expedientes y reportar los hechos duros: "
                "identificador, partes involucradas, fechas, plazos y montos. "
                "No interpretes ni tomes decisiones de sanción."
            ),
        },
        {
            "role": "user",
            "content": f"Extrae los datos críticos contenidos en '{archivo_entrada}'.",
        },
    ]

    r1 = ollama.chat(model=modelo, messages=mensajes_agente_1, tools=TOOLS_EXTRACTOR)
    mensajes_agente_1.append(r1["message"])

    if r1["message"].get("tool_calls"):
        for call in r1["message"]["tool_calls"]:
            if call["function"]["name"] == "leer_expediente":
                datos = leer_expediente(**call["function"]["arguments"])
                mensajes_agente_1.append({"role": "tool", "content": datos})
        
        informe_extractor = ollama.chat(model=modelo, messages=mensajes_agente_1)["message"]["content"]
    else:
        informe_extractor = r1["message"]["content"]

    # ---------------------------------------------------------
    # AGENTE 2: AUDITOR Y DICTAMINADOR
    # ---------------------------------------------------------
    mensajes_agente_2 = [
        {
            "role": "system",
            "content": (
                "Eres un auditor jurídico de cumplimiento contractual. "
                "Recibes una relación de hechos probados. Aplica rigurosamente las reglas "
                "de penalización, redacta la resolución formal y persístela en almacenamiento."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Hechos establecidos:\n{informe_extractor}\n\n"
                f"Genera el dictamen administrativo formal y archívalo en '{archivo_salida}'."
            ),
        },
    ]

    r2 = ollama.chat(model=modelo, messages=mensajes_agente_2, tools=TOOLS_AUDITOR)
    mensajes_agente_2.append(r2["message"])

    if r2["message"].get("tool_calls"):
        for call in r2["message"]["tool_calls"]:
            if call["function"]["name"] == "archivar_resolucion":
                resultado = archivar_resolucion(**call["function"]["arguments"])
                mensajes_agente_2.append({"role": "tool", "content": resultado})
        
        ollama.chat(model=modelo, messages=mensajes_agente_2)

    return archivo_salida

if __name__ == "__main__":
    archivo_generado = ejecutar_pipeline("documento_prueba.txt", "dictamen_final_auditado.txt")
    print(f"[PIPELINE COMPLETADO]: Resolución guardada en '{archivo_generado}'.")
