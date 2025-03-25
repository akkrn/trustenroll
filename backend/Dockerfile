FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements-backend.txt ./
RUN pip install --upgrade uv && uv venv && uv pip install -r requirements-backend.txt

COPY . .

CMD ["uv", "run", "uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]