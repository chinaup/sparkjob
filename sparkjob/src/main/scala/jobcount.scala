import org.apache.spark.sql.{Row, SparkSession}
import org.apache.spark.sql.types.{StringType, StructField, StructType}

object jobcount {

  def main(args: Array[String]): Unit = {

    val spark = SparkSession.builder()
      .appName("jobcount")
      .master("local")
      .getOrCreate()

    val sc = spark.sparkContext //使用SparkSession对象创建SparkContext

    val info = sc.textFile("file:///home/zhangbin/jobinfo.csv")
    val schemaString = "job company place money date"
    val fields = schemaString.split(" ").map(fieldName=>StructField(fieldName,StringType,nullable=true))
    val schema = StructType(fields)
    val row = info.map(_.split(",")).map(attributes=>Row(attributes(0),attributes(1),attributes(2),attributes(3),attributes(4)))
    val jobinfoDF = spark.createDataFrame(row,schema)
    jobinfoDF.createOrReplaceTempView("jobinfo")

    val results = spark.sql("select job from jobinfo")
    results.write.format("csv").save("file:///home/zhangbin/job.csv")
    val job = sc.textFile("file:///home/zhangbin/job.csv")
    val counts = job.map(job => (job,1)).reduceByKey((x,y) => x+y).filter{case(x,y) => y>10}//工作数目统计并过滤<10的工作
    counts.map(line=>{val word = line._1; val cnt  = line._2; word + " " +cnt}).saveAsTextFile("file:///home/zhangbin/jobcount.csv")//将键值对的小括号删除
  }
}
