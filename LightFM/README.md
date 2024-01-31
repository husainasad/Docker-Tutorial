## Step 1: Create Custom Environment for Jupyter notebook
Use dockerfile to import jupyter notebook and to install python dependencies

## Step 2: Build Application Image
docker build -t {application image name} .

## Step 3: Create and Run Application Container
docker run --rm --name {application container name} -p 8888:8888 {application image name} <br/>
Can attach volume by adding the following parameter:  -v {absolute path to local directory}:/home/jovyan/ ({absolute path to docker container directory})

## Step 4: Work on Jupyter notebook
Use the URL to open jupyter notebook <br/>
Upload or make changes to the notebook

## Step 7: Stop container
docker stop {container name}

## Step 8: Cleanup if required
docker container prune <br/>
docker image prune -a <br/>
docker system prune -a <br/>
docker volume prune -a <br/>
docker builder prune -a