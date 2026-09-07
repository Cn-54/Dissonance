#!/bin/bash

set -e

for dir in Lab/Docker-*/; do
    name=$(basename "$dir")

    echo "Building $name..."

    docker build \
        -t "$name" \
        -f "$dir/Dockerfile" \
        .

    echo "$name built successfully."
done

echo
echo "All Docker images built."