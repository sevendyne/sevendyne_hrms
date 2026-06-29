FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc libjpeg-dev zlib1g-dev \
    libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 libffi-dev shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/local.txt

COPY . .

RUN chmod +x compose/local/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["compose/local/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
