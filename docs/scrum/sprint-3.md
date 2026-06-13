# Sprint 3 — Integración del módulo CAG

**Objetivo del sprint:** Conectar ContextStore y apply_context en assistant.py 
y server.py para cumplir el contrato de validación, sin romper el RAG ni las 
pruebas existentes.

## Planificación
- [x] Revisar cómo server.py maneja /api/context y conectar ContextStore
- [x] Integrar list_for_user y apply_context en answer_question (assistant.py)
- [x] Rellenar context_used con las keys del contexto utilizado
- [x] Detectar y corregir bug de sincronización entre instancias (TDD)
- [x] Ejecutar pruebas de validación del profesor

## Hallazgo importante
Durante la integración se detectó que server.py y assistant.py creaban 
instancias separadas de ContextStore y list_for_user solo leía de memoria, 
por lo que una instancia no veía lo guardado por la otra. Se reprodujo el bug 
con una prueba (fase roja) y se corrigió haciendo que save y list_for_user 
relean del disco (fase verde).

## Cierre del sprint
Integración completa. Las 3 pruebas de validación del profesor pasan, junto 
con las 18 unitarias propias y las 3 base. El RAG no se modificó.

## Evidencias
![Validación final OK](../evidencias/09-validacion-ok.png)