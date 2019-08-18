include ./make_env
ifndef TAG
$(error The TAG variable is missing.)
endif
#TAG := v1
#SOURCE := /home/lbarosi/cosmos/
#TARGET := /home/cosmos/code/
#PORTS := 8888:8888
#FILTER := "until 24h"
#ACCOUNT := lbarosi
#SERVICE := cosmos

IMAGE := $(ACCOUNT)/$(SERVICE)


build:
	$(info Make: Building "$(TAG)" tagged images.)
	@docker build -t $(IMAGE):$(TAG) -f $(DOCKERFILE) .


tag:
	$(info Make: Tagging image with "$(TAG)".)
	@docker tag $(IMAGE):latest $(IMAGE):$(TAG)

run-jupyter:
	$(info Make: Starting "$(TAG)" tagged container with Jupyter. Open Browser)
	@docker run --name $(SERVICE) -p 8888:8888 --rm --mount type=bind,source=$(SOURCE),target=$(TARGET) $(IMAGE):$(TAG)

run-bash:
	$(info Make: Starting "$(TAG)" tagged container.)
	@docker run --name $(SERVICE) --rm --mount type=bind,source=$(SOURCE),target=$(TARGET) -ti $(IMAGE):$(TAG) /bin/bash

stop:
	$(info Make: Stopping "$(TAG)" tagged container.)
	@docker stop $(SERVICE)
	@docker rm $(SERVICE)

clean:
	@docker system prune --volumes --force

test:
	@echo $(FILTER)

push:
	$(info Make: Pushing "$(TAG)" tagged image.)
	@docker push $(IMAGE):$(TAG)
