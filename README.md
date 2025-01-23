# PDPH Health Information Portal


## ✏️ **Develop**
To begin you should have the following applications installed on your local development system:

- Python >= 3.11
- NodeJS == 20.5.x
- npm == 9.8.x (comes with node 16)
- [nvm](https://github.com/nvm-sh/nvm/blob/master/README.md) is not strictly _required_, but will almost certainly be necessary unless you just happen to have Node.js 16.x installed on your machine.
- [pip](http://www.pip-installer.org/) >= 20
- [virtualenv](http://www.virtualenv.org/) >= 1.10
- [virtualenvwrapper](http://pypi.python.org/pypi/virtualenvwrapper) >= 3.0
- Postgres >= 15
- git >= 2.26


### 🤷‍♂️ **Making changes to templates or stylesheets?**
This project uses [django-sass-processor](https://pypi.org/project/django-sass-processor/) for sass compilation and stylesheet management.

#### Stick to the following conventions when adding new templates
A template is one of:
1. page
  - these should be named `[page_name]_page.html`, lives in the templates/pages directory
2. include
  - no naming convention, a good place for html components, lives in the  templates/includes directory
  - these should be named `[component].html`
3. base
  - these are for high-level layout base-templates

#### Stylesheets follow the same convention. Stylesheets for pages live in the static/styles/pages directory, and so on.

#### To include a **new scss file** in a template, do the following:

Name your file according to the following convention:
1. If your scss file is for a html component add the file to `styles/includes` in the `static` directory in the `hip` project folder. If the scss file is for a html page add the file to `styles/pages` in the `static` directory in the `hip` project folder.
1. If your scss file is going to be linked to directly from a template, as below, name the file `[template_name].scss`. If styling for a component, name the file `[component].scss`.
2. If your scss file is only going to be imported by another scss file using the `@import` directive, prepend the filename with an underscore: `_[my_sass_file].scss`. Otherwise, all scss files that will provide styling for DOM elements need to imported into `hip/static/bundle.scss`.  `bundle.scss` is imported into `hip/templates/base.html` using django-sass-processor provided `sass_tags`.

#### Naming convention for individual scss classes

All styles in the scss file should have `-hip` appended to the end of their name. This is so developers can easily distinguish between any frameworks/style guides in use and our own custom scss.


```html
{% load sass_tags %}
<link href="{% sass_src '[app]/styles/[includes,pages,blocks]/[template-name].scss' %}" rel="stylesheet" type="text/css" />
```

We're doing our best to follow BEM, [Here's](https://www.smashingmagazine.com/2018/06/bem-for-beginners/) a little reading on BEM.


When styling, keep the following conventions in mind:
- If you're creating a new template, create a new stylesheet.
- Every stylesheet has its own brief documentation including
1. an "Index" describing the contents per BEM "block".
2. a description of each BEM "block"
- Keep it as flat as possible. Try to only nest state changes, like ":hover" or ".open".
- Is there a variable for that?
- REM is set up to change size based on screen width. Keep this in mind. You might actually want pixels!

### 🐳 **Development Container**

This project supports using a [Caktus Development Container](https://caktus.github.io/developer-documentation/developer-onboarding/dev-containers/). Make sure you have installed the [prerequisites](https://caktus.github.io/developer-documentation/developer-onboarding/dev-containers/#prerequisites), including the Remote Development extension pack for VS Code.

1. **Build and start dev container:** Using the [VS Code Command Pallete (`⇧⌘P`)](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette), select `Dev Containers: Reopen in Container`.
2. **Install Python and Node requirements:** 
   ```sh
   python3 -m venv /code/venv
   make setup
   npm install
   ```
2. **Setup pre-commit:** Install pre-commit to enforce a variety of community standards:
   ```sh
   pre-commit clean
   pre-commit install
   ```
3. **Reset local database:** Download copy of staging database and restore it locally:
   ```sh
   inv aws.configure-eks-kubeconfig
   inv staging pod.get-db-dump
   dropdb --if-exists hip && createdb hip
   pg_restore -Ox -d $DATABASE_URL < *.dump
   rm hip-staging_database.dump
   ```
4. **Reset local media:** Download copy of staging media:
   ```sh
   inv staging aws.sync-media --sync-to local --bucket-path="media/"
   ```
5. **Start Python dev server:** Start the Django development server:
   ```sh
   python manage.py runserver 0.0.0.0:8000
   ```

### 💪 **Setup Manually**

**1. Get the project**

First clone the repository from Github and switch to the new directory:

```linux
    $ git clone git@github.com:caktus/philly-hip.git
    $ cd philly-hip
```

**2. Set up virtual environment**

Next, set up your virtual environment:

```linux
    # Check that you have python3 installed
    $ which python3

    # Create the virtual environment, either with mkvirtualenv:
    $ mkvirtualenv hip -p `which python3`

    # or directly (if your system is set up differently than mkvirtualenv assumes):
    $ python3 -m virtualenv ~/.virtualenvs hip
    $ ln -s ~/.virtualenvs hip/bin/activate .venv
    $ source .venv
```


**3. Install dependencies**

``nvm`` is preferred for managing Node versions and ``.nvmrc`` contains the
specific Node version for this project. To install the correct (and latest)
Node version run:

```sh
    (hip)$ nvm install
```

Now install the project Node packages with ``npm``:

```sh
    (hip)$ npm install
```

Install Python dependencies with:

```linux
    (hip)$ make setup
```

NOTE: This project uses ``pip-tools``. If the dependency `.txt` files need to be
updated:

```sh
    (hip)$ make update_requirements setup
```

NOTE 2: During a development cycle if a developer needs to add subtract or modify the requirements of the project, the
workflow is to:

1) Make the change in the ``*.in`` requirement file
2) run ``make update_requirements``
3) commit both ``*.in`` file(s) and the ``*.txt`` file(s) generated


**4. Pre-commit**

pre-commit is used to enforce a variety of community standards. CI runs it,
so it's useful to setup the pre-commit hook to catch any issues before pushing
to GitHub and reset your pre-commit cache to make sure that you're starting fresh.

To install, run:

```linux
    (hip)$ pre-commit clean
    (hip)$ pre-commit install
```


**5. Set up local env variables**

Next, we'll set up our local environment variables. We use
[django-dotenv](https://github.com/jpadilla/django-dotenv) to automatically read
environment variables located in a file named `.env` in the top level directory of the
project (but you may use any other way of setting environment variables, like direnv or
manually setting them). The only variable we need to start is `DJANGO_SETTINGS_MODULE`:

```linux
    (hip)$ cp hip/settings/local.example.py hip/settings/local.py
    (hip)$ echo "DJANGO_SETTINGS_MODULE=hip.settings.local" > .env
```


**6. Database**

These instructions assume that you will be working with dockerized services.

First add the following line to your `.env` file:

```sh
(hip)$ echo "DATABASE_URL=postgres://postgres@127.0.0.1:5432/hip" >> .env
```

The `docker-compose.yml` sets up environment variables in a file, ``.postgres``.
To use the Docker setup, add these lines to that file:

```sh
    POSTGRES_DB=hip
    POSTGRES_HOST_AUTH_METHOD=trust
```

If you want to connect to the database from your host machine, export the
following shell environment variables:

```sh
    export PGHOST=127.0.0.1
    export PGPORT=5433
    export PGUSER=postgres
    export PGDATABASE=hip
```

If you're setting up your database with a dump from staging or production, 
your local server may not be configured to allow for page previews in the 
Wagtail admin. 
If the preview feature returns with a DisallowedHost error, visit [/cms/sites](http://localhost:8000/cms/sites/) 
and change the first entry's `Hostname` field to `localhost`.


**7. Migrate and create a superuser**

```linux
    (hip)$ docker-compose up -d
    (hip)$ python manage.py migrate
    (hip)$ python manage.py createsuperuser
```

**8. Run the server**

```linux
    (hip)$ docker-compose up -d
    (hip)$ make run-dev
```

After initial setup the development server should be run using ``make run-dev`` this will remove any deployment containers hanging around and setup using local sources and database.

**9. Access the server**

The Django admin is at ``/admin`` and the Wagtail admin is at ``/cms``.

**10. Run tests**

hip uses pytest as a test runner.


```sh
    (hip)$ make run-tests
```

**11. Reset Media and Database**

hip uses invoke for interactions with the deployed environments.

**Media Reset**


From time to time it may become necessary to sync your local media tree with either production or staging.

The basic command for resetting your local media is this:


```sh
    (hip)$ inv staging aws.sync-media --sync-to="local" --bucket-path="media"
```

Use the ``dry-run`` argument to see what would be done, without actually doing it.


```sh
    (hip)$ inv staging aws.sync-media --sync-to="local" --bucket-path="media" --dry-run
```

If you wish to clean out your local media tree before reset you can issue the command with a ``delete`` argument.


```sh
    (hip)$ inv staging aws.sync-media --sync-to="local" --bucket-path="media" --delete
```


**Database Reset**

To reset your local database from a deployed environment:


```sh
    (hip)$ inv staging project.reset-local-db
```

As mentioned in the Database setup instructions, you may need to visit 
[/cms/sites](http://localhost:8000/cms/sites/) and change the first entry's 
`Hostname` field to `localhost` to enable page previews in the Wagtail admin.

### GitHub Actions Runner

There are [GitHub Actions self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners) deployed in the Kubernetes cluster along side the application.

Setup instructions:

* Obtain a [GitHub PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with the `repo` scope that's valid for one week (it needs to be active only for the initial deployment). Add this to a local environment variable `RUNNER_CFG_PAT`:

```sh
export RUNNER_CFG_PAT="gh......"
```

* Run the playbook to deploy the runner:

```sh
cd deploy/
ansible-playbook deploy-runner.yml
```
