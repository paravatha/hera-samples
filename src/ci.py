from hera.auth import ArgoCLITokenGenerator
from hera.workflows import Steps, Resources, Workflow, script
from hera.shared import global_config

global_config.verify_ssl = False
global_config.host = "https://localhost:2746"
global_config.token = ArgoCLITokenGenerator

@script(image="quay.io/containers/podman:v4.7.0", resources=Resources(cpu_request=0.5, memory_request="1Gi"))
def build_image():
    import subprocess
    print("build_image")
    
    subprocess.run(
        ["podman", "ls"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )

    subprocess.run(
        ["podman", "ls"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )    

@script()
def run_image():
    print("run_image")


with Workflow(generate_name="ci-", 
                entrypoint="ci-steps",
                service_account_name="hera",
                namespace="argo",
              ) as w:
    with Steps(name="ci-steps") as s:
        build_image()
        # run_image()

w.create()
       