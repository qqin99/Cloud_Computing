from pyspark.ml.classification import RandomForestClassifier
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.linalg import Vectors
# from pyspark.ml.feature import StringIndexer

sc = SparkContext()
sqlContext = SQLContext(sc)


def predict(df_train, df_test):
    # TODO: Train random forest classifier

    # Hint: Column names in the given dataframes need to match the column names
    # expected by the random forest classifier `train` and `transform` functions.
    # Or you can alternatively specify which columns the `train` and `transform`
    # functions should use

    rf = RandomForestClassifier(numTrees=100, maxDepth=10, featuresCol="features", labelCol="label", seed=42)
    rf_model = rf.fit(df_train)
    predictions = rf_model.transform(df_test)
    # predictions.show()
    result = []
    for row in predictions.collect():
        result.append(row['prediction'])
    # Result: Result should be a list with the trained model's predictions
    # for all the test data points
    # print(result)
    return result


def parse_line(line):
    # TODO: Parse data from line into an RDD
    # Hint: Look at the data format and columns required by the KMeans fit and
    # transform functions
    line = line.split(',')
    label = int(line[-1])  # Parse label from line
    if len(line) > 1:
        features = line[:-1]  # Parse features from line
    else:
        features = []
    features = Vectors.dense(features)
    return [features, label]


def parse_feature(line):
    line = line.split(',')
    features = Vectors.dense(line)
    return [features]

def main():
    raw_training_data = sc.textFile("dataset/training.data")

    # TODO: Convert text file into an RDD which can be converted to a DataFrame
    # Hint: For types and format look at what the format required by the
    # `train` method for the random forest classifier
    # Hint 2: Look at the imports above
    rdd_train = raw_training_data.map(parse_line)
    # TODO: Create dataframe from the RDD
    df_train =sqlContext.createDataFrame(rdd_train, ['features','label'])
    # df_train.show()

    raw_test_data = sc.textFile("dataset/test-features.data")
    # TODO: Convert text file lines into an RDD we can use later
    test_rdd = raw_test_data.map(parse_feature)

    # TODO:Create dataframe from RDD
    df_test = sqlContext.createDataFrame(test_rdd, ['features'])

    predictions = predict(df_train, df_test)

    # You can take a look at dataset/test-labels.data to see if your
    # predictions were right
    for pred in predictions:
        print(int(pred))


if __name__ == "__main__":
    main()
