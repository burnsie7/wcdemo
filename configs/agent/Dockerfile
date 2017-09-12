FROM datadog/docker-dd-agent:latest

ENV HOST_PROC=/host/proc
ENV HOST_SYS=/host/sys

ADD conf.d/gunicorn.yaml /etc/dd-agent/conf.d/gunicorn.yaml
ADD conf.d/postgres.yaml /etc/dd-agent/conf.d/postgres.yaml
ADD conf.d/redisdb.yaml /etc/dd-agent/conf.d/redisdb.yaml

RUN echo "apm_enabled: true" >> /etc/dd-agent/datadog.conf
RUN echo "process_agent_enabled: true" >> /etc/dd-agent/datadog.conf

EXPOSE 8125
EXPOSE 8126
