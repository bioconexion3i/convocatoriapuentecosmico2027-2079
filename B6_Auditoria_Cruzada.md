# B.6 Sistema de Auditoría Cruzada Multi-IA

**Protocolo**: BioConexion3i v1.0.0  
**Estado**: EN IMPLEMENTACIÓN (Bootstrap)

## Objetivo
Evitar el "colapso de contexto" o alucinaciones no detectadas al depender de un solo modelo de IA para decisiones críticas.

## 1. Disparadores: ¿Cuándo activar B.6?
La auditoría es OBLIGATORIA para:
1. **Cambios al Protocolo**: Modificaciones a directivas o manifiesto.
2. **Definición de Métricas**: Establecer KPIs de largo plazo (ej. metas 2079).
3. **Evaluación de Proyectos**: Aprobar paso de fase (ej. de Calibración a Prototipado).
4. **Validación de Hechos Críticos**: Datos que fundamentan inversiones o riesgos.

## 2. Flujo de Trabajo (Workflow)

1. **Prompt Maestro**: El Tlacuilo redacta un prompt neutral.
2. **Consulta Paralela**: Se envía a mínimo 2 modelos de familias distintas (ej. GPT-4, Claude 3, Gemini, Llama 3).
3. **Matriz de Convergencia**:
   - **Puntos de Acuerdo**: Se asumen como base sólida.
   - **Divergencias**: Se marcan para revisión humana profunda.
4. **Síntesis Humana**: El Tlacuilo decide basándose en la comparación.

## 3. Cláusula de Bootstrap (Fase Fundacional)
*Vigencia: Q1 2026*
En caso de no tener acceso automatizado a múltiples APIs:
- El Tlacuilo puede realizar la consulta manual en interfaces web distintas.
- Si solo hay un modelo disponible, se debe etiquetar la decisión como: `[PENDIENTE AUDITORÍA B.6]`.

**Versión**: 1.0.0
Última actualización: 2025-12-30
Licencia: CC BY-SA 4.0
Contacto: bioconexion3i@gmail.com
