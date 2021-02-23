from pathlib import Path

import invoke
import kubesae
from colorama import Fore, init


PROJECT_BASE = Path(__file__).resolve().parent

init(autoreset=True)


@invoke.task
def staging(c):
    c.config.env = "staging"
    c.config.namespace = "hip-staging"


@invoke.task
def production(c):
    c.config.env = "production"
    c.config.namespace = "hip-production"


# project-specific tasks

# NOTE: Put things here if they are helpful, but try to eventually move these to
# invoke-kubesae if they are generally useful to other projects


@invoke.task
def reset_local_db(c, dump_file=None):
    """Reset local database from a Postgres dump file.

    Args:
        dump_file (str, optional): Name of the dumpfile. If not provided, a dump
                                   file will be downloaded from the specified environment.
    Usage:
        inv staging reset-local-db --dump-file="./pg_dump.db"
    """
    if not dump_file:
        kubesae.pod["get_db_dump"](c, db_var="DATABASE_URL")
        dump_file = f"{c.config.namespace}_database.dump"
    database_url = c.run("echo $DATABASE_URL").stdout.strip()
    if not database_url:
        print(Fore.RED + "Your environment is missing a DATABASE_URL definition.")
        exit(1)
    c.run(
        f"pg_restore --no-owner --no-acl --clean --if-exists --dbname {database_url} {dump_file}"
    )
    print(
        Fore.GREEN
        + f"Local DB reset. Be sure to delete {dump_file} if you are done with it."
    )


project = invoke.Collection("project")
project.add_task(reset_local_db)

ns = invoke.Collection()
ns.add_collection(kubesae.image)
ns.add_collection(kubesae.aws)
ns.add_collection(kubesae.deploy)
ns.add_collection(kubesae.pod)
ns.add_collection(kubesae.info)
ns.add_collection(project)
ns.add_task(staging)
ns.add_task(production)

ns.configure(
    {
        "app": "hip",
        "aws": {"region": "us-east-1"},
        "cluster": "caktus-saguaro-cluster",
        "container_name": "app",
        "repository": "472354598015.dkr.ecr.us-east-1.amazonaws.com/hip",
        "run": {
            "echo": True,
            "pty": True,
            "env": {"COMPOSE_FILE": "docker-compose.yml:docker-compose-deploy.yml",},
        },
    }
)
