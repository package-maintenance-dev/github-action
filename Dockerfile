FROM python:3.11-bookworm
WORKDIR /github/workspace/
COPY . /github/workspace/
RUN make install-dependencies
ENTRYPOINT ["python", "/github/workspace/main.py"]
