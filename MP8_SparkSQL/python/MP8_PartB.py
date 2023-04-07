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
# 2. Counting (10 points): How many lines does the file contains? Answer this question via both RDD api & #Spark SQL
####

# Spark SQL 
# SQL can be run over DataFrames that have been registered as a table.
test = sqlContext.sql("SELECT COUNT(*) FROM books")
# The results of SQL queries are RDDs and support all the normal RDD operations.
test.show()

# +--------+                                                                              
# |count(1)|
# +--------+
# |86618505|
# +--------+


