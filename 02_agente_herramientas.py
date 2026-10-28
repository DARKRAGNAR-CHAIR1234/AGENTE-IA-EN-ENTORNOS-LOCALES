import os
import json
import ollama

# ==============================================================================
# PARTE A: LAS MANOS DEL AYUDANTE (Python abre el archivo real)
# ==============================================================================
def leer_archivo(nombre_archivo: str) -> str:
    """Abre un archivo de texto en la computadora y entrega su contenido."""
    print(f"\n>> [AYUDANTE PYTHON]: Abriendo físicamente el archivo '{nombre_archivo}'...")
    
    if not os.path.exists(nombre_archivo):
        return f"Error: El archivo '{nombre_archivo}' no existe."
    
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        contenido = f.read()
    
    print(">> [AYUDANTE PYTHON]: ¡Archivo leído con éxito! Pasando el texto a la IA...")
    return contenido

# Lista de funciones reales que el ayudante sabe ejecutar
HERRAMIENTAS = {
    "leer_archivo": leer_archivo
}

# ==============================================================================
# PARTE B: EL MENÚ DE HERRAMIENTAS (La tarjeta que le mostramos a la IA)
# ==============================================================================
menu_herramientas = [
    {
        "type": "function",
        "function": {
            "name": "leer_archivo",
            "description": "Lee el contenido de un archivo de texto en la computadora.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_archivo": {
                        "type": "string",
                        "description": "El nombre exacto del archivo, ej: 'documento_prueba.txt'",
                    }
                },
                "required": ["nombre_archivo"],
            },
        },
    }
]

# ==============================================================================
# PARTE C: LA CONVERSACIÓN Y EL TRABAJO EN EQUIPO
# ==============================================================================
def preguntar_al_agente(orden_del_jefe: str):
    mensajes = [
        {
            "role": "system",
            "content": (
                "Eres un asistente analista de documentos muy formal y ordenado. "
                "Regla de oro: Si te piden analizar un archivo, pide usar tu herramienta 'leer_archivo'. "
                "No inventes datos. Responde con viñetas claras en español."
            ),
        },
        {"role": "user", "content": orden_del_jefe},
    ]

    print("=" * 60)
    print(f"[TÚ LE DICES AL AGENTE]: {orden_del_jefe}")
    print("=" * 60)

    # 1. La IA recibe tu orden y revisa el menú de herramientas
    print("[EL GENIO / IA]: Pensando qué necesita para responder...")
    primera_respuesta = ollama.chat(
        model="qwen2.5:7b",
        messages=mensajes,
        tools=menu_herramientas,
    )

    mensaje_ia = primera_respuesta["message"]
    mensajes.append(mensaje_ia)

    # 2. ¿La IA levantó el teléfono para pedirle una acción a Python?
    if mensaje_ia.get("tool_calls"):
        for peticion in mensaje_ia["tool_calls"]:
            nombre_herramienta = peticion["function"]["name"]
            argumentos = peticion["function"]["arguments"]

            print(f"\n[EL GENIO LLAMA AL AYUDANTE]: 'Por favor ejecuta {nombre_herramienta} con {argumentos}'")

            # Python ejecuta la acción con sus "manos"
            funcion = HERRAMIENTAS[nombre_herramienta]
            resultado_real = funcion(**argumentos)

            # Python le dicta el contenido del archivo al genio usando el rol "tool"
            mensajes.append({
                "role": "tool",
                "content": str(resultado_real),
            })

        # 3. La IA lee el texto real y redacta la respuesta final
        print("\n[EL GENIO / IA]: Ya tengo el texto en mis manos. Redactando el informe...")
        respuesta_final = ollama.chat(
            model="qwen2.5:7b",
            messages=mensajes,
        )

        print("\n" + "=" * 60)
        print("[RESPUESTA FINAL DEL AGENTE]:")
        print("=" * 60)
        print(respuesta_final["message"]["content"])
    else:
        # Si la IA no necesitó herramientas, responde directamente
        print("\n[RESPUESTA DIRECTA]:")
        print(mensaje_ia["content"])

# ==============================================================================
# 4. EJECUTAMOS LA PRUEBA
# ==============================================================================
if __name__ == "__main__":
    preguntar_al_agente(
        "Por favor revisa el archivo 'documento_prueba.txt'. Extrae el número de expediente, "
        "la empresa involucrada, la penalización y las 3 acciones urgentes."
    )
