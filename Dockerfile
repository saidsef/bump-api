FROM treeder/bump AS builder
USER root

CMD []
ENTRYPOINT []

###############################################################################

FROM python:3-alpine
MAINTAINER Said Sef <saidsef@gmail.com> (saidsef.co.uk/)

ARG PORT=""

ENV PORT ${PORT:-7070}
ENV version 1.5

WORKDIR /app

COPY --from=builder /script/bump /usr/bin/
COPY . /app

RUN pip --no-cache-dir install -r requirements.txt && \
    chown -R nobody:nobody .

USER nobody

EXPOSE ${PORT}

CMD ["python", "bump-api.py"]
