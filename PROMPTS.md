# PROMPTS.md  Registro cronológico de uso de IA

## Prompt 1 
**Objetivo:** Planificar el examen y entender el flujo de fork/clone/PR en GitHub
**Herramienta:** Claude (chat)
**Prompt usado:** Compartí el enunciado del examen y pedí un plan paso a paso  con 4 sprints, evidencias y manejo de GitHub Desktop
**Respuesta recibida:** Plan de 4 sprints (análisis/diseño, TDD del módulo CAG, 
integración, cierre), estructura de carpetas de documentación y flujo correcto 
fork → clone → rama → PR interno → merge
**Decisión humana:** Adopté el plan de 4 sprints y la estructura docs/. Decidí 
usar GitHub Desktop en lugar de la terminal por familiaridad
**Cambios realizados:** Fork del repo base, clone local, creación de estructura 
de documentación (docs/, PROMPTS.md)
**Verificación:** Fork visible en mi cuenta con etiqueta "forked from", repo clonado y abierto en VS  Code


## Prompt  2 
**Objetivo:** Ejecutar las pruebas base del proyecto en Windows (instrucción 3)
**Herramienta:** Claude
**Prompt usado:** Compartí el contenido de run_base_tests.sh y el error 
"Python was not found" de PowerShell
**Respuesta recibida:** El script usa unittest discover sobre tests/base; el error 
era por el alias de Microsoft Store. Propuso usar el lanzador `py` como equivalente
**Decisión humana:** Usé la opción del lanzador `py` por ser la más simple, 
en lugar de cambiar de terminal o modificar alias del sistema
**Cambios realizados:** Ninguno en código; evidencia 03-pruebas-base.png agregada
**Verificación:** py -m unittest discover -s tests/base → Ran 3 tests, OK

## Prompt 3 
**Objetivo:** Entender la arquitectura actual del proyecto y dónde está la lógica RAG (análisis de solo lectura, sin modificar archivos)
**Herramienta:** Claude Code (VS Code)
**Prompt usado:** "Estoy haciendo un proyecto donde debo integrar un módulo CAG. Antes de diseñar nada necesito entender el código existente. NO modifiques ni crees ningún archivo. Lee la carpeta backend/ y explícame: qué hace cada archivo, cómo fluye una pregunta del usuario desde el frontend hasta la respuesta, dónde está la lógica RAG, y si el sistema guarda contexto del usuario entre preguntas"
**Respuesta recibida:** El backend tiene 5 archivos: server.py (HTTP, rutas /api/ask y /api/context), assistant.py (orquestador), knowledge.py (RAG básico por coincidencia de palabras sobre data/knowledge_base.json) y dos esqueletos sin implementar: context_store.py (save y list_for_user lanzan NotImplementedError) y cag.py (apply_context devuelve la respuesta sin cambios). El contexto se pierde porque assistant.py nunca consulta el ContextStore ni llama a apply_context, y context_used siempre queda vacío
**Decisión humana:** Confirmé que la capa intermedia no se inventa desde cero: el proyecto ya define los esqueletos context_store.py y cag.py. Mi trabajo es implementarlos y conectarlos en assistant.py sin modificar el RAG existente, para mantener la claridad arquitectónica que pide el examen
**Cambios realizados:** Ninguno (análisis de solo lectura)
**Verificación:** Abrí personalmente context_store.py y cag.py y confirmé que save() y list_for_user() lanzan NotImplementedError y que apply_context() solo hace return base_answer, tal como describió la IA


## Prompt 4 
**Objetivo:** Extraer el checklist exacto de requisitos de las pruebas de validación final (tests/validation/)
**Herramienta:** Claude Code (VS Code)
**Prompt usado:** "Ahora lee la carpeta tests/validation/ SIN modificar nada y dime exactamente qué esperan esas pruebas: qué módulos, funciones y endpoints deben existir, qué comportamiento verifican y qué nombres exactos usan. Lista los requisitos como checklist"
**Respuesta recibida:** Hay un solo archivo (test_cag_contract.py) con 3 tests: (1) POST /api/context debe responder 201 con campo "saved" truthy; (2) GET /api/context?user_id=ana debe responder 200 con "user_id" y "context" como lista de dicts {"key","value"}; (3) tras guardar contexto, POST /api/ask debe responder 200, el "answer" debe contener el valor del contexto (ej. "principiante") y "context_used" debe contener la key (ej. "audience"). Las rutas, códigos HTTP y campos JSON son contrato fijo que no puedo cambiar
**Decisión humana:** Adopté ese checklist como contrato de implementación y como base de los escenarios BDD (docs/BDD.md). Identifiqué que el test 3 exige que apply_context() incorpore literalmente el valor del contexto dentro de la respuesta
**Cambios realizados:** Ninguno (análisis de solo lectura)
**Verificación:** Leí yo mismo tests/validation/test_cag_contract.py y confirmé los 3 tests, los códigos HTTP (201/200) y los campos exactos (saved, user_id, context, answer, context_used)


## Prompt 5
**Objetivo:** Tomar la decisión de diseño sobre la persistencia del contexto
**Herramienta:** Claude (chat)
**Prompt usado:** Pedí comparar opciones de persistencia para el ContextStore (diccionario en memoria, archivo JSON, SQLite) considerando que el enunciado exige contexto persistente
**Respuesta recibida:** Comparativa de 3 opciones: memoria no cumple "persistente" (se pierde al reiniciar); JSON es coherente con el estilo del proyecto (knowledge_base.json ya es JSON plano) y no agrega dependencias; SQLite es robusto pero complejidad innecesaria para el alcance del proyecto
**Decisión humana:** Elegí archivo JSON en data/ porque cumple el requisito de persistencia, mantiene la coherencia arquitectónica del proyecto base y deja la persistencia encapsulada en ContextStore (migrable a SQLite sin afectar al resto del sistema). Además decidí que el constructor de ContextStore reciba la ruta del archivo como parámetro, para que las pruebas unitarias usen archivos temporales y no toquen data/
**Cambios realizados:** docs/SDD.md con la decisión justificada, docs/BDD.md con escenarios Gherkin, cierre de Sprint 1 en docs/scrum/sprint-1.md
**Verificación:** Revisé que el diseño del SDD cubre punto por punto el contrato de tests/validation/test_cag_contract.py (rutas, códigos HTTP y campos JSON)

## Prompt 6 — 2026-06-12
**Objetivo:** Diagnosticar por qué PROMPTS.md no aparecía en GitHub
**Herramienta:** Claude (chat)
**Prompt usado:** Reporté que VS Code mostraba el archivo pero GitHub Desktop no detectaba cambios y la web no lo mostraba; compartí el contenido de .gitignore
**Respuesta recibida:** El .gitignore del proyecto base incluye la línea PROMPTS.md (pensada para los archivos del instructor), por lo que git ignoraba mi archivo
**Decisión humana:** Eliminé únicamente esa línea del .gitignore en mi fork, porque el examen exige PROMPTS.md dentro del repositorio; conservé el resto de exclusiones del instructor
**Cambios realizados:** .gitignore modificado; PROMPTS.md ahora versionado
**Verificación:** PROMPTS.md visible en la raíz del repo en GitHub tras el push