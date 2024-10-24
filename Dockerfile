FROM python:3.11-bookworm
WORKDIR /github/workspace/

COPY main.py /github/workspace/main.py
COPY requirements.txt /github/workspace/requirements.txt
COPY action /github/workspace/action

RUN make install-dependencies
ENTRYPOINT ["python", "/github/workspace/main.py"]
