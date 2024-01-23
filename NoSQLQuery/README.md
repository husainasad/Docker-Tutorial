## Step 1: Create and run docker container
docker run -p 8888:8888 jupyter/minimal-notebook<br>

## Step 2: Install application libraries
docker exec -u root -it {jupyter notebook container name} sudo apt-get update<br>
docker exec -u root -it {jupyter notebook container name} sudo apt-get install -y build-essential<br>
docker exec -it {jupyter notebook container name} pip install --no-cache-dir --upgrade pip<br>
docker exec -it {jupyter notebook container name} pip install --no-cache-dir unqlite<br>

## Step 3: Optimization
Step 1-2 can be combined<br>
### Create Custom Environment for Jupyter notebook in dockerfile

### Build Application Image
docker build -t {application image name} .

### Create and Run Application Container
docker run --rm --name {application container name} -v {absolute path to local directory}:/home/jovyan/ ({absolute path to docker container directory})-p 8888:8888 {application image name}

## Step 4: Work on Jupyter notebook
Use the URL to open jupyter notebook on web<br>

## Step 7: Stop container
docker stop {container name}<br>

## Step 8: Cleanup if required
docker container prune <br/>
docker image prune <br/>
docker system prune <br/>
docker volume prune <br/>
docker builder prune <br/>