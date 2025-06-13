# Usar la imagen oficial de Python como base
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto de Flask
EXPOSE 5000

# Por defecto ejecuta app.py (usuarios)
CMD ["python", "app.py"]
