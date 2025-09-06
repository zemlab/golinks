FROM ghcr.io/astral-sh/uv:alpine3.22

ENV USER_ID=65535
ENV GROUP_ID=65535
ENV USER_NAME=app
ENV GROUP_NAME=app

RUN addgroup -g $GROUP_ID $GROUP_NAME && \
    adduser --shell /sbin/nologin --disabled-password \
    --uid $USER_ID --ingroup $GROUP_NAME $USER_NAME


RUN mkdir /app && chown $USER_NAME:$GROUP_NAME /app
USER $USER_NAME
COPY . /app


WORKDIR /app
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1


RUN uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["golinks"]