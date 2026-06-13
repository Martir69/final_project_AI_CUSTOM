# BDD — Escenarios de comportamiento del módulo CAG

Escenarios escritos en Gherkin, derivados del enunciado del examen y del 
contrato de validación (tests/validation/test_cag_contract.py).

## Característica: Persistencia de contexto del usuario

```gherkin
Característica: Guardar contexto del usuario
  Como usuario del asistente
  Quiero que el sistema guarde mis preferencias y datos de contexto
  Para recibir respuestas adaptadas en consultas posteriores

  Escenario: Guardar un dato de contexto
    Dado que el backend está en ejecución
    Cuando envío POST /api/context con user_id "ana", key "preferred_style" 
      y value "explicaciones con analogias"
    Entonces la respuesta tiene código HTTP 201
    Y el cuerpo contiene el campo "saved" con valor verdadero

  Escenario: Recuperar el contexto de un usuario
    Dado que el usuario "ana" guardó la key "project" con value 
      "usa arquitectura monolitica moderna"
    Cuando consulto GET /api/context?user_id=ana
    Entonces la respuesta tiene código HTTP 200
    Y el campo "user_id" es "ana"
    Y el campo "context" es una lista que incluye 
      {"key": "project", "value": "usa arquitectura monolitica moderna"}

  Escenario: El contexto guardado influye en respuestas posteriores
    Dado que el usuario "luis" guardó la key "audience" con value 
      "explicar como principiante"
    Cuando envío POST /api/ask con user_id "luis" y question "Que es CAG?"
    Entonces la respuesta tiene código HTTP 200
    Y el campo "answer" contiene el texto "principiante"
    Y el campo "context_used" incluye "audience"
```

## Trazabilidad

| Escenario BDD | Test de validación | Módulo responsable |
|---|---|---|
| Guardar un dato de contexto | test_saves_context_for_user | context_store.py |
| Recuperar el contexto | test_retrieves_context_for_user | context_store.py + server.py |
| El contexto influye en respuestas | test_ask_uses_context_to_influence_later_response | cag.py + assistant.py |