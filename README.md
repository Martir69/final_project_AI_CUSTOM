# Proyecto Examen Final - Módulo 3: Integración CAG

> **Estudiante:** Martir69
> **Repositorio (fork público):** https://github.com/Martir69/final_project_AI_CUSTOM
> **Tema:** Integración de un módulo CAG (Context-Augmented Generation) sobre un proyecto base con frontend, backend y RAG.

---

## Índice de la documentación (informe)

### Diseño y comportamiento
- [Documento de diseño (SDD)](docs/SDD.md) — arquitectura y decisiones
- [Escenarios BDD (Gherkin)](docs/BDD.md) — comportamiento esperado

### Gestión Scrum
- [Product Backlog](docs/scrum/backlog.md)
- [Sprint 1 — Análisis y diseño](docs/scrum/sprint-1.md)
- [Sprint 2 — Implementación TDD](docs/scrum/sprint-2.md)
- [Sprint 3 — Integración](docs/scrum/sprint-3.md)
- [Sprint 4 — Validación, PR y cierre](docs/scrum/sprint-4.md)

### Uso de IA
- [PROMPTS.md — registro cronológico](PROMPTS.md)

### Evidencias (capturas)
- [Carpeta completa de evidencias](docs/evidencias/)
- [01 — Fork creado](docs/evidencias/01-fork-creado.png)
- [02 — Clone del fork](docs/evidencias/02-clone.png)
- [03 — Pruebas base OK](docs/evidencias/03-pruebas-base.png)
- [05 — TDD ContextStore (fase roja)](docs/evidencias/05-tdd-context-store-rojo.png)
- [06 — TDD ContextStore (fase verde)](docs/evidencias/06-tdd-context-store-verde.png)
- [07 — TDD apply_context (fase roja)](docs/evidencias/07-tdd-cag-rojo.png)
- [08 — TDD apply_context (fase verde)](docs/evidencias/08-tdd-cag-verde.png)
- [09 — Validación final OK](docs/evidencias/09-validacion-ok.png)
- [11 — App funcionando con contexto](docs/evidencias/11-app-funcionando.png)
- [12 — App sin contexto (comparativa)](docs/evidencias/12-app-sin-contexto.png)
---

## 1. Problema y solución

El proyecto base respondía con un RAG simple (coincidencia de palabras sobre data/knowledge_base.json) pero no conservaba contexto del usuario: cada pregunta era independiente y context_used siempre quedaba vacío.

Se integró la capa CAG, que guarda, recupera y utiliza contexto persistente:
- ContextStore (backend/context_store.py): persiste el contexto de cada usuario en data/context_store.json.
- apply_context (backend/cag.py): inyecta el contexto del usuario en la respuesta base.
- Integración (backend/assistant.py): consulta el contexto y rellena context_used, sin modificar el RAG existente.

## 2. Arquitectura

    frontend -> server.py -> assistant.py
                               |- knowledge.py (RAG, sin cambios) -> snippets
                               |- context_store.py (CAG) -> contexto del usuario
                               |- cag.py (CAG) -> respuesta aumentada + context_used

Decisión de diseño clave (detalle en [docs/SDD.md](docs/SDD.md)): la persistencia se hizo en archivo JSON por coherencia con el proyecto base y queda encapsulada en ContextStore. Durante la integración se detectó y corrigió por TDD un bug de sincronización entre instancias (ver [PROMPTS.md](PROMPTS.md), prompts 11 y 12).

## 3. Resultados de pruebas

| Suite | Resultado |
|-------|-----------|
| tests/base/ (proyecto base) | 3 pruebas OK |
| tests/unit/ (CAG, propias) | 18 pruebas OK |
| tests/validation/ (contrato final) | 3 pruebas OK |

Evidencia: [09-validacion-ok.png](docs/evidencias/09-validacion-ok.png)

## 4. Cómo ejecutar

Requisitos: Python 3. En Windows usar py en lugar de python3.

Pruebas:

    $env:PYTHONPATH="."
    py -m unittest discover -s tests/base -p "test_*.py"
    py -m unittest discover -s tests/unit -p "test_*.py"
    py -m unittest discover -s tests/validation -p "test_*.py"

Backend:

    $env:PYTHONPATH="."
    py -m backend.server

Disponible en http://127.0.0.1:8000. El frontend se abre con frontend/index.html.

## 5. Metodología

Trabajo organizado con Scrum en 4 sprints (TDD, ciclos rojo->verde):
- Sprint 1: Análisis y diseño (SDD, BDD)
- Sprint 2: Implementación TDD del módulo CAG (ContextStore, apply_context)
- Sprint 3: Integración en assistant.py y corrección de bug
- Sprint 4: Validación final, Pull Request y documentación

## 6. Estructura del repositorio

| Ruta | Contenido |
|------|-----------|
| backend/ | Servidor, RAG y módulo CAG |
| frontend/ | Interfaz web |
| data/ | Base de conocimiento (el contexto se genera en runtime) |
| tests/base/ | Pruebas base del proyecto |
| tests/unit/ | Pruebas unitarias propias del CAG |
| tests/validation/ | Pruebas de validación final |
| docs/ | Documentación (SDD, BDD), Scrum y evidencias |