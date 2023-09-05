from hera.workflows import DAG, Steps, Workflow, WorkflowsService, script
from hera.shared import global_config
#global_config.host = "https://localhost:2746"
# Copy token value after "Bearer" from the `argo auth token` command
#global_config.token = ""  
# global_config.image = "<your-image-repository>/python:3.8"  # Set the image if you cannot access "python:3.8" via Docker Hub
#global_config.verify_ssl = False

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
                service_account_name="jenkins",
                namespace="argo",
              ) as w:
    with DAG(name="d") as s:
        f = flip()
        heads().on_other_result(f, "heads")
        tails().on_other_result(f, "tails")

w.create()
       