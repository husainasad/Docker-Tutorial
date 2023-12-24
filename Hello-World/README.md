## Build image from a Dockerfile
Command: docker build -t {your image name} . ({directory})

## Create a new container from Docker image
Command: docker create {your image name} <br/>

## Run an existing container from Docker image
Command: docker start {your container name} <br/>

## Create and Run container from Docker image
Command: docker run {your image name} <br/>
-it flag runs the container in interactive mode and shows the output <br/>
--rm flag removes the container as soon as it exits <br/><br/>

## See container logs
Command: docker logs {containername}