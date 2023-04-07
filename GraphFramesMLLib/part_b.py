from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.clustering import KMeans
from pyspark.ml.linalg import Vectors
from collections import defaultdict
import pyspark.sql.functions as F

############################################
#### PLEASE USE THE GIVEN PARAMETERS     ###
#### FOR TRAINING YOUR KMEANS CLUSTERING ###
#### MODEL                               ###
############################################

NUM_CLUSTERS = 4
SEED = 0
MAX_ITERATIONS = 100
INITIALIZATION_MODE = "random"

sc = SparkContext()
sqlContext = SQLContext(sc)


def get_clusters(df, num_clusters, max_iterations, initialization_mode,
                 seed):
    # TODO:
    # Use the given data and the cluster pparameters to train a K-Means model
    # Find the cluster id corresponding to data point (a car)
    # Return a list of lists of the titles which belong to the same cluster
    # For example, if the output is [["Mercedes", "Audi"], ["Honda", "Hyundai"]]
    # Then "Mercedes" and "Audi" should have the same cluster id, and "Honda" and
    # "Hyundai" should have the same cluster id
    create_cluster = KMeans(k=num_clusters, maxIter=max_iterations, initMode=initialization_mode, seed=seed)
    # fit your kmeans model
    model = create_cluster.fit(df.select('features'))
    # transform your initial dataframe to include cluster assignments
    transformed = model.transform(df)
    # transformed.show()
    results = transformed.collect()
    # print(results)
    components = defaultdict(list)
    # use prediction as dictionary id, and car id as a list of values
    for row in results:
        components[row['prediction']].append(row['id'])

    to_return = []
    for key, value in components.items():
        to_return.append(value)

    return to_return


def parse_line(line):
    # TODO: Parse data from line into an RDD
    # Hint: Look at the data format and columns required by the KMeans fit and
    # transform functions
    line = line.split(',')
    car_brand = line[0]  # Parse src from line
    if len(line) > 1:
        features = line[1:]  # Parse dst_list from line
    else:
        features = []
    features = Vectors.dense(features)
    return [car_brand, features]


if __name__ == "__main__":
    f = sc.textFile("dataset/cars.data")

    rdd = f.map(parse_line)

    # TODO: Convert RDD into a dataframe
    dataframe = sqlContext.createDataFrame(rdd, ['id','features'])

    clusters = get_clusters(dataframe, NUM_CLUSTERS, MAX_ITERATIONS,
                            INITIALIZATION_MODE, SEED)
    for cluster in clusters:
        print(','.join(cluster))
