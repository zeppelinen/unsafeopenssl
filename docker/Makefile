REGISTRY?=unsafeopenssl
VERSION=0.1
DOCKERFILES=$(shell find * -type f -name Dockerfile)
IMAGES=$(subst /,\-,$(subst /Dockerfile,,$(DOCKERFILES)))
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)


.PHONY: all

all: $(IMAGES)

debug: 
	echo $(IMAGES)

%:
	docker build -t $(REGISTRY)/$@:$(VERSION) -f $(subst -,/,$@)/Dockerfile ../ > $@_build.log
	# -docker build -t $(REGISTRY)/$@ -f $(subst -,/,$@)/Dockerfile ../ 2>&1 | \
	# tee $@.log | sed -e 's/^/$@: /'
	echo Copy packages to build directory
	mkdir -p ../packages/
	docker create --name $(REGISTRY)_$@_$(VERSION)-$(TIMESTAMP) $(REGISTRY)/$@:$(VERSION)
	docker cp $(REGISTRY)_$@_$(VERSION)-$(TIMESTAMP):/pkg /tmp/$(REGISTRY)_$@_$(VERSION)/
	mv /tmp/$(REGISTRY)_$@_$(VERSION)/* ../packages/
	rm -rf /tmp/$(REGISTRY)_$@_$(VERSION)
	docker rm $(REGISTRY)_$@_$(VERSION)-$(TIMESTAMP)
	echo Done
