
    FROM python:3.10-slim
    COPY examples/sql-query.md /app/
    WORKDIR /app
    RUN pip install markdown
    CMD python3 -m markdown sql-query.md
    