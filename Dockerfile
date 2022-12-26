
###############################################
# Base Image
###############################################
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.11 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python

WORKDIR $PYSETUP_PATH
COPY ./ ./
# If on cloud run uncomment to use tmp file storage
# RUN --mount=type=tmpfs,target=/tmp
# RUN chmod -R ### /tmp/folder
# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

#CMD ["uvicorn", "resize_image.api:app", "--host", "0.0.0.0", "--port", "8080"]
#gunicorn --bind 0.0.0.0:5000 main:app -k uvicorn.workers.UvicornWorker
CMD gunicorn --bind 0.0.0.0:8080 resize_image.api:app -k uvicorn.workers.UvicornWorker
