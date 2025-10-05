FROM python:3.11-slim

# system deps for Playwright
RUN apt-get update \
  && apt-get install -y \
     libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
     libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
     libasound2 libpangocairo-1.0-0 libpangoft2-1.0-0 libpci3 \
     libxshmfence1 wget gnupg \
  && rm -rf /var/lib/apt/lists/*

# Python libs + Playwright browsers
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt \
  && pip install --no-cache-dir playwright \
  && playwright install --with-deps

# app code
COPY src/ /app/src
COPY .env /app/.env
COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
