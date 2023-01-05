CASSANDRA_MARKER=.runcass
TAGSTORE_MARKER=.runts
TESTCONTAINER_MARKER=.runtestcontainer
CASSANDRA_MOCK=cassandra_mock
TAGSTORE_MOCK=tagstore_mock
USE_DOCKER=FALSE
DOCKER_GROUPID=999
ORGANIZATION=graphsense
TESTCONTAINER_NAME=graphsense-rest-test 

test: $(CASSANDRA_MARKER) $(TAGSTORE_MARKER)
	# start container if it's not running
	docker ps -a | grep $(CASSANDRA_MOCK) || bash -c 'rm -f $(CASSANDRA_MARKER) && make $(CASSANDRA_MARKER)'
	docker ps -a | grep $(TAGSTORE_MOCK) || bash -c 'rm -f $(TAGSTORE_MARKER) && make $(TAGSTORE_MARKER)'
ifeq ($(USE_DOCKER), TRUE)
	docker ps -a | grep $(TESTCONTAINER_NAME) || bash -c 'rm -f $(TESTCONTAINER_MARKER) && make $(TESTCONTAINER_MARKER)'
else
	tox -- $(ORGANIZATION)
endif

clean: 
	rm -f $(CASSANDRA_MARKER)
	rm -f $(TAGSTORE_MARKER)

$(CASSANDRA_MARKER): $(wildcard cassandra/data/*)
	./cassandra/start_mock.sh $(CASSANDRA_MOCK) $(ORGANIZATION) "$?"
	touch $(CASSANDRA_MARKER)
	make ips

$(TAGSTORE_MARKER): $(wildcard tagstore/data/*)
	./tagstore/start_mock.sh $(TAGSTORE_MOCK) $(ORGANIZATION) "$?"
	touch $(TAGSTORE_MARKER)
	make ips

$(TESTCONTAINER_MARKER): Dockerfile 
	docker build --build-arg USERID=$(UID) --build-arg DOCKER_GROUPID=$(DOCKER_GROUPID) -t $(TESTCONTAINER_NAME) .
	docker run --rm \
		--workdir /src \
		--name $(TESTCONTAINER_NAME) \
		-v ${PWD}/../:/src \
		--link $(CASSANDRA_MOCK):$(CASSANDRA_MOCK) \
		--link $(TAGSTORE_MOCK):$(TAGSTORE_MOCK) \
		-v /var/run/docker.sock:/var/run/docker.sock \
		--init \
		$(TESTCONTAINER_NAME) tox -e py37 -- $(ORGANIZATION)

ips:
	@ip=`docker exec $(CASSANDRA_MOCK) cat /etc/hosts | tail -n 1 | awk '{print $$1}'`;\
		echo "Cassandra mock container ip is $$ip"; \
		mkdir -p instance; \
		sed "s/CASSANDRA_MOCK_IP/$$ip/" ./config.yaml.tmp > ./instance/config.yaml
	@ip=`docker exec $(TAGSTORE_MOCK) cat /etc/hosts | tail -n 1 | awk '{print $$1}'`;\
		echo "Tagstore mock container ip is $$ip"; \
		sed -i "s/TAGSTORE_MOCK_IP/$$ip/" ./instance/config.yaml 


.PHONY: test ips clean
