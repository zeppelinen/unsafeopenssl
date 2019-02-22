REGISTRY?=unsafeopenssl
VERSION=0.1
DOCKERFILES=$(shell find * -type f -name Dockerfile)
IMAGES=$(subst /,\-,$(subst /Dockerfile,,$(DOCKERFILES)))
TIMESTAMP=$(shell date +%Y-%m-%d_%H-%M-%S)


.PHONY: all

all: $(IMAGES)

debug: 
	echo $(IMAGES)

%:
	mkdir -p log
	docker build -t $(REGISTRY)/$@:$(VERSION) -f $(subst -,/,$@)/Dockerfile ../ > log/$@_build.log
	echo Copy packages to build directory
	mkdir -p ../packages/
	docker create --name $(REGISTRY)_$@_$(VERSION)-$(TIMESTAMP) $(REGISTRY)/$@:$(VERSION)
	docker cp $(REGISTRY)_$@_$(VERSION)-$(TIMESTAMP):/pkg /tmp/$(REGISTRY)_$@_$(VERSION)-$(TIMESTAMP)/
	mv -vf /tmp/$(REGISTRY)_$@_$(VERSION)-$(TIMESTAMP)/* ../packages/
	rm -rf /tmp/$(REGISTRY)_$@_$(VERSION)-$(TIMESTAMP)
	docker rm $(REGISTRY)_$@_$(VERSION)-$(TIMESTAMP)
	docker rmi $(REGISTRY)/$@:$(VERSION)
	echo Done
