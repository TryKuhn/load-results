FROM oven/bun:1-alpine
LABEL authors="try_kuhn"

EXPOSE 8000

WORKDIR /load-results

# Update packages
RUN apk update && \
    apk upgrade && \
    apk add curl make bash nodejs-current supervisor python3 py-pip python3-dev musl-dev pkgconf mariadb-dev gcc

# Python requirements
COPY requirements.txt /load-results/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Moving files
COPY web /load-results/web
COPY deployment/Makefile /load-results/Makefile
COPY deployment/supervisord.conf /load-results/supervisord.conf
COPY pylintrc.toml /load-results/pylintrc.toml

ENTRYPOINT ["top", "-b"]