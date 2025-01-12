FROM python:3.9-slim

WORKDIR /app

# Копіюємо requirements.txt в контейнер
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код в контейнер
COPY . .

# Запускаємо бота
CMD ["python", "bot1.py"]
