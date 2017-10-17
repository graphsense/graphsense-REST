# GraphSense REST Interface

A REST service for accessing data stored in Apache Cassandra.

## Prerequisites

This component connects to an existing Apache Cassandra installation.
Make sure Java 8 and [sbt][scala-sbt] are installed on your system.

## Setup and Installation

If needed, adapt the setting of `cassandra.host` in `conf/application.conf`
to point to a different Cassandra node.

Start the server in development mode:

    sbt run

Test the service in your browser:

    http://localhost:9000/block/9000

In production mode `sbt stage` can be used (see the [Play documentation][play-doc]).

[scala-sbt]: http://www.scala-sbt.org/
[play-doc]: https://www.playframework.com/documentation/2.6.x/Deploying
