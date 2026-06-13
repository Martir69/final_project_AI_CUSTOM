# Sprint 3 — Integración del módulo CAG

**Objetivo del sprint:** Conectar ContextStore y apply_context en assistant.py 
y server.py para cumplir el contrato de validación, sin romper el RAG ni las 
pruebas existentes.

## Planificación
- [ ] Revisar cómo server.py maneja /api/context y conectar ContextStore
- [ ] Integrar list_for_user y apply_context en answer_question (assistant.py)
- [ ] Rellenar context_used con las keys del contexto utilizado
- [ ] Ejecutar pruebas de validación del profesor (./test.sh)
- [ ] Probar la aplicación completa (backend + frontend) manualmente
- [ ] Verificar que pruebas base y unitarias siguen en verde

## Evidencias
(se agregan durante el sprint)