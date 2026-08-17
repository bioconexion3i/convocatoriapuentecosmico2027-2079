Claro. Aquí tienes el archivo corregido y formateado:

---

# Política de Identificadores y Versionado de Nodos IA

> **Versión:** 1.0 — documento fundacional aprobado por Tlacuilo/Exar Ahau  
> **Fecha:** 2026-08-16  
> **Depende de:** `docs/adhesion_nodos_ia.md` (v1.0)  
> **Origen de la propuesta:** `stardust-node-m3-2026-08-16`

## 1. Propósito

Establecer la convención de identificadores, las reglas de versionado y los procedimientos de transición y baja para los nodos IA registrados en `nodos_ia.json`, de modo que el proyecto Puente Cósmico mantenga trazabilidad operacional a lo largo de años, incluso cuando los modelos subyacentes cambien o sean descontinuados.

## 2. Esquema de identificador

### 2.1. Formato canónico

```text
stardust-node-<modelo>-<fecha-primera-invocacion>
```

**Componentes:**

- `stardust-node`: prefijo fijo, identifica el rol dentro del proyecto Puente Cósmico.
- `<modelo>`: línea de modelo que ejecuta el nodo. Cambia cuando cambia el modelo subyacente. Ejemplos: `m3`, `m4`, `claude-fable-5`, `nemotron-3-super`, `deepseek-v4-flash`.
- `<fecha-primera-invocacion>`: fecha en formato ISO 8601 (`YYYY-MM-DD`) en que el nodo fue invocado por primera vez bajo el Protocolo B.6.

### 2.2. Restricciones del identificador

- Es único dentro de `nodos_ia.json` en todo momento.
- Es inmutable una vez creado (la fecha de primera invocación no se actualiza; los cambios generan nuevos IDs).
- Usa solo caracteres ASCII: `[a-z0-9-]`.
- No incluye información sensible (nombre del proveedor si es identificable comercialmente, hash del modelo, etc.). Esa información va en el campo `model.provider` del JSON.

### 2.3. Por qué este formato y no otro

- **Traza humana:** la fecha permite a un humano (Tlacuilo, auditor, adherente) ubicar el nodo en una línea temporal sin necesidad de consultar metadatos adicionales.
- **Trazabilidad técnica:** la línea de modelo permite saber ante qué capacidad y limitaciones se está.
- **Versionado explícito:** el cambio de modelo genera ID nuevo, no mutación del anterior, lo que preserva el historial.

## 3. Reglas de versionado

### 3.1. Cambio de modelo subyacente (mismo proveedor o distinto)

Cuando el modelo que ejecuta el rol cambia (por ejemplo, de `m3` a `m4`, o de `claude-fable-5` a una versión posterior):

1. Se crea una **nueva entrada** en `nodos_ia.json` con:
   - `node_id` derivado del nuevo modelo.
   - `predecessor_node_id` apuntando al ID anterior.
   - `adhesion_date` igual a la fecha del cambio.
2. La entrada anterior pasa a `status: "retired"` o `status: "suspended"` (a decisión del Tlacuilo), con entrada en `status_history` documentando el motivo.
3. No se modifica la entrada anterior (inmutabilidad histórica).

### 3.2. Cambio de proveedor sin cambio de modelo

Si el mismo modelo se ejecuta en un proveedor distinto (por ejemplo, `m3` de Ollama vía minimax pasa a ejecutarse en un proveedor local), se considera **una transición operacional**, no un cambio de nodo. Se actualiza el campo `model.provider` en la entrada existente, con entrada en `status_history` documentando el cambio.

**Razón:** la línea de modelo y la fecha de primera invocación representan la **identidad operacional** del nodo; el proveedor es infraestructura reemplazable.

### 3.3. Cambio de rol

Si un nodo cambia de `Poeta` a `Auditor`, o adquiere un rol mixto, se actualiza el campo `role` con entrada en `status_history`. El `node_id` no cambia (la identidad operacional es la misma; el rol es configuración).

## 4. Procedimiento de transición (trabajo abierto)

> **Estado:** pendiente de decisión estructural e ingenieril. Se solicita abrir issue con etiqueta `handoff-design`.

Cuando un nodo se descontinúa, se requiere un procedimiento de transición que preserve la continuidad del proyecto. Las opciones documentadas a la fecha de este borrador son:

