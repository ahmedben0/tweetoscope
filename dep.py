import os

'''
THIS IS A SIMPLE SCRIPT TO DEPLOY THE APP ON K8S

TO BE RUN FROM root
  $$ python3 dep.py
'''

os.system("kubectl delete -f K8s/deployment.yml")
os.system("kubectl delete -f K8s/zookeeper-and-kafka.yml")

os.system("kubectl apply -f K8s/zookeeper-and-kafka.yml")
os.system("kubectl apply -f K8s/deployment.yml")
