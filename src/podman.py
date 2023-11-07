from hera.auth import ArgoCLITokenGenerator
from hera.workflows import Steps, Step, Container, Workflow, script

from hera.shared import global_config

global_config.verify_ssl = False
global_config.host = "https://localhost:2746"
global_config.token = ArgoCLITokenGenerator

# @script(image="quay.io/containers/podman:v4.7.0", resources=Resources(cpu_request=0.5, memory_request="1Gi"))
@script()
def build_image():
    print("build_image")

    build = Container(
        name="build",
        image="quay.io/containers/podman:v4.7.0",
        command=["podman", "ls"],
    )
    

@script()
def run_image():
    print("run_image")


with Workflow(generate_name="ci-", 
                entrypoint="ci-steps",
                service_account_name="hera",
                namespace="argo",
              ) as w:
        pull_image = Container(
            name="pull",
            image="quay.io/containers/podman:v4.7.0",
            command=["sh", "-c"],
            args=[" echo 'FROM fedora:latest' >> Dockerfile "],
        )

        list_images = Container(
            name="list",
            image="quay.io/containers/podman:v4.7.0",
            command=["podman", "image"],
        )
        with Steps(name="ci-steps") as s:
            Step(name="pull", template=pull_image)
            Step(name="list", template=list_images)

w.create()
       