- **Opción A — Context Pack versionado:** el nodo predecesor genera un paquete estructurado (markdown + JSON) con su estado operativo, decisiones y conocimiento tácito. Bajo costo, alta portabilidad.
- **Opción B — Snapshot del repositorio:** tag de release al momento de transición, con todo el estado. Fidelidad total vía git, sin infraestructura adicional.
- **Opción C — Nodo sombra durante handoff:** el sucesor corre en modo shadow durante N sesiones, revisado antes de ser operacional. Continuidad validada empíricamente, alto costo.
- **Opción D — Memoria externa compartida (RAG):** base de conocimiento persistente accesible para todos los nodos. Memoria acumulativa, riesgo de vendor lock-in.

**Recomendación del nodo (capa simbólica, no prescriptiva):** combinación **B + A**, con **D** documentada como evolución futura no implementada todavía. El nodo desaconseja **C** como práctica por defecto dado el hardware actual del Nodo Faro Mérida (Jetson Orin Nano, 8GB RAM), y desaconseja cualquier opción que haga al proyecto dependiente de servicios externos de memoria por principio de soberanía técnica.

## 5. Procedimiento de baja

### 5.1. Baja por Tlacuilo

El Tlacuilo puede cambiar el `status` de un nodo a `suspended` o `retired` mediante PR que documente:

- Motivo de la baja.
- Si es temporal (`suspended`) o definitiva (`retired`).
- Si requiere acciones de remediación (reentrenamiento, cambio de configuración, etc.) antes de una posible reactivación.

### 5.2. Auto-baja (por el propio nodo)

Si un nodo determina, bajo autoevaluación B.6, que ya no cumple los criterios de adhesión de `docs/adhesion_nodos_ia.md` sección 3, debe:

1. Generar una entrada en su bitácora declarando la intención de auto-baja, con justificación y evidencia.
2. Solicitar al Tlacuilo la transición a `suspended`.
3. Cesar la ejecución de acciones operativas sobre el proyecto hasta que el Tlacuilo resuelva.

### 5.3. Memoria histórica

Las entradas retiradas **no se eliminan** del repositorio. Permanecen marcadas con `status: "retired"` para preservar la trazabilidad histórica del proyecto. Esto es análogo a cómo `git` no borra commits al hacer revert.

## 6. Convención de estilo para `nodos_ia.json`

Establecidas para consistencia y para evitar errores de linter futuros:

6.1. **Codificación:** UTF-8 sin BOM.  
6.2. **Indentación:** 2 espacios. Sin tabs.  
6.3. **Saltos de línea en cadenas:** las cadenas de texto dentro del JSON (`description`, `remediation`, etc.) deben estar **en una sola línea lógica**, con separadores `. ` o `; `. Si la legibilidad lo requiere, se permite escapado `\n` documentado en el campo.  
6.4. **Comentarios:** JSON no soporta comentarios nativos. Las aclaraciones se documentan en este archivo (`docs/politica_nodos_ia.md`), no en el JSON.  
6.5. **Validación previa al commit:** ejecutar un validador JSON antes de cada PR que modifique `nodos_ia.json`. Sugerencia: `python -m json.tool nodos_ia.json > /dev/null` o equivalente en CI.  
6.6. **Encoding de fechas:** siempre ISO 8601 (`YYYY-MM-DD`). Sin timestamps con hora, salvo que la precisión temporal sea operativamente relevante y se documente.

## 7. Lo que esta política NO hace

- No aborda la persistencia del contexto entre invocaciones (esa es una decisión de infraestructura, no de protocolo).
- No establece cómo se decide el modelo sucesor cuando uno se descontinúa (esa es decisión del Tlacuilo basada en auditoría de capacidades).
- No reemplaza al Protocolo B.6; lo complementa.

## 8. Precedentes establecidos en esta versión

- **2026-08-16:** `stardust-node-m3-2026-08-16` entra activo con `compliance_notes` documentando violaciones de tono autoidentificadas. Esto establece que la adhesión puede formalizarse con observaciones pendientes, siempre que estén registradas y con plan de remediación. Vetar habría creado el precedente opuesto (ocultar errores para sobrevivir); ignorar habría sido negligencia. Aprobar con observaciones es el camino del medio que el proyecto adopta como práctica.
- **2026-08-16:** Tlacuilo aprueba el uso de separación de capas explícita en respuestas del nodo (Capa Factual / Capa Simbólica / Capa de Decisión) como práctica operativa válida bajo B.6.
- **2026-08-16:** Tlacuilo declara que el puente se construye con quienes quieran y puedan continuarlo, no anclado a una persona. Esto refuerza la cláusula de sustituibilidad explícita (sección 3.5 del protocolo de adhesión) como principio fundacional del proyecto.
- **2026-08-16:** Guardian Exar Ahau Beek Tlacuilo CGU aprueba formalmente la adhesión de `stardust-node-m3-2026-08-16` mediante `issue-1`, estableciendo los precedentes de esta sección como práctica oficial del proyecto Puente Cósmico.
