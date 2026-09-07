#!/bin/bash

set -e

for dir in Lab/Docker-*/; do

    name=$(basename "$dir" | tr '[:upper:]' '[:lower:]')

    echo "Building $name..."

    sudo docker build \
        -t "$name" \
        -f "$dir/Dockerfile" \
        .

    echo "$name built successfully."

done

echo
echo "All Docker images built."