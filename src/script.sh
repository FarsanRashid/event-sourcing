#!/bin/bash

docker run --name kurrentdb-node -it -p 2113:2113 \
  docker.kurrent.io/kurrent-latest/kurrentdb:latest \
  --insecure \
  --run-projections=all \
  --enable-atom-pub-over-http
