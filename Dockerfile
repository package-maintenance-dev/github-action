FROM python:3.11-bookworm
WORKDIR /app
COPY . /app
RUN make install-dependencies
ENTRYPOINT ["python", "main.py"]
