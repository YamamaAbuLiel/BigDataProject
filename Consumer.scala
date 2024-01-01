import org.apache.log4j.BasicConfigurator
import org.apache.log4j.varia.NullAppender
import org.apache.spark.sql.{DataFrame, SparkSession, functions}

object Consumer {

  def main(args: Array[String]): Unit = {
    val nullAppender = new NullAppender
    BasicConfigurator.configure(nullAppender)


    val spark = SparkSession
      .builder
      .config("es.nodes", "127.0.0.1")
      .config("es.port", "9200")
      .master("local[8]")
      .appName("KafkaConsumerTweets")
      .getOrCreate()

    import spark.implicits._

    spark.conf.set("spark.sql.shuffle.partitions", 2)

    // Read from Kafka topic "tweets"
    val df = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "localhost:9092")
      .option("subscribe", "tweets")
      .load()


    val df1 = df.selectExpr("CAST(value AS STRING)")
      .select(functions.json_tuple($"value", "id", "date", "user", "text", "retweets"))
      .toDF("id", "date", "user", "text", "retweets")

    // Write the streaming DataFrame to MongoDB in append mode
    df1.writeStream
      .outputMode("append")
      .foreachBatch { (batchDF: DataFrame, batchId: Long) =>
        batchDF.write
          .format("mongodb")
          .option("uri", "mongodb://localhost:27017")
          .option("database", "twitterdb")
          .option("collection", "tweets")
          .mode("append")
          .save()
      }
      .start()
      .awaitTermination()
  }
}
