MARKER=.runtest
CASSANDRA_MOCK=cassandra_mock
TAGSTORE_MOCK=tagstore_mock

test: $(MARKER)
	# start container if it's not running
	docker ps -a | grep $(CASSANDRA_MOCK) || docker ps -a | grep $(TAGSTORE_MOCK) || bash -c 'rm $(MARKER) && make .runtest'
	tox -e py37

$(MARKER): $(wildcard cassandra/data/*) $(wildcard tagstore/data/*)
	#./cassandra/start_mock.sh $(CASSANDRA_MOCK) "$?"
	./tagstore/start_mock.sh $(TAGSTORE_MOCK) "$?"
	touch $(MARKER)
	@ip=`docker exec $(CASSANDRA_MOCK) cat /etc/hosts | tail -n 1 | awk '{print $$1}'`;\
		echo "Cassandra mock container ip is $$ip"; \
		mkdir -p instance; \
		sed "s/CASSANDRA_MOCK_IP/$$ip/" ./config.yaml.tmp > ./instance/config.yaml
	@ip=`docker exec $(TAGSTORE_MOCK) cat /etc/hosts | tail -n 1 | awk '{print $$1}'`;\
		echo "Tagstore mock container ip is $$ip"; \
		sed -i "s/TAGSTORE_MOCK_IP/$$ip/" ./instance/config.yaml 

.PHONY: test
