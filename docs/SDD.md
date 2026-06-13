# SDD — Diseño de la solución: Módulo CAG

## 1. Problema
El proyecto base responde preguntas usando un RAG simple (knowledge.py sobre 
data/knowledge_base.json), pero no conserva contexto persistente del usuario. 
Cada pregunta es independiente: assistant.py nunca consulta contexto y 
context_used siempre queda vacío.

## 2. Decisión de diseño: persistencia del contexto

Opciones evaluadas:

| Opción | Pros | Contras | Decisión |
|---|---|---|---|
| A. Diccionario en memoria | Mínimo código | Se pierde al reiniciar: NO cumple "contexto persistente" | Descartada |
| B. Archivo JSON en data/ | Persistente, coherente con el estilo del proyecto (knowledge_base.json), sin dependencias, fácil de inspeccionar y testear | No escala a alta concurrencia (irrelevante para este alcance) | **ELEGIDA** |
| C. SQLite | Persistencia robusta, librería estándar | Complejidad innecesaria para el alcance del examen | Descartada |

**Justificación:** el enunciado exige contexto persistente; el JSON lo cumple 
manteniendo la coherencia arquitectónica del proyecto y minimizando riesgo. 
La persistencia queda encapsulada en ContextStore, por lo que una migración 
futura a SQLite no afectaría al resto del sistema.

## 3. Arquitectura: dónde encaja el CAG

Flujo actual (sin contexto):

    frontend → server.py → assistant.py → knowledge.py (RAG) → respuesta

Flujo nuevo (con capa CAG integrada):

    frontend → server.py → assistant.py
                              │
                              ├─ knowledge.py (RAG)          → snippets
                              ├─ context_store.py (NUEVO)    → contexto del usuario
                              └─ cag.py (NUEVO)              → respuesta aumentada
                                       │
                                       ▼
                            respuesta final + context_used

El RAG existente NO se modifica. El CAG es una capa intermedia que se aplica 
después de la recuperación documental.

## 4. Componentes

### 4.1 ContextStore (backend/context_store.py)
- `__init__(self, path="data/context_store.json")`: ruta configurable 
  (inyección de dependencia) para que las pruebas usen archivos temporales.
- `save(user_id, key, value)`: agrega {"key", "value"} a la lista del usuario 
  y escribe el JSON a disco. Retorna el ítem guardado (truthy).
- `list_for_user(user_id)`: retorna la lista de dicts del usuario, o [] si 
  no tiene contexto.

Formato de data/context_store.json:

    {
      "ana": [{"key": "preferred_style", "value": "explicaciones con analogias"}],
      "luis": [{"key": "audience", "value": "explicar como principiante"}]
    }

### 4.2 apply_context (backend/cag.py)
- `apply_context(user_id, question, base_answer, context_items)`
- Si context_items está vacío: retorna base_answer sin cambios.
- Si hay contexto: anexa a la respuesta una nota con los valores del contexto, 
  p. ej. "(Adaptado al contexto del usuario: explicar como principiante)". 
  Esto garantiza que el valor del contexto aparezca en el answer, como exige 
  el contrato de validación.

### 4.3 Integración en assistant.py
- answer_question() consulta context_store.list_for_user(user_id), pasa los 
  ítems a apply_context() y rellena "context_used" con las keys utilizadas.

### 4.4 server.py
- Las rutas POST/GET /api/context ya existen y delegan en ContextStore; 
  se verificará durante la implementación si requieren ajustes mínimos.

## 5. Contrato a cumplir (de tests/validation/test_cag_contract.py)
- POST /api/context → 201, body con "saved" truthy
- GET /api/context?user_id=X → 200, body con "user_id" y "context" (lista de dicts)
- POST /api/ask → 200, "answer" contiene el value del contexto, 
  "context_used" contiene las keys

## 6. Estrategia de pruebas (TDD)
1. Pruebas unitarias propias en tests/unit/ para ContextStore 
   (guardar, recuperar, aislamiento entre usuarios, persistencia entre 
   instancias) y para apply_context (con y sin contexto).
2. Ciclo rojo → verde por función, con commits separados.
3. Las pruebas de validación del profesor actúan como pruebas de integración 
   finales (./test.sh).