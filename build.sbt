ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.13.12"

lazy val root = (project in file("."))
  .settings(
    name := "Big Data Project",
    libraryDependencies += "org.apache.spark" %% "spark-streaming-kafka-0-10" % "3.5.0",
    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-core" % "3.3.2",
      "org.apache.spark" %% "spark-sql" % "3.3.2",
      "org.apache.spark" %% "spark-streaming" % "3.3.2",
      "org.apache.spark" %% "spark-sql-kafka-0-10" % "3.3.2",
      "org.elasticsearch" % "elasticsearch-spark-30_2.13" % "8.6.2",
      "org.apache.logging.log4j" % "log4j-core" % "2.20.0",
      "org.apache.logging.log4j" % "log4j-api" % "2.20.0",
      "org.apache.logging.log4j" % "log4j-1.2-api" % "2.20.0",
      "org.mongodb.spark" %% "mongo-spark-connector_2.13" % "10.1.1",
      "org.apache.spark" %% "spark-core" % "3.3.1",
      "org.apache.spark" %% "spark-sql" % "3.3.1"
  )
  )