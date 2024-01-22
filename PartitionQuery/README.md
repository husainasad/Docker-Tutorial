## Step 1: Create and run postgres container
docker pull postgres <br>
docker run -d --name {container name} -p 5432:5432 -e POSTGRES_PASSWORD=1234 postgres<br>

## Step 2: Get IP address from postgres container
docker inspect -f "{{ .NetworkSettings.IPAddress }}" {containerName}<br/>

## Step 3: Replace IP adress in the application to make connection

## Step 4: Build application container
docker build -t {application image name} . ({directory})<br>

## Step 5: Create and run application image (attach volume for convenience)
docker run -v {absolute path to local directory}:/app/ ({absolute path to docker container directory}) {image name} <br/>

## Step 6: Run application python files inside the application container shell
docker exec -it {application container name} python /app/tester.py<br>

## Step 7: Stop application and postgres containers
docker stop {container name}<br>

## Step 8: Cleanup if required
docker container prune <br/>
docker image prune <br/>
docker system prune <br/>
docker volume prune <br/>
docker builder prune <br/>