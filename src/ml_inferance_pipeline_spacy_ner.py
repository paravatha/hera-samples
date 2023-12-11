from hera.auth import ArgoCLITokenGenerator
from hera.shared import global_config

global_config.verify_ssl = False
global_config.host = "https://localhost:2746"
global_config.token = ArgoCLITokenGenerator


"""
This example showcases how to run ML pipeline prepare data and run spacy within Hera / Argo Workflows!

"""
from hera.workflows import Resources, script, Steps, Volume, Workflow, models as m

@script(image="jupyter/datascience-notebook:latest", 
        resources=Resources(cpu_request=0.5, memory_request="1Gi"),
        volume_mounts=[
        m.VolumeMount(name="data-dir", mount_path="/mnt/data")
    ],)
def data_prep() -> None:
    import subprocess
    print(subprocess.run("cd /mnt/data && ls -l &&  df -h", shell=True, capture_output=True).stdout.decode())
    print("Data preparation completed")

@script(image="jupyter/datascience-notebook:latest", 
        resources=Resources(cpu_request=0.5, memory_request="1Gi"),
        volume_mounts=[
        m.VolumeMount(name="data-dir", mount_path="/mnt/data")
    ],) 
def inferance_spacy() -> None:
    import random
    import subprocess
    import time

    # the used image does not have `spacy` or `pandas` installed, so we need to install it first!
    subprocess.run(["pip", "install", "spacy", "pandas"], stdout=subprocess.PIPE, universal_newlines=True,)
    
    import pandas as pd
    print(subprocess.run("cd /mnt/data && ls -l &&  df -h", shell=True, capture_output=True).stdout.decode())
    print("Training completed")

with Workflow(generate_name="ml-pipeline-xgb-", 
                entrypoint="ml-pipeline-xgb",
                volumes=[Volume(name="data-dir", size="1Gi", mount_path="/mnt/data")],
                service_account_name="hera",
                namespace="argo") as w:
    with Steps(name="ml-pipeline-xgb") as steps:
        data_prep(name="data-prep")
        inferance_spacy(name="inferance-spacy")

w.create()
