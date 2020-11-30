import os

'''
THIS IS A SAMPLE SCRIPT TO BUILD THE DOCKER IMAGES AND PUSH THEM TO DOCKERHUB

TO BE RUN FROM root
  $$ python3 generate_push.py
'''

p   = ["dashboard", "estimator", "learner", "monitor", "predictor"]
tag = 1

for d in p :
    os.system(f"docker build -f docker/Dockerfile.{d} -t fellajimed/tweetoscope-python:{d}-{tag} .")
    os.system(f"docker push fellajimed/tweetoscope-python:{d}-{tag}")

c = ["generator", "collector"]

for d in c :
    os.system(f"docker build -f docker/Dockerfile.{d} -t fellajimed/tweetoscope-cpp:{d}-{tag} .")
    os.system(f"docker push fellajimed/tweetoscope-cpp:{d}-{tag}")