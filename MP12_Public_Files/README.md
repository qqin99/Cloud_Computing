# MP12_PublicFiles
## 1. Overview

Having developed one of the best image classification neural networks out there, it is now time to provide it as an online service and capture some market share. To do so, we set up and manage the infrastructure using Kubernetes and Docker containers over a cluster of nodes in this MP.

Essentially, you will start a web server interface for end-users to access machine learning services. When users send HTTP requests, your server is responsible for launching the corresponding ML jobs via Kubernetes. The autograder will act as an end-user, sending HTTP requests to your exposed server to grade the submissions.

## 2. Requirements

Note: Please use region -> us-east-1 for your deployment.

You need an AWS account with some free credit available and will work on EKS, EC2, Kubernetes, and Docker. AWS Educate accounts will not work as these accounts cannot create the network resources (EKS) needed for this assignment. Also, you need to be familiar with one of the following programming languages for implementing your server and interacting with Kubernetes: Python 3 / Javascript / Java / Go. 

We recommend completing this MP on an EC2 instance as you need to run a server that the autograder will try to access.
## 3. Procedure

## 3.1 AWS EKS / Kubernetes Setup

Prepare a host machine through which you will manage your EKS. Next, create a nodeGroup with two instances of type t2.medium (two vCPUs are required). You can do this by using an EC2 instance (t2.nano is enough). 

The following is an introduction to EKS, Amazon's Elastic Kubernetes Service.

https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html  

We highly recommend using eksctl with a YAML file to not configure the IAM roles and the VPC yourself.

https://eksctl.io/

Some other helpful resources: 

https://www.youtube.com/watch?v=p6xDCz00TxU

https://kubernetes.io/docs/reference/kubectl/cheatsheet/

```sh

apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata: 
    name: mp12-cluster 
    region: us-east-1
    
availabilityZones:
   - us-east-1a
   - us-east-1b

nodeGroups: 
  - name: ng-1 
    instanceType: t2.medium 
    desiredCapacity: 2
    privateNetworking: true
```

## 3.2 Containerization

We have provided the image classification neural network implementation with two versions - (classify.py). The first is a simple feed-forward neural network that you will use to market your product, providing it as a free service. The second is your premium service - a convolutional neural network. The provided implementation retrieves the dataset from the internet, trains the model, and then performs testing/classification on it. The 'DATASET' can be mnist or kmnist, and the 'TYPE' can be ff or cnn, both passed in using environment variables. Here, you only need to know how to run classify.py; not worry about its implementation. 

First, you have to dockerize the classification script to run it on your cluster. Install docker on the EKS EC2 instance and create a docker image. The environment variables can either be passed through the Dockerfile or later via Kubernetes. We have also provided requirements.txt, which specifies the python packages that your docker image needs. Once you have created the image, you should test that it works when you run it in a docker container. 

https://docs.docker.com/get-started/02_our_app/

The expected output of successfully running a docker container is similar to the following:
```sh
dataset: mnist
Downloading http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz to ./data/MNIST/raw/train-images-idx3-ubyte.gz
100.1%Extracting ./data/MNIST/raw/train-images-idx3-ubyte.gz to ./data/MNIST/raw
...
Processing...
Done!
Epoch [1/5], Step [100/600], Loss: 0.2846
Epoch [1/5], Step [200/600], Loss: 0.3859
Epoch [1/5], Step [300/600], Loss: 0.1448
...

```
Accuracy of the network on the 10K test images: 98 %

## 3.3 Deploying to cluster

Now that the container image is ready, it is time to deploy it to your Kubernetes server. First, you need to create a repository for your image on Docker Hub. Next, push your image to this repository so that worker nodes in Kubernetes can pull the image. You can refer to the following documentation:

https://docs.docker.com/docker-hub/repos/

https://docs.docker.com/engine/reference/commandline/push/

Note: if the EKS host is the same one you used to create the container image, you do not need to push it to the Docker hub. 

Then you need to create a configuration file and use the Kubernetes API to deploy it to the cluster nodes. Kubernetes will execute each job in its own pod. Since your python code runs to completion (and does not stay alive as a service), you will be using a “job” as the Kubernetes resource type. 

You can follow the official document of Kubernetes to learn how to deploy your job:

https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/  

Here is an example of how to set environment variables in a Kubernetes YAML file (note that you will not be using “kind: Pod” as described in the following guide. This is just an example of environment variables usage in YAML.)

https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/

You can also test your YAML file using the kubectl command-line interface or minikube on your machine. 

https://minikube.sigs.k8s.io/docs/start/

## 3.4 Resource Provisioning

As you will be hosting both free and premium services, you must provision your cluster appropriately to run the jobs. You do not want the free service to take up all the available hardware resources. To do so, you will provision at most two CPUs out of the total four (t2.medium has two cores) for your free service. We do this by using the Kubernetes namespace to create a virtual cluster. You can use a Resource Quota YAML file for the "free-service" namespace. 

