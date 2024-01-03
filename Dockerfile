# syntax=docker/dockerfile-upstream:master-labs
FROM python:3.10 as builder

ADD https://github.com/flipperdevices/flipperzero_protobuf_py.git#main /build
WORKDIR /build
RUN pip3 install -r requirements.txt
RUN mkdir -p /wheels && pip3 wheel --wheel-dir=/wheels .

FROM python:3.10-slim

WORKDIR /app

RUN --mount=type=bind,from=builder,source=/wheels,target=/wheels pip3 install --no-index --find-links=/wheels flipperzero_protobuf

ENTRYPOINT ["/usr/local/bin/flipperCmd"]
