
###############################################
# Base Image
###############################################
FROM python:3.10.9-slim-buster

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
# Following up, we will install system and python dependencies.
#RUN apt-get update \
#  && apt-get -y install netcat gcc libpq-dev \
#  && apt-get install --no-install-recommends -y curl build-essential \
#  && apt-get clean
# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python
# Install poetry separated from system interpreter
#RUN python3 -m venv $POETRY_HOME \
#	&& $POETRY_HOME/bin/pip install -U pip setuptools \
#	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}
EXPOSE 80
WORKDIR $PYSETUP_PATH
COPY ./ ./
# If on cloud run uncomment to use tmp file storage
# RUN --mount=type=tmpfs,target=/tmp
# RUN chmod -R ### /tmp/folder
# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
# RUN pip install setuptools
RUN poetry install --no-dev
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
# CMD ["uvicorn", "resize_image.api:app", "--host", "0.0.0.0", "--port", "8080"]
# gunicorn --bind 0.0.0.0:5000 main:app -k uvicorn.workers.UvicornWorker
CMD gunicorn --bind 0.0.0.0:80 resize_image.api:app -k uvicorn.workers.UvicornWorker
# CMD python -m uvicorn resize_image.api:app --host 0.0.0.0 --port ${PORT}