FROM python:3.11-bookworm
WORKDIR /action
COPY . .
RUN make install-dependencies
ENTRYPOINT ["python", "/action/main.py"]
