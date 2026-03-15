# Protocolo B6: Marco de Seguridad y Validación Técnica (v1.0.0)

El **Protocolo B6** es el estándar de seguridad obligatorio para la operación del **Puente Cósmico 2027-2079**. Establece los requisitos técnicos para la comunicación entre la infraestructura Edge (Nodos Jetson) y el ecosistema Cloud (GitHub).

## 🛡️ Pilares del Protocolo

### 1. Auditoría de Secretos (Zero-Leak Policy)
- **Herramienta:** TruffleHog v3.93.8+.
- **Requisito:** 0 secretos detectados en el historial de Git (Pass/Fail).
- **Alcance:** Análisis de 476KB+ y 382 chunks de datos históricos.

### 2. Inmunización de la Cadena de Suministro (Supply Chain Security)
- **SHA Pinning:** Queda prohibido el uso de tags mutables (ej. `@v4`) en GitHub Actions. 
- **Mitigación CVE-2025-30066:** Todas las acciones deben referenciarse mediante su **commit hash (SHA)** único para evitar inyección de código malicioso.

### 3. Verificación de Nodo (B6-Verified Identity)
- **Endpoint:** Puerto `8082` (FastAPI).
- **Integridad:** El servicio debe responder con un encabezado de seguridad que certifique el estado del nodo y el timestamp del sistema.
- **Aislamiento:** Ejecución obligatoria bajo Docker con política de reinicio `unless-stopped`.

## ⚙️ Configuración del Nodo Edge (Jetson)
Los nodos deben cumplir con la siguiente especificación de orquestación:
- **Logging:** Rotación de archivos (max-size: 10m, max-file: 3).
- **Red:** Mapeo de puertos `8082:8080`.
- **Persistencia:** Redirección de logs a `stdout` para monitoreo centralizado.
