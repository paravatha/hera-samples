from hera.auth import ArgoCLITokenGenerator
from hera.workflows import DAG, Steps, Workflow, WorkflowsService, script
from hera.shared import global_config

global_config.verify_ssl = False
global_config.host = "https://localhost:2746"
global_config.token = ArgoCLITokenGenerator


@script()
def flip():
    import random

    result = "heads" if random.randint(0, 1) == 0 else "tails"
    print(result)


@script()
def heads():
    print("it was heads")


@script()
def tails():
    print("it was tails")


with Workflow(generate_name="coinflip-", 
                entrypoint="d",
                service_account_name="hera",
                namespace="argo",
              ) as w:
    with DAG(name="d") as s:
        f = flip()
        heads().on_other_result(f, "heads")
        tails().on_other_result(f, "tails")

w.create()
       