# Ubuntu 22.04 base as required
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    pip3 install --no-cache-dir --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install deps first for better layer caching
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# then app code
COPY . .

EXPOSE 5000
CMD ["python3", "-m", "gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "wsgi:application"]
