FROM treeder/bump AS builder
USER root

CMD []
ENTRYPOINT []

###############################################################################

FROM python:3-alpine

ARG PORT=""

LABEL maintainer="saidsef@gmail.com"

ENV PORT ${PORT:-7070}
ENV version 1.5

WORKDIR /app

COPY --from=builder /script/bump /usr/bin/
COPY . /app

RUN pip --no-cache-dir install -r requirements.txt && \
    chown -R nobody:nobody .

USER nobody

EXPOSE ${PORT}

HEALTHCHECK --interval=30s --timeout=10s CMD curl --fail http://localhost:${PORT}/ || exit 1

CMD ["bump-api.py"]
ENTRYPOINT ["python"]
