docker ps --all | awk {'print $1'} | xargs docker rm

docker images | grep none | awk {'print $3'} | xargs docker rmi

