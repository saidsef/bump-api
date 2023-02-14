FROM docker.io/treeder/bump AS builder
USER root

CMD []
ENTRYPOINT []

###############################################################################

FROM docker.io/python:3.11-alpine3.17

ARG PORT=""

LABEL maintainer="saidsef@gmail.com"

ENV PORT ${PORT:-7070}
ENV version 3.1

WORKDIR /app

COPY --from=builder /script/bump /usr/bin/
COPY . /app

RUN pip --no-cache-dir install -r requirements.txt && \
    apk add -U --no-cache expat && \
    chown -R nobody:nobody .

USER nobody

EXPOSE ${PORT}

HEALTHCHECK --interval=60s --timeout=10s CMD curl --fail http://localhost:${PORT}/ || exit 1

CMD ["bump-api.py"]
ENTRYPOINT ["/usr/local/bin/python"]
