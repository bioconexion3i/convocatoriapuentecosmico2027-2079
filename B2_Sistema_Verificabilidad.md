# B.2 Sistema de Verificabilidad

**Protocolo**: BioConexion3i v1.0.0  
**Directiva**: B.2 - Directiva de Verificabilidad  
**Versión**: 1.0.0  
**Fecha**: 2025-12-30  
**Estado**: OPERACIONAL

---

## Objetivo

Implementar un sistema operacional que garantice que toda afirmación factual relevante en el proyecto Puente Cósmico incluya trazabilidad verificable o etiquetado explícito de su nivel epistémico.

---

## 1. TAXONOMÍA EPISTÉMICA

### Categorías de Afirmaciones

#### 1.1 HECHO VERIFICABLE
**Definición**: Afirmación respaldada por fuente externa verificable o documento interno oficial.
**Formato**: `[HECHO] Afirmación factual. [Fuente: URL/DOI/Referencia]`

**Ejemplos válidos**:
- Datos científicos publicados en journals revisados por pares
- Estadísticas de organismos oficiales (ONU, NASA, IPCC)
- Documentos internos del proyecto versionados
- Datasets públicos con DOI
- Estándares técnicos publicados (ISO, IEEE, W3C)

#### 1.2 HIPÓTESIS
**Definición**: Extrapolación razonada basada en datos existentes, pero sin verificación empírica directa.
**Formato**: `[HIPÓTESIS] Afirmación inferida. Basada en: [fuentes]. Método: [descripción]. Confianza: [bajo/medio/alto].`

**Ejemplos**:
- Proyecciones de tendencias basadas en series temporales
- Modelos predictivos con parámetros conocidos
- Inferencias causales con correlaciones documentadas

#### 1.3 ESPECULACIÓN
**Definición**: Planteamiento exploratorio sin soporte suficiente.
**Formato**: `[ESPECULACIÓN] Idea exploratoria. Propósito: [ideación/pregunta]. No verificada.`

**Ejemplos**:
- Escenarios futuros sin modelado riguroso
- Conexiones metafóricas entre dominios
- Preguntas de investigación emergentes

---

## 2. TIPOS DE FUENTES VERIFICABLES

### Categoría A: Alta Verificabilidad
- Artículos científicos (DOI)
- Datasets públicos con identificador
- Informes ONU, NASA, IPCC, IPBES
- Estándares ISO, IEEE, W3C

### Categoría B: Verificabilidad Media
- Preprints (arXiv, bioRxiv)
- Documentación técnica oficial
- Informes de ONGs reconocidas

### Categoría C: Baja (Uso Limitado)
- Prensa generalista (solo contexto)
- Blogs especializados
- Redes sociales (solo citas directas)

---

## 3. CHECKLIST DE VERIFICACIÓN

**Para todo documento o sección con contenido factual**:

```markdown
## Checklist de Verificabilidad B.2

- [ ] Todas las afirmaciones factuales identificadas
- [ ] Cada afirmación tiene etiqueta [HECHO/HIPÓTESIS/ESPECULACIÓN]
- [ ] Hechos incluyen fuente verificable (URL/DOI/referencia interna)
- [ ] Hipótesis describen base de datos y método de inferencia
- [ ] Especulaciones marcan propósito exploratorio
- [ ] Enlaces verificados como funcionales
- [ ] Fuentes accesibles a terceros
- [ ] Fechas de acceso incluidas para URLs sin DOI
- [ ] Separación clara entre capa factual y narrativa
- [ ] Límites de conocimiento declarados explícitamente
```

---

## 4. TEMPLATES DE DOCUMENTACIÓN

### Template para Análisis Técnico

```markdown
# [Título del Análisis]

**Autor**: [Nombre/Nodo IA]  
**Fecha**: [YYYY-MM-DD]  
**Verificación**: [Estado del checklist B.2]

## Resumen Ejecutivo
[Síntesis sin afirmaciones factuales o con citas inline]

## Hechos Verificables

### [Sección 1]
[HECHO] Afirmación 1. [Fuente: Autor et al., 2024. DOI: 10.xxxx/xxxxx]

[HECHO] Afirmación 2. [Fuente interna: README.md, Sección "Objetivos 2079", v1.0.0]

## Hipótesis de Trabajo

### [Hipótesis 1]
[HIPÓTESIS] Si se implementa X, entonces Y.
- **Base de datos**: [fuente 1], [fuente 2]
- **Método**: Extrapolación lineal de tendencia 2010-2025
- **Supuestos**: A, B, C
- **Confianza**: Media (limitado por disponibilidad de datos)

## Especulaciones Exploratorias

[ESPECULACIÓN] Podría existir relación entre A y B. Propósito: Generar pregunta de investigación. No verificada.

## Referencias

1. [Formato APA o similar]
2. ...

## Checklist B.2
- [x] Verificado
```

---

## 5. METAS DE CUMPLIMIENTO

**Meta 2026**:
- 100% de documentos técnicos con checklist B.2 completado
- 95% de [HECHO] con fuente verificable
- <5% de enlaces rotos

---

## 6. INTEGRACIÓN CON OTRAS DIRECTIVAS

### Relación con B.3 (Gestión de Incertidumbre)
- Las etiquetas [HIPÓTESIS] deben incluir nivel de confianza
- Ver `B3_Sistema_Incertidumbre.md` para detalles de escala

### Relación con B.5 (Separación Dato/Narrativa)
- Capa factual: Solo [HECHO] y [HIPÓTESIS]
- Capa narrativa: Puede incluir [ESPECULACIÓN] claramente marcada

### Relación con B.8 (Errores)
- Fuentes inválidas se registran en ERRORES_IA.md
- Categoría: FUENTE_INVALIDA

---

## Metadatos

**Versión**: 1.0.0  
**Implementa**: Directiva B.2 del Protocolo BioConexion3i  
**Archivos relacionados**:  
- `Protocolo_BioConexion3i.md` (Directiva B.2)  
- `ERRORES_IA.md` (Categoría: FUENTE_INVALIDA)  
- `B3_Sistema_Incertidumbre.md` (Niveles de confianza)  

**Licencia**: CC BY-SA 4.0  
**Mantenedores**: Tlacuilo + Comité BioConexion3i  
**Contacto**: bioconexion3i@gmail.com

---

**Próxima revisión**: 2026-12-30