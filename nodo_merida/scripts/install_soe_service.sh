#!/bin/bash
set -e
SERVICE_NAME="soe"
echo "🔧 Instalando servicio systemd del SOE..."
sudo cp /etc/systemd/system/$SERVICE_NAME.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME
echo "✅ Servicio $SERVICE_NAME instalado, habilitado e iniciado."
