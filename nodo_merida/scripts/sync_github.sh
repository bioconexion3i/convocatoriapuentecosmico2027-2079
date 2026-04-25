#!/bin/bash
REPO_DIR="/home/bio/convocatoriapuentecosmico2027-2079"
BRANCH="main"
COMMIT_MSG="⚡ Sincronización automática SOE - $(date '+%Y-%m-%d %H:%M:%S')"

cd "$REPO_DIR" || { echo "❌ Error: No se pudo acceder a $REPO_DIR"; exit 1; }

if [[ -z $(git status --porcelain) ]]; then
    echo "✅ No hay cambios locales que sincronizar."
    exit 0
fi

echo "📝 Cambios detectados:"
git status --short

git add -A
git commit -m "$COMMIT_MSG"
git push origin "$BRANCH" 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Sincronización completada exitosamente."
else
    echo ""
    echo "⚠️ Error al hacer push. Verifica tu conexión y credenciales SSH."
    exit 1
fi
