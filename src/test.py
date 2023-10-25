import hera

from hera.workflows import DAG, Steps, Workflow, WorkflowsService, script
from hera.shared import global_config
global_config.host = "https://localhost:2746"
# Copy token value after "Bearer" from the `argo auth token` command
global_config.token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImVPQUtYVzFHR1l6dTBvLUtyUzNaYWJpRVowRnRCM0o0V3ZNdHk4LWdEd3MifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJhcmdvIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImhlcmEuc2VydmljZS1hY2NvdW50LXRva2VuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImhlcmEiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI5ZDE5YTk5NS1lZjJmLTRhOTctOGNiMi03NjFjZjhjZjMzYTUiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6YXJnbzpoZXJhIn0.cGMSCstc-IFDxTYoS60KhHdWC5bALXTxJSw-g4WKrBdEYCI4Q4dIE2MxIR1bnx5Kc3gveqZ6nwwN1SPtvny1QDAEiociqRXneuNjGk63Q6mTkaGB2f2f9KzhsoZP53-DNsdtAef1Lv2dnV-crxDZi3Uir15z6DGUocH22zq9YC3FNUimpdLpv3_3KLhUEPU2kt6dosYGlL8nih3NQxpHjwKBV1EQUJ6bwtebeW8_nwmG-cBhe1qOwa0cmbUPkCp8jpqwn8lZQMbt-sgOE8tCBcTFhrJJVKGP__7nQExsWmN2bVZeCSUeB3EOC8KhgD4mRI1y6ow8DgkOB1bpiJBOPA"  
# global_config.image = "<your-image-repository>/python:3.8"  # Set the image if you cannot access "python:3.8" via Docker Hub
global_config.verify_ssl = False

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
       