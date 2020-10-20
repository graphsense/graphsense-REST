MARKER=.runtest
CASSANDRA_MOCK=cassandra_mock
testcmd=docker exec $(CASSANDRA_MOCK) cqlsh -e 'describe keyspaces'

$(MARKER): $(wildcard data/*)
	./make_cassandra_mock.sh $(CASSANDRA_MOCK)
	touch $(MARKER)

clean:
		rm $(MARKER)

test: $(MARKER)
	./start_cassandra_mock.sh $(CASSANDRA_MOCK)
	@ip=`docker exec $(CASSANDRA_MOCK) cat /etc/hosts | tail -n 1 | awk '{print $$1}'`;\
		echo "Cassandra mock container ip is $$ip"; \
		mkdir -p instance; \
		sed "s/CASSANDRA_MOCK_IP/$$ip/" ./config.py.tmp > ./instance/config.py
