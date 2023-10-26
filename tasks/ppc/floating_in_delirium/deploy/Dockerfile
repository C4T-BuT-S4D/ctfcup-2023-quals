FROM python:3.10

RUN apt -y update && apt -y install socat

ADD delirium.py /
RUN chmod +x /delirium.py

USER nobody

CMD [ "socat", "TCP-LISTEN:2112,reuseaddr,fork", "EXEC:/delirium.py" ]
