#!/bin/bash

protoc -I=./flipperzero-protobuf --python_out=./flipperzero_protobuf_compiled ./flipperzero-protobuf/*.proto
protol --create-package --in-place --python-out ./flipperzero_protobuf_compiled protoc --proto-path ./flipperzero-protobuf ./flipperzero-protobuf/*.proto