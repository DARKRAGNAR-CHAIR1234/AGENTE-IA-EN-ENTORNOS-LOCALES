import os
import json
import ollama

# ==============================================================================
# PARTE A: LAS HERRAMIENTAS FÍSICAS DE PYTHON (Leer y Escribir)
# ==============================================================================

def leer_archivo(nombre_archivo: str) -> str:
    """Abre y lee el contenido de un archivo de texto en la computadora."""
    print(f"\n>> [AYUDANTE PYTHON]: Leyendo físicamente '{nombre_archivo}'...")
    if not os.path.exists(nombre_archivo):
        return f"Error: El archivo '{nombre_archivo}' no existe."
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        contenido = f.read()
    print(">> [AYUDANTE PYTHON]: Archivo leído correctamente.")
    return contenido

def guardar_archivo(nombre_archivo: str, contenido: str) -> str:
    """Crea y guarda un nuevo archivo en la computadora con el texto proporcionado."""
    print(f"\n>> [AYUDANTE PYTHON]: Escribiendo y guardando el archivo '{nombre_archivo}'...")
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f">> [AYUDANTE PYTHON]: ¡Archivo '{nombre_archivo}' guardado con éxito en el disco!")
        return f"Éxito: El archivo '{nombre_archivo}' fue creado y guardado satisfactoriamente."
    except Exception as e:
        return f"Error al intentar guardar el archivo: {str(e)}"

# Caja de herramientas disponibles
CAJA_HERRAMIENTAS = {
    "leer_archivo": leer_archivo,
    "guardar_archivo": guardar_archivo,
}

# ==============================================================================
# PARTE B: EL MENÚ CON DOS OPCIONES PARA EL GENIO
# ==============================================================================
menu_herramientas = [
    {
        "type": "function",
        "function": {
            "name": "leer_archivo",
            "description": "Lee el texto de un archivo existente en la computadora.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_archivo": {
                        "type": "string",
                        "description": "Nombre del archivo a consultar (ej: 'documento_prueba.txt').",
                    }
                },
                "required": ["nombre_archivo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "guardar_archivo",
            "description": "Guarda un informe, reporte o texto dentro de un archivo nuevo en la computadora.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_archivo": {
                        "type": "string",
                        "description": "El nombre con el que se guardará el nuevo archivo (ej: 'dictamen_final.txt').",
                    },
                    "contenido": {
                        "type": "string",
                        "description": "El texto completo que se va a escribir dentro del archivo.",
                    },
                },
                "required": ["nombre_archivo", "contenido"],
            },
        },
    },
]

# ==============================================================================
# PARTE C: EL BUCLE DE ACCIONES MÚLTIPLES
# ==============================================================================
def ejecutar_agente(orden_del_jefe: str):
    mensajes = [
        {
            "role": "system",
            "content": (
                "Eres un agente analista profesional y resolutivo. "
                "Tu trabajo es procesar información y generar resultados concretos. "
                "Reglas obligatorias:\n"
                "1. Si necesitas datos de un archivo, usa 'leer_archivo'.\n"
                "2. Si el usuario te pide guardar o generar un reporte en archivo, usa 'guardar_archivo'.\n"
                "3. Calcula con exactitud cualquier cifra económica o penalización.\n"
                "4. Responde en español formal y ordenado."
            ),
        },
        {"role": "user", "content": orden_del_jefe},
    ]

    print("=" * 70)
    print(f"[ORDEN DEL JEFE]: {orden_del_jefe}")
    print("=" * 70)

    # El ciclo puede requerir varios pasos; permitimos hasta 4 rondas de acción
    for ciclo in range(4):
        print(f"\n[CICLO {ciclo + 1} - EL GENIO]: Analizando la situación...")
        respuesta = ollama.chat(
            model="qwen2.5:7b",
            messages=mensajes,
            tools=menu_herramientas,
        )

        mensaje_ia = respuesta["message"]
        mensajes.append(mensaje_ia)

        # Si el genio no solicita herramientas, significa que terminó su trabajo
        if not mensaje_ia.get("tool_calls"):
            print("\n" + "=" * 70)
            print("[RESPUESTA FINAL DEL AGENTE]:")
            print("=" * 70)
            print(mensaje_ia["content"])
            break

        # Si el genio pidió usar una o más herramientas:
        for peticion in mensaje_ia["tool_calls"]:
            nombre_herramienta = peticion["function"]["name"]
            argumentos = peticion["function"]["arguments"]

            print(f"\n[EL GENIO SOLICITA ACCIÓN]: Usar '{nombre_herramienta}'")
            print(f"[DATOS ENVIADOS]: {argumentos}")

            # Python ejecuta la acción correspondiente
            if nombre_herramienta in CAJA_HERRAMIENTAS:
                funcion = CAJA_HERRAMIENTAS[nombre_herramienta]
                resultado_accion = funcion(**argumentos)
            else:
                resultado_accion = f"Error: La herramienta '{nombre_herramienta}' no existe."

            # Le pasamos el resultado a la IA para el siguiente paso del ciclo
            mensajes.append({
                "role": "tool",
                "content": str(resultado_accion),
            })

# ==============================================================================
# PARTE D: PRUEBA DE FLUJO COMPLETO
# ==============================================================================
if __name__ == "__main__":
    ejecutar_agente(
        "Por favor lee 'documento_prueba.txt'. Calcula la penalización de 7 días "
        "(1.5% diario sobre $350,000 MXN) y redacta un reporte formal con el número de "
        "expediente, el monto exacto de la multa y los siguientes pasos. "
        "Guarda ese reporte en un archivo llamado 'reporte_resolucion.txt'."
    )
