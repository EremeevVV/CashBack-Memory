FROM python:3.11.8-slim-bookworm as update_os
SHELL ["/bin/bash", "-c"]

RUN apt update -y || true

FROM update_os as poetry_build
# Creating a python base with shared environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_REQUESTS_TIMEOUT=100 \
    POETRY_INSTALLER_MAX_WORKERS=4 \
    POETRY_VERSION=1.8.1

ENV PATH="$POETRY_HOME/.venv/bin:$PATH"

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_HOME/.venv \
    && $POETRY_HOME/.venv/bin/pip install -U pip setuptools \
    && $POETRY_HOME/.venv/bin/pip install poetry==${POETRY_VERSION}


FROM poetry_build as only_main
WORKDIR /app
# get user identity from compose
ARG USER_ID
ARG GROUP_ID
ARG USERNAME
# Create User
RUN groupadd --gid $USER_ID ${USERNAME} \
    && useradd -u $USER_ID -g $USER_ID --shell /bin/bash --create-home ${USERNAME}
RUN chown $USER_ID:$USER_ID ./

USER ${USERNAME}
# Copy Dependencies
COPY --chown=$USER_ID:$USER_ID poetry.lock pyproject.toml README.md  ./
# Install Dependencies
RUN  mkdir cashback_memory && touch cashback_memory/__init__.py && \
     poetry install --no-interaction --no-cache --only main --sync
COPY --chown=$USER_ID:$USER_ID . ./

CMD poetry run python3 main.py
