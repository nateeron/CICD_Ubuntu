import subprocess
import os
import json
from typing import Dict
from fastapi import FastAPI, Request, HTTPException
import logging
from urllib.parse import parse_qs
import uvicorn
import time
app = FastAPI()

@app.get("/run")
def run():
    return "OK Rin CICD V. 0.0.1"

p = "/root/bot/BotGrid2025-Deploy"
default_image_name = "bot-run-test-v1"
default_container_name = "bot-run-test-v1-container"
port = "80:45441"


logging.basicConfig(level=logging.INFO)

@app.post("/test")
async def github_webhooktest(request: Request):
    global p
    global default_image_name
    global default_container_name
    global port
    pull_command = f"git -C {p} pull"
    pull_process = subprocess.Popen(pull_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = pull_process.communicate()
    
    # Change to the /root/git directory
    os.chdir(p)
    
    print(f"docker ps --filter 'name={default_container_name}' -q")
    container_ID = subprocess.check_output(
            f"docker ps --filter 'name={default_container_name}' -q", shell=True, text=True
        ).strip()
    print(f"docker stop {container_ID}")
    os.system(f"docker stop {container_ID}")
    print(f"docker rm {container_ID}")
    os.system(f"docker rm {container_ID}")
    print(f"docker rmi {default_image_name}")
    os.system(f"docker rmi {default_image_name}")
    
    print(f"docker build -t {default_image_name} .")
    os.system(f"docker build -t {default_image_name} .")
    
    print(f"docker run -d --restart always -p {port} --name {default_container_name} {default_image_name}")
    os.system(f"docker run -d --restart always -p {port} --name {default_container_name} {default_image_name}")
    time.sleep(2)
    print("wait Log.....3")
    time.sleep(2)
    print("wait Log.....2")
    time.sleep(2)
    print("wait Log.....1")
    container_ID = subprocess.check_output(
            f"docker ps --filter 'name={default_container_name}' -q", shell=True, text=True
        ).strip()
    print(f"docker logs {container_ID}")
    os.system(f"docker logs {container_ID}")
    
    
@app.post("/github-webhook")
async def github_webhook(request: Request):
    global p
    global default_image_name
    global default_container_name
    global port
    try:
        # Get raw body and log it
        raw_body = await request.body()
        # logging.info(f"Raw body received: {raw_body.decode('utf-8')}")

        # Parse URL-encoded payload
        parsed_body = parse_qs(raw_body.decode("utf-8"))
        # if "payload" not in parsed_body:
        #     raise ValueError("Missing 'payload' in request body")
        print(parsed_body)
        # Decode JSON from the payload parameter
        payload = json.loads(parsed_body["payload"][0])
        # logging.info(f"Decoded JSON payload: {payload}")
        #print("************************************************************\n")
        clone_url = payload['repository']['clone_url']
        #print(f"Clone URL: {clone_url}")
        # commands ="git  pull origin master"
        # run_command(commands)
        
        pull_command = f"git -C {p} pull"
        pull_process = subprocess.Popen(pull_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = pull_process.communicate()
        
        # Change to the /root/git directory
        os.chdir(p)
        
        print(f"docker ps --filter 'name={default_container_name}' -q")
        container_ID = subprocess.check_output(
                f"docker ps --filter 'name={default_container_name}' -q", shell=True, text=True
            ).strip()
        print(f"docker stop {container_ID}")
        os.system(f"docker stop {container_ID}")
        print(f"docker rm {container_ID}")
        os.system(f"docker rm {container_ID}")
        print(f"docker rmi {default_image_name}")
        os.system(f"docker rmi {default_image_name}")
        
        print(f"docker build -t {default_image_name} .")
        os.system(f"docker build -t {default_image_name} .")
        
        print(f"docker run -d --restart always -p {port} --name {default_container_name} {default_image_name}")
        os.system(f"docker run -d --restart always -p {port} --name {default_container_name} {default_image_name}")
        time.sleep(2)
        print("wait Log.....3")
        time.sleep(2)
        print("wait Log.....2")
        time.sleep(2)
        print("wait Log.....1")
        container_ID = subprocess.check_output(
                f"docker ps --filter 'name={default_container_name}' -q", shell=True, text=True
            ).strip()
        print(f"docker logs {container_ID}")
        os.system(f"docker logs {container_ID}")
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")


# Define the GitHub webhook endpoint


  
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error occurred: {stderr.decode()}")
    else:
        print(stdout.decode())
@app.post("/gitClone")
async def gitClone(request: Request):
    global p
    payload = await request.json()
    print(payload)
   
    u = ""
    try: 
        p = payload["path"]
        u = payload["urlgit"]
    except Exception as e:
        print(e.message)
    #    
    #folder_path = 'root/P'
    ## Change to the directory P
    os.chdir(p)
#
    ## Initialize Git and run the necessary commands
    commands = [
        "git init",
        f"git remote add origin {u}",
        "git fetch origin",
        "git checkout -t origin/master",
        "git pull origin master"
    ]
#
    for command in commands:
        run_command(command)
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("cicd:app",host="0.0.0.0",  port=200, reload=1)