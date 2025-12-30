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

#### 1.2 HIPÓTESIS
**Definición**: Extrapolación razonada basada en datos existentes, pero sin verificación empírica directa.
**Formato**: `[HIPÓTESIS] Afirmación inferida. Basada en: [fuentes]. Método: [descripción]. Confianza: [bajo/medio/alto].`

#### 1.3 ESPECULACIÓN
**Definición**: Planteamiento exploratorio sin soporte suficiente.
**Formato**: `[ESPECULACIÓN] Idea exploratoria. Propósito: [ideación/pregunta]. No verificada.`

---

## 2. TIPOS DE FUENTES VERIFICABLES

### Categoría A: Alta Verificabilidad
- Artículos científicos (DOI)
- Datasets públicos con identificador
- Informes ONU, NASA, IPCC
- Estándares ISO, IEEE

### Categoría B: Verificabilidad Media
- Preprints (arXiv)
- Documentación técnica oficial
- Informes de ONGs reconocidas

### Categoría C: Baja (Uso Limitado)
- Prensa generalista (solo contexto)
- Blogs especializados
- Redes sociales (solo citas directas)

---

## 3. CHECKLIST DE VERIFICACIÓN

- [ ] Todas las afirmaciones factuales identificadas
- [ ] Etiquetas aplicadas: [HECHO], [HIPÓTESIS], [ESPECULACIÓN]
- [ ] Hechos incluyen fuente verificable (Nivel A o B preferentemente)
- [ ] Hipótesis incluyen base de datos y nivel de confianza
- [ ] Enlaces verificados y funcionales
- [ ] Separación clara entre capa factual y narrativa

---

## 4. TEMPLATES

### Template: Análisis Técnico

[Título]
Autor: [Nombre] | Fecha: [Fecha]

Hechos Verificables
[HECHO] Dato clave 1. [Fuente: DOI/URL]

Hipótesis
[HIPÓTESIS] Proyección X. Base: [Fuente]. Confianza: Media.

Referencias
[Cita completa]


---

## 5. METAS 2026
- 100% documentos técnicos con checklist completado.
- 95% de hechos con fuente verificable.

**Licencia**: CC BY-SA 4.0 | **Contacto**: bioconexion3i@gmail.com
