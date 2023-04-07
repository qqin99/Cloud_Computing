from pyspark import SparkContext, SQLContext
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType, IntegerType

sc = SparkContext()
sqlContext = SQLContext(sc)

####
# 1. Setup (10 points): Download the gbook file and write a function to load it in an RDD & DataFrame
####
# Load a text file and convert each line to a Row.
lines = sc.textFile("gbooks")
parts = lines.map(lambda l: l.split("\t"))
books = parts.map(lambda p: (str(p[0]), int(p[1]), int(p[2]), int(p[3])))

# Spark SQL - DataFrame API
fields = [StructField('word', StringType(), True),
          StructField('count1', IntegerType(), True),
          StructField('count2', IntegerType(), True),
          StructField('count3', IntegerType(), True)]
schema = StructType(fields)

# Apply the schema to the RDD.
schemaBook = sqlContext.createDataFrame(books, schema)
# Register the DataFrame as a table.
schemaBook.registerTempTable("books")

####
# 5. Joining (10 points): The following program construct a new dataframe out of 'df' with a much smaller size.
####
df2 = schemaBook.select("word", "count1").distinct().limit(100);
df2.createOrReplaceTempView('gbooks2') # Register table name for SQL

# Now we are going to perform a JOIN operation on 'df2'. Do a self-join on 'df2' in lines with the same #'count1' values and see how many lines this JOIN could produce. Answer this question via DataFrame API and #Spark SQL API
# Spark SQL API
results = sqlContext.sql("SELECT g1.word AS word1, g2.word AS word2 FROM gbooks2 g1, gbooks2 g2 WHERE g1.count1 = g2.count1")
print(results.count())
# output: 218

