import shutil
from pathlib import Path

import invoke
import kubesae
import yaml
from colorama import init


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


@invoke.task
def build_ci_images(c):
    """Build CircleCI test image using docker-compose"""
    c.run("docker-compose -f docker-compose.yml -f docker-compose-test.yml build app")


@invoke.task(
    help={"command": "Passes a command to the container to run (ex: 'ls -la')"}
)
def run_in_ci_image(c, command):
    """Runs command in the CircleCI test container.

    Args:
        command (str): A bash style command line command of variable length and composition.
    Usage:
        inv ci-run --command='pytest'
    """
    c.run(
        f"docker-compose -f docker-compose.yml -f docker-compose-test.yml run --rm app sh -lc '{ command }'"
    )


@invoke.task
def build_deployable(c):
    """Builds a deployable image using the Dockerfile deploy target"""
    kubesae.image["tag"](c)
    c.run(f"docker build -t {c.config.app}:{c.config.tag} --target deploy .")


@invoke.task(pre=[build_deployable])
def build_deploy(c, push=True, deploy=True):
    """Pushes the built images"""
    if push:
        kubesae.image["push"](c)
    if deploy:
        kubesae.deploy["deploy"](c)


@invoke.task
def reset_local_media(c, dry_run=False, clean_local=False):
    """Sync the media tree for a given deployment into the ./media folder.

    Args:
        dry_run (bool, optional): Show the files to be synced. Defaults to False.
        clean_local (bool, optional): Deletes local media tree first. Defaults to False.
    Usage:
        inv staging sync-media --dry-run
    """
    media_name = kubesae.pod["fetch_namespace_var"](
        c, fetch_var="MEDIA_STORAGE_BUCKET_NAME"
    ).stdout.strip()
    local_media = PROJECT_BASE / "media"
    dr = ""
    if clean_local:
        shutil.rmtree(local_media)
    if dry_run:
        dr = "--dryrun"
    c.run(f"aws s3 sync s3://{media_name}/{c.config.env}/ {PROJECT_BASE} {dr}")


@invoke.task
def reset_local_db(c, dump_file=None):
    """Resets local database with a dumpfile.

    Args:
        dump_file (str, optional): Name of the dumpfile. Defaults to None.
    Usage:
        inv staging reset-database --dump-file="./pg_dump.db"
    """
    if not dump_file:
        kubesae.pod["get_db_dump"](c, db_var="DATABASE_URL")
        dump_file = f"{c.config.namespace}_database.dump"
    database_url = c.run("source .env && echo $DATABASE_URL").stdout.strip()
    if not database_url:
        print(".env is missing a DATABASE_URL definition")
        exit(1)
    c.run(
        f"pg_restore --no-owner --no-acl --clean --if-exists --dbname {database_url} {dump_file}"
    )


@invoke.task
def print_ansible_vars(c, var=None):
    """A command to inspect any ansible varible by environment. If no variable is specified then it will
    print out the current k8s environment variables.

    Args:
        var (string): [description]
    """
    if not var:
        var = "k8s_environment_variables"
    with c.cd("deploy/"):
        c.run(
            f"ansible {c.config.env} -m debug -a var='{var}' -e '@host_vars/{c.config.env}.yml'"
        )


@invoke.task
def ansible_playbook(c, name, extra="", verbosity=1):
    with c.cd("deploy/"):
        c.run(f"ansible-playbook {name} {extra} -{'v'*verbosity}")


@invoke.task
def pod_stats(c):
    """Report total pods vs pod capacity."""
    nodes = yaml.safe_load(c.run("kubectl get nodes -o yaml", hide="out").stdout)
    pod_capacity = sum(
        [int(item["status"]["capacity"]["pods"]) for item in nodes["items"]]
    )
    pod_total = c.run(
        "kubectl get pods --all-namespaces | grep Running | wc -l", hide="out"
    ).stdout.strip()
    print(f"Running pods: {pod_total}")
    print(f"Maximum pods: {pod_capacity}")
    print(f"Total nodes: {len(nodes['items'])}")


project = invoke.Collection("project")
project.add_task(build_ci_images, name="ci-build")
project.add_task(run_in_ci_image, name="ci-run")
project.add_task(build_deploy)
project.add_task(reset_local_media)
project.add_task(reset_local_db)
project.add_task(print_ansible_vars)
project.add_task(pod_stats)
project.add_task(ansible_playbook, name="playbook")

ns = invoke.Collection()
ns.add_collection(kubesae.image)
ns.add_collection(kubesae.aws)
ns.add_collection(kubesae.deploy)
ns.add_collection(kubesae.pod)
ns.add_collection(project)
ns.add_task(staging)
ns.add_task(production)

ns.configure(
    {
        "app": "hip_app",
        "aws": {
            "region": "us-east-2",
        },
        "cluster": "hip-stack-cluster",
        "container_name": "app",
        "repository": "<<Container Repository Here>>",
        "run": {
            "echo": True,
            "pty": True,
            "env": {
                "COMPOSE_FILE": "docker-compose.yml:docker-compose-deploy.yml",
            },
        },
    }
)
