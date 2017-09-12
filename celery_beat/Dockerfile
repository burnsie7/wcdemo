FROM ubuntu:16.04

RUN apt-get update

# Install necessary tooling and python tools
RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential
RUN apt-get install -y python python-dev python-distribute python-pip

ADD . .
RUN pip install -r requirements.txt

ENV DATADOG_TRACE_AGENT_HOSTNAME=dd-agent
ENV DATADOG_TRACE_AGENT_PORT=8126
ENV DATADOG_TRACE_DEBUG=true
ENV DATADOG_TRACE_ENABLED=true
ENV DATADOG_SERVICE_NAME=wcd-celery
ENV API_KEY=406a7ddd336276ee91fbcd1ff1821473

# Run the celeryd worker
CMD DATADOG_ENV=wcd ddtrace-run celery -A perfdemo.perfdemo beat --loglevel=info
