FROM python:3.11-bookworm
COPY . /
RUN make install-dependencies
ENTRYPOINT ["python", "main.py"]
