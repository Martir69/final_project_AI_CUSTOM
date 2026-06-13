"""Módulo CAG: adapta respuestas del asistente al contexto del usuario."""


def apply_context(user_id, question, base_answer, context_items):
    """Retorna base_answer enriquecido con los valores del contexto del usuario."""
    if not context_items:
        return base_answer
    values = "; ".join(item["value"] for item in context_items)
    return f"{base_answer} (Adaptado al contexto del usuario: {values})"