https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/  

Each of the jobs should request and have a limit of 0.9 CPU. The same requirement applies to premium service as well. We want to ensure that at any time, only two free service pods are running (the other free service pods should be queued up). However, there can be any number of premium pods running. You must use a Job YAML to specify this resource limit. 

https://kubernetes.io/docs/concepts/workloads/controllers/job/

Premium service pods should execute under the "default" namespace and the free ones under the "free-service".

## 3.5 Exposing Image Classification

Now that the cluster is ready to use, you will build a server that accepts image classification requests and the necessary configurations from the autograder to verify your implementation. You will implement the server on the machine you used to set up the EKS, which has the Kubernetes configuration. We recommend running the server on an EC2 instance, not exposing your local network to the autograder. You can reuse the server code from MP2 if you like. However, the main part is programmatically interacting with Kubernetes, which you can achieve by using one of the following client libraries:

https://kubernetes.io/docs/reference/using-api/client-libraries/

The two APIs you will need are list_pod_for_all_namespaces() and create_namespaced_job().

You will be implementing the following API's:

### 1. Free Service - Create a container (job) with the feed-forward neural network within the free service namespace

- HTTP POST: /img-classification/free 

- BODY: {"dataset":"mnist"} (even though this looks like JSON string, the content type might not be application/json, so parse the request body accordingly)

- The response status code should be 200 if the job has been successfully created. Based on your namespace configuration, only two free service jobs should be running at a time.

### 2. Premium Service - Create a container (job) with the convolutional neural network within the default namespace

- HTTP POST: /img-classification/premium

- BODY: {"dataset":"kmnist"} (even though this looks like JSON string, the content type might not be application/json, so parse the request body accordingly)

- The response status code should be 200. You are hypothetically getting paid for this service. 

### 3. Configuration - Sends a snapshot of the current outlook of your Kubernetes cluster by returning information about all pods across all namespaces.

- HTTP GET: /config

- Response status code should be 200, and the body should be valid JSON. The body contains all the pods, including those created by  Kubernetes that are currently executing with some specifications. The following are the specifications:

- BODY: { "pods": [pod1, pod2 ...]}

    -- pods : a list of pods

    -- a pod:  {"node" : "node on which the pod is executing", "ip" : "ip address of the pod", "namespace" : "namespace of the node", "name" : "name of the pod", "status":"status of the pod"}
    
```sh
For example:
{
   "pods": [
      {
         "node": "ip-192-168-123-7.ec2.internal", 
         "ip": "192.168.125.2", 
         "namespace": "default", 
         "name": "mnist-deployment-6dc644dd6d-grpfd", 
         "status": "Succeeded"
      },
      {
         "node": "ip-192-168-123-7.ec2.internal", 
         "ip": "192.168.125.2", 
         "namespace": "default", 
         "name": "mnist-deployment-6dc644dd6d-grpfd", 
         "status": "Succeeded"
      } 
  ] 
}
```

The following are the object mappings for the python code (https://github.com/kubernetes-client/python)
```sh
{ 
"name": pod.metadata.name,
"ip": pod.status.pod_ip,
"namespace":pod.metadata.namespace,
"node":pod.spec.node_name, 
"status": pod.status.phase 
}
```

If your server is running correctly, you should be seeing three default pods and two free-service pods running. 

## 4. Autograder

Autograder does the following job (roughly) to test your submission:

- create a number of POST requests to /img-classification/free and check if jobs are successfully created by checking the HTTP response code == 200.

- create 1 GET request to /config and check if there are the correct number of free pods running

- create a number of POST requests to /img-classification/premium check if jobs are successfully created by checking the HTTP response code == 200.

- create 1 GET request to /config and check if there are  the correct number of free pods and premium pods running

- create 1 GET request to /config and check if the cluster is deployed properly (e.g., two nodes).

Tips:

Common mistake: use a constant job name in the YAML file so only one pod is created with multiple POST requests. 

Fix: Update metadata to use a new name in the python server code or  use generateName in YAML files. See: https://kubernetes.io/docs/reference/_print/#generated-values 

5. Final Result / Submission

Virtualization helped us effectively provision our hardware resources and achieve isolation between different executions. Moreover, we could easily deploy our neural network in any of our nodes without worrying about the environment, dependencies, etc.

Now that your service is ready, it is time to submit it to the autograder. Please ensure that you do not have any additional pods/jobs running other than the Kubernetes ones before submitting them. Add the necessary info in the payload section in the test.py file and execute the program. It takes about 20 seconds to run all of the test cases on your infrastructure. If all the test cases pass, you will see your grade on Coursera. 

Note: Please make sure that you delete all your old jobs in all namespaces before running test.py every time. 
