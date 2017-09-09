FROM python:2.7.13

RUN apt-get -q update && apt-get install -y -q \
  sqlite3 --no-install-recommends \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LANG C.UTF-8

RUN pip install --upgrade pip virtualenv

RUN virtualenv /venv
ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH

RUN mkdir -p /perfdemo
WORKDIR /perfdemo

ADD requirements.txt /perfdemo/requirements.txt
RUN pip install --no-cache-dir -r /perfdemo/requirements.txt

ADD . /perfdemo

ENV DATADOG_TRACE_AGENT_HOSTNAME=dd-agent
ENV DATADOG_TRACE_AGENT_PORT=8126
ENV DATADOG_TRACE_DEBUG=true
ENV DATADOG_TRACE_ENABLED=true
ENV DATADOG_SERVICE_NAME=django-test
ENV API_KEY=406a7ddd336276ee91fbcd1ff1821473

ENTRYPOINT ["/perfdemo/docker-entrypoint.sh"]
