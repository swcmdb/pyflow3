BIN_NAME ?= pyflow3
VERSION ?= 0.1.0
IMAGE_NAME ?= $(BIN_NAME):$(VERSION)
DOCKER_ID_USER ?= swcmdb

docker: Dockerfile
	docker build --no-cache -t $(IMAGE_NAME) .

push:
	docker tag $(IMAGE_NAME) ${DOCKER_ID_USER}/$(BIN_NAME):$(VERSION)
	docker tag $(IMAGE_NAME) ${DOCKER_ID_USER}/$(BIN_NAME):latest
	docker push ${DOCKER_ID_USER}/$(BIN_NAME):$(VERSION)
	docker push ${DOCKER_ID_USER}/$(BIN_NAME):latest
