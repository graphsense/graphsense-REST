# GraphSense REST Interface

The GraphSense REST Interface provides access to denormalized views computed by the [Graphsense
Transformation Pipeline][graphsense-transformation]. It is used by the
[graphsense-dashboard][graphsense-dashboard] component.

This component is implemented using the [Scala Play Framework][play-doc].

## Local Development Environment Setup

Follow the local development environment setup instructions described in the
[graphsense-transformation][graphsense-transformation] component.

Create an eclipse project file using `sbt`

    sbt eclipse

Import project into the Scala-IDE via
`File > Import... > Existing Projects into Workspace`

## Run REST interface locally

Create an application configuration file

	cp conf/application.conf.template conf/application.conf

...and configure `cassandra.host` and `cassandra.keyspace`. Example:

	cassandra.host = HOST (e.g., localhost)
	cassandra.keyspace = TRANSFORMED_KEYSPACE (e.g., graphsense_transformed) 

Start the server in development mode:

    sbt run

Test the service in your browser:

    http://localhost:9000/block/9000

In production mode `sbt stage` can be used (see the [Play documentation][play-doc]).

[graphsense-transformation]: https://github.com/graphsense/graphsense-transformation
[graphsense-dashboard]: https://github.com/graphsense/graphsense-dashboard
[play-doc]: https://www.playframework.com/documentation/2.6.x/Deploying
