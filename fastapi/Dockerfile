FROM alpine AS fastapi-build

COPY requirements.txt .

# Alpine Package Keeper: apk
RUN apk add python3 python3-dev py-pip libffi libffi-dev musl-dev gcc linux-headers libuv \
  && pip install wheel \
  && pip wheel -r requirements.txt --wheel-dir=/wheels

FROM python:3.11-alpine AS fastapi-api

# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures that the python output is sent straight to terminal
ENV PYTHONUNBUFFERED 1

COPY --from=fastapi-build /wheels /wheels
COPY requirements.txt ./

RUN pip install --no-index --no-cache-dir --find-links=/wheels -r requirements.txt \
  && rm -rf /wheels requirements.txt

COPY /app /app

WORKDIR /app

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
