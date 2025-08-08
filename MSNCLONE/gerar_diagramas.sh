#!/bin/bash

# Script para gerar imagens dos diagramas PlantUML
# Requer: java e plantuml.jar

echo "Gerando diagramas PlantUML..."

# Verificar se o PlantUML está disponível
if ! command -v plantuml &> /dev/null; then
    echo "PlantUML não encontrado. Tentando usar java -jar plantuml.jar..."
    
    # Download do PlantUML se não existir
    if [ ! -f "plantuml.jar" ]; then
        echo "Baixando PlantUML..."
        wget -O plantuml.jar https://github.com/plantuml/plantuml/releases/download/v1.2024.8/plantuml-1.2024.8.jar
    fi
    
    # Gerar diagramas usando java
    java -jar plantuml.jar -tpng uso_caso_msn.puml
    java -jar plantuml.jar -tpng diagrama_classes_msn.puml
else
    # Gerar diagramas usando plantuml command
    plantuml -tpng uso_caso_msn.puml
    plantuml -tpng diagrama_classes_msn.puml
fi

# Mover imagens para o diretório static
if [ -f "uso_caso_msn.png" ]; then
    mv uso_caso_msn.png static/core/diagramas/
    echo "Diagrama de Casos de Uso gerado: static/core/diagramas/uso_caso_msn.png"
fi

if [ -f "diagrama_classes_msn.png" ]; then
    mv diagrama_classes_msn.png static/core/diagramas/
    echo "Diagrama de Classes gerado: static/core/diagramas/diagrama_classes_msn.png"
fi

echo "Diagramas gerados com sucesso!"
echo ""
echo "Para visualizar os diagramas online, você também pode usar:"
echo "- http://www.plantuml.com/plantuml/uml/ (colar o código PlantUML)"
echo "- VS Code com extensão PlantUML"
