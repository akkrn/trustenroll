FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY  requirements-bot.txt ./
RUN pip install --upgrade uv && uv venv && uv pip install -r requirements-bot.txt

COPY . .

CMD ["uv", "run", "bot.py"]
