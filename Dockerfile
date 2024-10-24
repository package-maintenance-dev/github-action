FROM python:3.11-bookworm
COPY . /github/workspace/
RUN make install-dependencies
ENTRYPOINT ["python", "/github/workspace/main.py"]
