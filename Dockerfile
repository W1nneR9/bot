# Використовуємо офіційний Python образ з Docker Hub
FROM python:3.9-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файл вимог (якщо він є)
COPY requirements.txt .

# Встановлюємо залежності Python
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо решту коду програми
COPY . .

# Відкриваємо порт, на якому працюватиме додаток (за бажанням)
EXPOSE 8000

# Запускаємо Python додаток
CMD ["python", "bot1.py"]
