FROM python:3.12-slim

WORKDIR /app
#Evita generar archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
#Permite ver los registros de python inmediatamente
ENV PYTHONUNBUFFERED=1
#instala las dependencias del sistema necesarias para compilar
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]