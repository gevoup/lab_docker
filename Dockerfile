FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip/* && \
    rm -rf /var/cache/apk/* && \
    rm -rf /tmp/*

COPY . .

RUN addgroup -S appgroup && adduser -S appuser -G appgroup && \
    chown -R appuser:appgroup /app && \
    chmod +x init_db.sh

USER appuser

CMD ["sh", "-c", "sh /app/init_db.sh"]
