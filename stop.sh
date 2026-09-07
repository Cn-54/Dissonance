#!/bin/bash

for dir in Lab/Docker-*/; do

    image=$(basename "$dir" | tr '[:upper:]' '[:lower:]')

    echo "Stopping $image..."

    sudo docker stop "$image" 2>/dev/null || true
    sudo docker rm "$image" 2>/dev/null || true

done

echo
echo "All Dissonance containers stopped and removed."