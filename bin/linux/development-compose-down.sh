#!/bin/bash

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

docker-compose --file ${BIN_DIR}/../../docker-compose.development.yml --project-name opa-http-api-dev down $@
