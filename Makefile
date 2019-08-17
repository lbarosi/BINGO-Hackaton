include ./make_env
#ifndef TAG
#$(error The TAG variable is missing.)
#endif
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
	@docker build -t $(IMAGE):$(TAG) -f Dockerfile .
	@make -s tag
	@make -s clean

tag:
	$(info Make: Tagging image with "$(TAG)".)
	@docker tag $(IMAGE):latest $(IMAGE):$(TAG)

jupyter:
	$(info Make: Starting "$(TAG)" tagged container.)
	@docker run --rm --mount type=bind,source=$(SOURCE),target=$(TARGET) $(IMAGE):$(TAG)

bash:
	$(info Make: Starting "$(TAG)" tagged container.)
	@docker run --rm --mount type=bind,source=$(SOURCE),target=$(TARGET) -ti $(IMAGE):$(TAG) /bin/bash

clean:
	@docker system prune --volumes --force

test:
	@echo $(FILTER)
