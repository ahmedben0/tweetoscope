import os

'''
THIS IS A SAMPLE SCRIPT TO BUILD THE DOCKER IMAGES AND PUSH THEM TO DOCKERHUB

TO BE RUN FROM root
  $$ python3 generate_push.py
'''


p   = ["dashboard", "estimator", "learner", "monitor", "predictor"]
tag_p = 3


os.system(f"docker build -f docker/Dockerfile.python-main -t fellajimed/tweetoscope-python:main-{tag_p} .")
os.system(f"docker push fellajimed/tweetoscope-python:main-{tag_p}")


for d in p :
    os.system(f"docker build -f docker/Dockerfile.{d} -t fellajimed/tweetoscope-python:{d}-{tag_p} .")
    os.system(f"docker push fellajimed/tweetoscope-python:{d}-{tag_p}")

c = ["generator", "collector"]
tag_c = 1
for d in c :
    os.system(f"docker build -f docker/Dockerfile.{d} -t fellajimed/tweetoscope-cpp:{d}-{tag_c} .")
    os.system(f"docker push fellajimed/tweetoscope-cpp:{d}-{tag_c}")