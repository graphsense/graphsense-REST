CASSANDRA_MARKER=.runcass
TAGSTORE_MARKER=.runts
CASSANDRA_MOCK=cassandra_mock
TAGSTORE_MOCK=tagstore_mock

test: $(MARKER)
	# start container if it's not running
	docker ps -a | grep $(CASSANDRA_MOCK) || bash -c 'rm -f $(CASSANDRA_MARKER) && make $(CASSANDRA_MARKER)'
	docker ps -a | grep $(TAGSTORE_MOCK) || bash -c 'rm -f $(TAGSTORE_MARKER) && make $(TAGSTORE_MARKER)'
	tox -e py37

$(CASSANDRA_MARKER): $(wildcard cassandra/data/*)
	./cassandra/start_mock.sh $(CASSANDRA_MOCK) "$?"
	touch $(CASSANDRA_MARKER)
	@ip=`docker exec $(CASSANDRA_MOCK) cat /etc/hosts | tail -n 1 | awk '{print $$1}'`;\
		echo "Cassandra mock container ip is $$ip"; \
		mkdir -p instance; \
		sed "s/CASSANDRA_MOCK_IP/$$ip/" ./config.yaml.tmp > ./instance/config.yaml

$(TAGSTORE_MARKER): $(wildcard tagstore/data/*)
	./tagstore/start_mock.sh $(TAGSTORE_MOCK) "$?"
	touch $(TAGSTORE_MARKER)
	@ip=`docker exec $(TAGSTORE_MOCK) cat /etc/hosts | tail -n 1 | awk '{print $$1}'`;\
		echo "Tagstore mock container ip is $$ip"; \
		sed -i "s/TAGSTORE_MOCK_IP/$$ip/" ./instance/config.yaml 

.PHONY: test
