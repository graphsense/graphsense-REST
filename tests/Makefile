MARKER=.runtest
CASSANDRA_MOCK=cassandra_mock
testcmd=docker exec $(CASSANDRA_MOCK) cqlsh -e 'describe keyspaces'

$(MARKER): $(wildcard data/*)
	./makeCassandraMock.sh
	touch $(MARKER)

test: $(MARKER)
	-docker run --name $(CASSANDRA_MOCK) -d cassandra || docker start $(CASSANDRA_MOCK)
	@ip=`docker exec $(CASSANDRA_MOCK) cat /etc/hosts | tail -n 1 | awk '{print $$1}'`;\
		echo "Cassandra mock container ip is $$ip"; \
		mkdir -p instance; \
		sed "s/CASSANDRA_MOCK_IP/$$ip/" ./config.py.tmp > ./instance/config.py
