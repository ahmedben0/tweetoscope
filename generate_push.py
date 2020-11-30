import os

'''
THIS IS A SAMPLE SCRIPT TO BUILD THE DOCKER IMAGES AND PUSH THEM TO DOCKERHUB

TO BE RUN FROM root
  $$ python3 generate_push.py
'''

p = ["dashboard", "estimator", "learner", "monitor", "predictor"]

for d in p :
    os.system(f"docker build -f docker/Dockerfile.{d} -t fellajimed/tweeto-{d}:latest .")
    os.system(f"docker push fellajimed/tweeto-{d}:latest")

c = ["generator", "collector"]

for d in c :
    os.system(f"docker build -f docker/Dockerfile.{d} -t fellajimed/tweeto-{d}:v3 .")
    os.system(f"docker push fellajimed/tweeto-{d}:v3")