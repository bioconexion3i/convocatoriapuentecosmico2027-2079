#!/bin/bash
set -e
SERVICE_NAME="soe"
echo "🔧 Instalando servicio systemd del SOE..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME
echo "✅ Servicio $SERVICE_NAME instalado, habilitado e iniciado."
echo ""
echo "📋 Comandos útiles:"
echo "   sudo systemctl status $SERVICE_NAME"
echo "   sudo journalctl -u $SERVICE_NAME -f"
