FROM node:20-bookworm-slim as static_files
WORKDIR /code
ENV PATH /code/node_modules/.bin:$PATH
COPY package.json package-lock.json webpack.config.js /code/
RUN npm install --silent
COPY . /code/
RUN npm run build

FROM python:3.11-slim-bookworm as base

# Install packages needed to run your application (not build deps):
#   mime-support -- for mime types when serving static files
#   postgresql-client -- for running database commands
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    mime-support \
    postgresql-client-12 \
    vim \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get -y install wget gnupg2 lsb-release \
    && sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy in your requirements file
# ADD requirements.txt /requirements.txt

# OR, if you're using a directory for your requirements, copy everything (comment out the above and uncomment this if so):
ADD requirements /requirements

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    libffi-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install -U -q pip-tools \
    && pip-sync requirements/base/base.txt requirements/deploy/deploy.txt \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code/
WORKDIR /code/
ADD . /code/

COPY --from=static_files /code/hip/static /code/hip/static

FROM base AS deploy

# Create a group and user to run our app
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# uWSGI will listen on this port
EXPOSE 8000

# Add any static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=hip.settings.deploy

# silence django-dotenv warning
RUN touch /code/.env

# Compile all the scss files
RUN DATABASE_URL='' DJANGO_SECRET_KEY='dummy' DOMAIN='' python manage.py compilescss
# Run collectstatic (ignore scss files so only the compiled files end up in the STATIC_ROOT)
RUN DATABASE_URL='' DJANGO_SECRET_KEY='dummy' DOMAIN='' python manage.py collectstatic --noinput --ignore=*.scss --no-default-ignore

# Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE=hip/wsgi.py

# Base uWSGI configuration (you shouldn't need to change these):
ENV UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy UWSGI_IGNORE_SIGPIPE=true UWSGI_IGNORE_WRITE_ERRORS=true UWSGI_DISABLE_WRITE_EXCEPTION=true

# Number of uWSGI workers and threads per worker (customize as needed):
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4

# Reload workers after the specified amount of managed requests (avoid memory leaks)
ENV UWSGI_MAX_REQUESTS=1000

# uWSGI static file serving configuration (customize or comment out if not needed):
ENV UWSGI_STATIC_MAP="/static/=/code/static/" UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

# Change to a non-root user
USER ${APP_USER}:${APP_USER}

# Uncomment after creating your docker-entrypoint.sh
ENTRYPOINT ["/code/docker-entrypoint.sh"]

# Start uWSGI
CMD ["newrelic-admin", "run-program", "uwsgi", "--single-interpreter", "--enable-threads", "--show-config"]


FROM python:3.11-slim-bookworm AS dev

ARG USERNAME=appuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create non-root user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID --create-home --shell /bin/bash $USERNAME

# Install packages for Dev Container development
#   build-essential -- for gcc to compile non-wheel packages with C dependencies
#   docker-ce-cli -- docker CLI
#   docker-compose-plugin -- docker compose CLI
#   git-core -- to pull, commit, and push from dev container
#   gnupg2 -- GNU privacy guard - a free PGP replacement
#   libpq-dev -- header files for PostgreSQL
#   openssh-client -- for git over SSH
#   sudo -- to run commands as superuser
#   vim -- enhanced vi editor for commits
ENV KUBE_CLIENT_VERSION="v1.25.10"
ENV HELM_VERSION="3.12.0"
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    --mount=type=cache,mode=0755,target=/root/.cache/pip \
    set -ex \
    && RUN_DEPS=" \
    build-essential \
    docker-ce-cli \
    docker-compose-plugin \
    git-core \
    gnupg2 \
    jq \
    libpcre3 \
    libpq-dev \
    libpng-dev \
    libjpeg-dev \
    libssl-dev \
    libffi-dev \
    mime-support \
    nodejs \
    openssh-client \
    postgresql-client-14 \
    sudo \
    vim \
    zlib1g-dev \
    " \
    && apt-get update && apt-get -y install curl wget gnupg2 lsb-release \
    # starship.rs prompt
    && curl -sS https://starship.rs/install.sh | sh -s -- -y \
    # kubectl
    && curl --silent -L https://dl.k8s.io/release/$KUBE_CLIENT_VERSION/bin/linux/$(dpkg --print-architecture)/kubectl -o /usr/local/bin/kubectl \
    && chmod +x /usr/local/bin/kubectl \
    # helm
    && curl --silent -L https://get.helm.sh/helm-v$HELM_VERSION-linux-$(dpkg --print-architecture).tar.gz --output - | tar -xzC /tmp \
    && mv /tmp/linux-$(dpkg --print-architecture)/helm /usr/local/bin/helm \
    && chmod +x /usr/local/bin/helm \
    # docker
    && curl https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor | tee /etc/apt/trusted.gpg.d/docker.gpg >/dev/null \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/trusted.gpg.d/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    # nodejs
    && sh -c 'echo "deb https://deb.nodesource.com/node_20.x $(lsb_release -cs) main" > /etc/apt/sources.list.d/nodesource.list' \
    && wget --quiet -O- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - \
    # PostgreSQL
    && sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
    && curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg >/dev/null \
    # dev packages
    && apt-get update \
    && apt-get install -y --no-install-recommends $RUN_DEPS \
    # sudo
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

COPY --chown=$USER_UID:$USER_GID . /code/

USER $USERNAME
RUN set -ex \
    && touch /code/.env \
    && echo 'eval "$(starship init bash)"' >> ~/.bashrc

ENV DJANGO_SETTINGS_MODULE=hip.settings.dev
ENV PATH=/code/venv/bin:$PATH

WORKDIR /code

CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
