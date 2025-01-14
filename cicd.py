from fastapi import FastAPI, Request
import subprocess
import os
import json
from typing import Dict

app = FastAPI()

@app.post("/run")
def run():
    return "OK Rin CICD V. 0.0.1"


# Define the GitHub webhook endpoint
@app.post("/github-webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    # Make sure this is a push event
    if payload.get("ref") != "refs/heads/main":
        return {"message": "Not a main branch push event"}

    # The directory where the repository will be cloned or pulled
    repo_dir = "/root/P"

    # Pull the latest changes from the GitHub repo
    # git -C /root/MyProject pull
    pull_command = f"git -C {repo_dir} pull"
    pull_process = subprocess.Popen(pull_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = pull_process.communicate()

    if pull_process.returncode != 0:
        return {"message": "Failed to pull from GitHub", "error": stderr.decode()}

    # Rebuild the Docker container
    build_command = f"docker build -t my_app_image {repo_dir}"
    build_process = subprocess.Popen(build_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = build_process.communicate()

    if build_process.returncode != 0:
        return {"message": "Failed to build Docker image", "error": stderr.decode()}

    # Restart the Docker container with the new image
    restart_command = f"docker stop my_app_container && docker rm my_app_container"
    subprocess.run(restart_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    run_command = f"docker run -d --restart always --name my_app_container -p 80:80 my_app_image"
    subprocess.run(run_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return {"message": "GitHub webhook processed and Docker container updated successfully"}

