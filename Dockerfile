FROM python:3.11

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install python dependencies
WORKDIR /app
RUN pip install --upgrade pip
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
ADD . /app

# Run the script
CMD ["python3", "main.py"]
