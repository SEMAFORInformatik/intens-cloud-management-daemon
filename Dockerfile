FROM python:3.13.1-alpine3.21

RUN adduser --disabled-password --gecos '' app
ARG REVISION

WORKDIR /app
COPY requirements.txt .
# install the library dependencies for this application
RUN pip3 install --no-cache-dir  -r requirements.txt && opentelemetry-bootstrap -a install; \
  [ -z "$REVISION" ] ||echo "$REVISION" > vcs.info

COPY . .

ENV FLASK_APP="manager"
ENV SERVICE_PORT=3000

EXPOSE ${SERVICE_PORT}
USER app
#
CMD [ "/app/entrypoint.sh" ]
