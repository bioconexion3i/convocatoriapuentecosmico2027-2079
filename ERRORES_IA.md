# Registro de Errores y Alucinaciones de Nodos IA

**Protocolo**: BioConexion3i v1.0.0  
**Directiva**: B.8 - Manejo de Errores y "Alucinaciones"  
**Propósito**: Documentar casos de respuestas falsas, engañosas o no trazables de nodos IA para mejorar prompts, filtros y criterios de validación humana.

---

## Estructura de Registro

Cada caso debe incluir:

1. **ID del Caso**: Identificador único (formato: ERR-YYYY-MM-DD-XXX)
2. **Fecha**: Timestamp ISO 8601
3. **Nodo IA**: Modelo que generó el error (Claude, Perplexity, Gemini, etc.)
4. **Categoría**: Tipo de error
   - `ALUCINACION`: Invención de datos no existentes
   - `SESGO`: Presentación sesgada sin balance
   - `ERROR_LOGICO`: Fallo en razonamiento o inferencia
   - `FUENTE_INVALIDA`: Cita incorrecta o fuente no verificable
   - `PERFILAMIENTO`: Cambio de postura sin evidencia nueva
5. **Contexto**: Tarea o consulta en curso
6. **Prompt Utilizado**: Instrucción completa enviada al modelo
7. **Respuesta Problemática**: Output erróneo (citado literalmente)
8. **Detección**: Cómo se identificó el error
9. **Corrección**: Información correcta con fuentes verificables
10. **Acción Tomada**: Ajustes en prompts o protocolos
11. **Responsable**: Humano que documentó el caso

---

## Casos Registrados

### Ejemplo: ERR-2025-12-29-001 (Plantilla)

**Fecha**: 2025-12-29T21:35:00-06:00  
**Nodo IA**: [Nombre del modelo]  
**Categoría**: ALUCINACION  
**Contexto**: [Descripción de la tarea]

**Prompt Utilizado**:
```
[Texto completo del prompt]
```

**Respuesta Problemática**:
```
[Output erróneo citado literalmente]
```

**Detección**:
- Método: [Verificación cruzada / Revisión de fuentes / Inconsistencia lógica]
- Herramienta: [Base de datos / Artículo científico / Consulta a experto]

**Corrección**:
[Información correcta con fuentes verificables]
- Fuente 1: [URL/DOI/Referencia]
- Fuente 2: [URL/DOI/Referencia]

**Acción Tomada**:
- [ ] Ajuste de prompt (especificar cambios)
- [ ] Adición de restricción explícita
- [ ] Implementación de verificación obligatoria
- [ ] Actualización de protocolo (indicar sección)

**Responsable**: [Nombre/ID del Tlacuilo o miembro del comité]

**Notas Adicionales**:
[Observaciones sobre patrones, frecuencia, o contexto relevante]

---

## ERR-2025-12-29-002: [Título descriptivo]

*[Próximo caso real a documentar aquí]*

---

## Estadísticas y Patrones

### Por Categoría
- ALUCINACION: 0 casos
- SESGO: 0 casos
- ERROR_LOGICO: 0 casos
- FUENTE_INVALIDA: 0 casos
- PERFILAMIENTO: 0 casos

### Por Nodo IA
- Claude: 0 casos
- Perplexity: 0 casos
- Gemini: 0 casos
- Otros: 0 casos

### Tendencias Identificadas
*A actualizar tras acumulación de casos suficientes (mínimo 10)*

---

## Protocolo de Documentación

### Cuándo Registrar

Se debe crear un registro cuando:
1. Una respuesta de IA contenga información factualmente incorrecta
2. Se detecte una cita o referencia inválida
3. El modelo cambie de postura sin justificación técnica
4. Se identifique sesgo significativo sin balance
5. Exista fallo lógico en razonamiento

### Cuándo NO Registrar

- Diferencias de interpretación legítimas
- Limitaciones conocidas del modelo (ej: conocimiento con fecha de corte)
- Errores tipográficos menores sin impacto factual
- Respuestas válidas pero suboptimales

### Proceso

1. **Detección**: Identificar error mediante verificación
2. **Documentación**: Completar plantilla de registro
3. **Verificación**: Validar corrección con al menos 2 fuentes independientes
4. **Análisis**: Determinar causa raíz y patrón
5. **Acción**: Implementar mejora en prompts o protocolo
6. **Registro en Git**: Commit con mensaje descriptivo

### Responsabilidades

**Tlacuilo/Comité**:
- Revisión semanal de nuevos casos
- Análisis mensual de patrones
- Actualización de estadísticas
- Propuesta de mejoras protocolares

**Contribuyentes**:
- Reportar errores detectados
- Documentar casos según plantilla
- Sugerir mejoras en prompts

---

## Directiva Operativa ante Duda Grave

> **"Detener narrativa, priorizar verificación."**

Si durante una interacción con un nodo IA surge duda grave sobre la veracidad de una respuesta:

1. **DETENER**: No continuar generando contenido basado en la respuesta dudosa
2. **MARCAR**: Señalar explícitamente la sección problemática
3. **VERIFICAR**: Buscar fuentes independientes y verificables
4. **DOCUMENTAR**: Si se confirma error, registrar caso completo
5. **CORREGIR**: Actualizar contenido con información verificada

---

## Integración con Protocolo

Este archivo implementa:
- **Directiva B.8**: Sistema de archivo de casos
- **Directiva B.2**: Verificabilidad de correcciones
- **Directiva B.7**: Rol del humano como filtro epistémico
- **Directiva B.4**: Documentación de cambios de postura

---

## Revisión y Actualización
**Frecuencia de revisión**: Mensual  
**Próxima revisión programada**: 2026-01-29  
**Responsable**: Tlacuilo + Comité BioConexion3i

**Criterios de actualización**:
- Cada nuevo caso documentado
- Actualización mensual de estadísticas
- Análisis trimestral de patrones
- Revisión anual sincronizada con CHANGELOG_Protocolo.md

---

**Versión del archivo**: 1.0.0  
**Fecha de creación**: 2025-12-29  
**Licencia**: CC BY-SA 4.0  
**Contacto**: bioconexion3i@gmail.com