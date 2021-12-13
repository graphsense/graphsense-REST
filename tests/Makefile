MARKER=.runtest
CASSANDRA_MOCK=cassandra_mock

test: $(MARKER)
	# start container if it's not running
	docker ps -a | grep $(CASSANDRA_MOCK) || bash -c 'rm $(MARKER) && make .runtest'
	tox -e py37

$(MARKER): $(wildcard cassandra/data/*)
	./cassandra/start_cassandra_mock.sh $(CASSANDRA_MOCK) "$?"
	touch $(MARKER)
	@ip=`docker exec $(CASSANDRA_MOCK) cat /etc/hosts | tail -n 1 | awk '{print $$1}'`;\
		echo "Cassandra mock container ip is $$ip"; \
		mkdir -p instance; \
		sed "s/CASSANDRA_MOCK_IP/$$ip/" ./config.yaml.tmp > ./instance/config.yaml

.PHONY: test
