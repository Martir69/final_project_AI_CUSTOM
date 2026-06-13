# Proyecto Examen Final - Módulo 3: Integración CAG

> **Estudiante:** Martir69
> **Repositorio (fork público):** https://github.com/Martir69/final_project_AI_CUSTOM
> **Tema:** Integración de un módulo CAG (Context-Augmented Generation) sobre un proyecto base con frontend, backend y RAG.

---

## Guía rápida para el evaluador

Todo el trabajo del examen está organizado en estos documentos:

| Requisito | Dónde encontrarlo |
|-----------|-------------------|
| Fork público | Etiqueta "forked from rortizs/..." en este repo |
| Diseño de la solución (SDD) | docs/SDD.md |
| Escenarios BDD (Gherkin) | docs/BDD.md |
| Scrum: backlog y 4 sprints | docs/scrum/ |
| Registro cronológico de IA | PROMPTS.md |
| Evidencias (capturas) | docs/evidencias/ |
| Pruebas propias del CAG | tests/unit/ |
| Pull Request revisado y merge | Pestaña Pull requests del repo |

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

Decisión de diseño clave (detalle en docs/SDD.md): la persistencia se hizo en archivo JSON por coherencia con el proyecto base y queda encapsulada en ContextStore. Durante la integración se detectó y corrigió por TDD un bug de sincronización entre instancias (ver PROMPTS.md, prompts 11 y 12).

## 3. Resultados de pruebas

| Suite | Resultado |
|-------|-----------|
| tests/base/ (proyecto base) | 3 pruebas OK |
| tests/unit/ (CAG, propias) | 18 pruebas OK |
| tests/validation/ (contrato final) | 3 pruebas OK |

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

Trabajo organizado con Scrum en 4 sprints:
- Sprint 1: Análisis y diseño (SDD, BDD)
- Sprint 2: Implementación TDD del módulo CAG (ContextStore, apply_context)
- Sprint 3: Integración en assistant.py y corrección de bug
- Sprint 4: Validación final, Pull Request y documentación

Detalle de cada sprint en docs/scrum/.

## 6. Estructura del repositorio

| Ruta | Contenido |
|------|-----------|
| backend/ | Servidor, RAG y módulo CAG |
| frontend/ | Interfaz web |
| data/ | Base de conocimiento y contexto persistido |
| tests/base/ | Pruebas base del proyecto |
| tests/unit/ | Pruebas unitarias propias del CAG |
| tests/validation/ | Pruebas de validación final |
| docs/ | Documentación (SDD, BDD), Scrum y evidencias |