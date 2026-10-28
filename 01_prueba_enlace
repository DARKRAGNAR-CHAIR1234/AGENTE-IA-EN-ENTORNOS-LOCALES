import ollama

# Ahora definimos explícitamente el rol "system" antes del mensaje del usuario
mensajes = [
    {
        "role": "system",
        "content": (
            "Eres un agente técnico documental. "
            "Regla estricta: Responde única y exclusivamente en español claro y conciso. "
            "No utilices ningún carácter en otro idioma."
        ),
    },
    {
        "role": "user",
        "content": "Explica en una sola oración qué es un agente de IA y para qué sirve en una oficina.",
    },
]

print("[Sistema]: Enviando solicitud a Ollama con rol System definido...")

respuesta = ollama.chat(
    model="qwen2.5:7b",
    messages=mensajes,
)

print("\n[Respuesta del Modelo]:")
print(respuesta["message"]["content"])
