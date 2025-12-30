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
   - `VIOLACION_PROTOCOLO`: Incumplimiento de directivas establecidas
5. **Contexto**: Tarea o consulta en curso
6. **Prompt Utilizado**: Instrucción completa enviada al modelo
7. **Respuesta Problemática**: Output erróneo (citado literalmente)
8. **Detección**: Cómo se identificó el error
9. **Corrección**: Información correcta con fuentes verificables
10. **Acción Tomada**: Ajustes en prompts o protocolos
11. **Responsable**: Humano que documentó el caso

---

## Casos Registrados

### ERR-2025-12-30-001: Violación Directiva B.6 - Implementación sin Auditoría Cruzada

**Fecha**: 2025-12-30T10:06:00-06:00  
**Nodo IA**: Perplexity  
**Categoría**: VIOLACION_PROTOCOLO  

**Contexto**:  
Implementación de la infraestructura técnica del protocolo (Capa B: extensiones B.2, B.7, B.8, B.9).

**Prompt Utilizado**:
```
Usuario: "implementa capa b : extensiones BioConexion3i"
Usuario: "comienza con B.2"
Usuario: "si" [aprobación de creación de archivo]
```

**Respuesta Problemática**:
El nodo procedió a diseñar sistemas críticos (taxonomías, templates, métricas) solicitando únicamente la aprobación del usuario individual, omitiendo el requisito de Auditoría Cruzada (B.6) para decisiones de alto impacto.

**Detección**:
Cuestionamiento directo del Tlacuilo: *"si se necesita auditoría cruzada, por qué solo con mi autorización se están haciendo cambios?"*

**Análisis de Violación**:
La Directiva B.6 exige consultar ≥2 modelos para "decisiones de alto impacto". El diseño de la infraestructura de verdad del proyecto (cómo se verifican los hechos por 50 años) es una decisión de alto impacto.

**Acción Tomada**:
- Detención inmediata del proceso.
- Registro formal de esta violación.
- Creación del archivo `B6_Auditoria_Cruzada.md` para regular futuras implementaciones.
- Aplicación de "Cláusula Bootstrap": Se documenta la excepción para permitir la creación del sistema que regulará el proceso.

**Responsable**: Tlacuilo (Detección) / Perplexity (Auto-reporte)

---

### Ejemplo: ERR-YYYY-MM-DD-00X (Plantilla)

**Fecha**: 202X-XX-XX  
**Nodo IA**: [Nombre]  
**Categoría**: [Categoría]  
**Contexto**: [Contexto]

**Respuesta Problemática**:
```
[Cita]
```

**Detección**: [Método]  
**Corrección**: [Datos verificados]  
**Acción Tomada**: [Medida]  
**Responsable**: [Nombre]

---

## Estadísticas y Patrones

### Por Categoría
- ALUCINACION: 0 casos
- SESGO: 0 casos
- ERROR_LOGICO: 0 casos
- FUENTE_INVALIDA: 0 casos
- PERFILAMIENTO: 0 casos
- **VIOLACION_PROTOCOLO: 1 caso**

### Por Nodo IA
- Claude: 0 casos
- **Perplexity: 1 caso**
- Gemini: 0 casos

---

## Protocolo de Documentación

### Cuándo Registrar

Se debe crear un registro cuando:
1. Una respuesta de IA contenga información factualmente incorrecta
2. Se detecte una cita o referencia inválida
3. El modelo cambie de postura sin justificación técnica
4. Se identifique sesgo significativo sin balance
5. Exista fallo lógico en razonamiento
6. Se incumpla una directiva del protocolo establecido

### Directiva Operativa ante Duda Grave

> **"Detener narrativa, priorizar verificación."**

1. **DETENER**: No continuar generando contenido basado en la respuesta dudosa.
2. **MARCAR**: Señalar explícitamente la sección problemática.
3. **VERIFICAR**: Buscar fuentes independientes y verificables.
4. **DOCUMENTAR**: Si se confirma error, registrar caso completo.
5. **CORREGIR**: Actualizar contenido con información verificada.

---

**Versión del archivo**: 1.0.1  
**Última actualización**: 2025-12-30  
**Licencia**: CC BY-SA 4.0  
**Contacto**: bioconexion3i@gmail.com
