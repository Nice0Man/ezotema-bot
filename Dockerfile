# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY requirements.txt /app

# Устанавливаем зависимости
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN pip install supervisor
RUN chmod 755 .
COPY . /app
# Копируем конфигурацию supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Запускаем supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]