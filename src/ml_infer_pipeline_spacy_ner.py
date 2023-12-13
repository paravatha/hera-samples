from hera.auth import ArgoCLITokenGenerator
from hera.shared import global_config
from hera.workflows import Resources, script, Steps, Volume, Workflow, models as m

global_config.verify_ssl = False
global_config.host = "https://localhost:2746"
global_config.token = ArgoCLITokenGenerator

"""
This example showcases how to run ML pipeline prepare data and run spacy Named Entity Recognition (NER) model inference within Hera / Argo Workflows!
"""

@script(image="jupyter/datascience-notebook:latest", 
        resources=Resources(cpu_request=0.5, memory_request="1Gi"),
        volume_mounts=[
            m.VolumeMount(name="data-dir", mount_path="/mnt/data")
            ],
        )
def data_prep() -> None:
    import subprocess
    import spacy
    from spacy.lang.en.examples import sentences 
    import json

    print(subprocess.run("cd /mnt/data && ls -l", shell=True, capture_output=True).stdout.decode())
    # the used image does not have `spacy` installed, so we need to install it first!
    subprocess.run(["pip", "install", "spacy"], stdout=subprocess.PIPE, universal_newlines=True,)

    # dumping spacy example sentences data into a file
    # replace this with real dataset
    with open('/mnt/data/input_data.json', 'w') as json_file:
        json.dump(sentences, json_file) 
    print("Data preparation completed")
    print(subprocess.run("cd /mnt/data && ls -l", shell=True, capture_output=True).stdout.decode())


@script(image="jupyter/datascience-notebook:latest", 
        resources=Resources(cpu_request=0.5, memory_request="1Gi"),
        volume_mounts=[
            m.VolumeMount(name="data-dir", mount_path="/mnt/data")
            ],
        )
def inference_spacy() -> None:
    import subprocess

    # the used image does not have `spacy` installed, so we need to install it first!
    subprocess.run(["pip", "install", "spacy"], stdout=subprocess.PIPE, universal_newlines=True,)
    print(subprocess.run("cd /mnt/data && ls -l ", shell=True, capture_output=True).stdout.decode())
    import spacy
    import pydantic
    import json
    from typing import List

    # download and load spacy model https://spacy.io/models/en#en_core_web_lg 
    from spacy.cli import download
    spacy_model_name = 'en_core_web_lg'
    download(spacy_model_name)
    nlp = spacy.load(spacy_model_name)

    # build pydantic model
    print(pydantic.version.version_info())
    from pydantic import BaseModel
    class NEROutput(BaseModel):
        input_text: str
        ner_entities: List[str] = []

    ner_output_list : List[NEROutput] = []

    # read data prepared from previous step data_prep
    with open('/mnt/data/input_data.json', 'r') as json_file:
        input_data = json.load(json_file)
        print(input_data)
        # iterate each sentance in the data and perform NER 
        for sentence in input_data:
            print(f"input text: {sentence}")
            doc = nlp(sentence)    
            print(f"output NER:")
            ner_entities: List[str] = []
            for entity in doc.ents:    
                # Print the entity text and its NER label
                ner_entity = f"{entity.text} is {entity.label_}" 
                print(ner_entity)
                ner_entities.append(ner_entity)
            print(f"ner_entities = {ner_entities}")
            ner_output = NEROutput(input_text=sentence, ner_entities = ner_entities)
            ner_output_list.append(dict(ner_output))
        print(f"ner_output_list = {ner_output_list}")
    print("Inference completed")
    # save output in a file
    with open('/mnt/data/output_data.json', 'w') as json_file:
        json.dump(ner_output_list, json_file) 
    print(subprocess.run("cd /mnt/data && ls -l ", shell=True, capture_output=True).stdout.decode())

with Workflow(generate_name="ml-infer-pipeline-spacy-", 
                entrypoint="ml-infer-pipeline-spacy",
                volumes=[Volume(name="data-dir", size="1Gi", mount_path="/mnt/data")],
                service_account_name="hera",
                namespace="argo") as w:
    with Steps(name="ml-infer-pipeline-spacy") as steps:
        data_prep(name="data-prep")
        inference_spacy(name="inference-spacy")

w.create()
