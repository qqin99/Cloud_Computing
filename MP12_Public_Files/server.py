from kubernetes import client, config
from flask import Flask,request
from os import path
import yaml, random, string, json
import sys
import json

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()
app = Flask(__name__)
# app.run(debug = True)

job_counter = 0

def create_job_object(dataset, nn_type):
    global job_counter
    env = [client.V1EnvVar(name="DATASET", value=dataset),
           client.V1EnvVar(name="TYPE", value=nn_type)]

    # Configureate Pod template container
    if nn_type == "cnn":
        container = client.V1Container(
            name=nn_type+str(job_counter),
            image="classification",
            env=env)
    else:
        container = client.V1Container(
            name=nn_type+str(job_counter),
            image="classification",
            env=env,
            resources=client.V1ResourceRequirements(limits={'cpu': '0.9'}))

    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))
    # Create the specification of deployment
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=4)
    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name="job"+str(job_counter)),
        spec=spec)
    return job


def create_job(api_instance, job, namespace):
    api_response = api_instance.create_namespaced_job(
        body=job,
        namespace=namespace)
    print("Job created. status='%s'" % str(api_response.status))
    
    
@app.route('/config', methods=['GET'])
def get_config():
    pods = []

    # your code here
    config.load_kube_config()
    print("Active host is %s" % configuration.Configuration().host)

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)

    for item in ret.items:
        print(
            "%s\t%s\t%s\t%s" %
            (item.status.pod_ip,
                item.metadata.namespace,
                item.metadata.name,
                item.status.phase))
        pod_list.append({'node': item.spec.node_name,
                         'ip': item.status.pod_ip,
                         "namespace": item.metadata.namespace,
                         "name": item.metadata.name,
                         "status": item.status.phase})

    output = {"pods": pods}
    output = json.dumps(output)

    return output

@app.route('/img-classification/free',methods=['POST'])
def post_free():
    # your code here
    global job_counter
    job_counter = job_counter + 1

    config.load_kube_config(context='free')
    batch_v1 = client.BatchV1Api()

    req_data = request.get_json(force=True)
    dataset = req_data['dataset']
    free_job = create_job_object(dataset, nn_type="ff")
    create_job(batch_v1, free_job, "free-service")
    return "success"


@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    # your code here
    global job_counter
    job_counter = job_counter + 1

    config.load_kube_config(context='premium')
    batch_v1 = client.BatchV1Api()

    req_data = request.get_json(force=True)
    dataset = req_data['dataset']
    premium_job = create_job_object(dataset, nn_type="cnn")
    create_job(batch_v1, premium_job, "default")
    return "success"

    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
