from pathlib import Path

import invoke
import kubesae
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


ns = invoke.Collection()
ns.add_collection(kubesae.image)
ns.add_collection(kubesae.aws)
ns.add_collection(kubesae.deploy)
ns.add_collection(kubesae.pod)
ns.add_collection(kubesae.info)
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
            "env": {
                "COMPOSE_FILE": "docker-compose.yml:docker-compose-deploy.yml",
            },
        },
    }
)
