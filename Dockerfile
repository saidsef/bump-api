FROM treeder/bump AS builder
USER root

CMD []
ENTRYPOINT []

###############################################################################

FROM python:3.6-alpine
MAINTAINER Said Sef <saidsef@gmail.com> (saidsef.co.uk/)

ARG PORT=""

ENV PORT ${PORT:-7070}
ENV version 1.0

WORKDIR /app

COPY --from=builder /script/bump /usr/bin/
COPY . /app

RUN pip install -r requirements.txt && \
    chmod +x /usr/bin/bump

EXPOSE ${PORT}

CMD ["python3", "bump-api.py"]
