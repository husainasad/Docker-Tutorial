# Building Postgres Container
<br/>

## Using postgres
Command: docker pull postgres

## Running postgres container
Command: docker run -d --name {container name} -p 5432:5432 -e POSTGRES_PASSWORD=1234 postgres <br/>
-d flag specifies that the container should execute in the background.

## Get container ip address
Command: docker inspect -f "{{ .NetworkSettings.IPAddress }}" {containerNameOrId}<br/>
IP address is needed for connection <br/>

## Open shell within postgres container
Command: docker exec -it {container name} bash <br/>

## Build image from a Dockerfile
Command: docker build -t {your image name} . ({directory})

## Create and Run container from Docker image
Command: docker run {your image name} <br/>
-it flag runs the container in interactive mode and shows the output <br/>
--name flag lets you name the image/container
--rm flag removes the container as soon as it exits <br/><br/>

Command: docker run -v {absolute path to local directory}:/app/{absolute path to docker container directory} {image name} <br/>
-v flag adds volume to the container (can mount local directory to container directory and make changes without needing to rebuild) <br/>

## See container directory structure
Command: docker exec -it {container name} ls /app/ <br/>
Basically additional commands can be executed inside a running docker container through docker exec <br/>
use -u root for admin access