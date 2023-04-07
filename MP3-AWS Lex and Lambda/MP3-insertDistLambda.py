from collections import deque
import json
import boto3
from collections import defaultdict

graph = "Chicago->Urbana,Urbana->Springfield,Chicago->Lafayette"


# parse the graph into a dictionary
def parse_graph(graph):
    trip_list = graph.split(",")
    locations = []
    for trip in trip_list:
        locations.append(trip.split("->"))
    graph_dict = defaultdict(list)

    for location in locations:
        graph_dict[location[0]].append(location[1])
    return graph_dict


# the dict record for each destination as key, the value is a list of shortest path
def find_shortest_path(graph, start, end):
    dist = {start: [start]}
    q = deque([start])

    while len(q):
        at = q.popleft()
        if at not in graph:
            continue
        for next in graph[at]:
            if next not in dist:
                dist[next] = dist[at] + [next]
                q.append(next)
    print(dist)
    return dist.get(end)


def calcDistance(graph, fromCity, toCity):
    shortest_path = find_shortest_path(graph, fromCity, toCity)
    if not shortest_path:
        return -1
    distance = shortest_path.index(toCity) - shortest_path.index(fromCity)
    return distance


def record_distance(graph):
    graph = parse_graph(graph)
    print(graph)

    destination_list = []
    for source in graph:
        for destination in graph[source]:
            destination_list.append(destination)
    for source in graph:
        for destination in destination_list:
            distance = calcDistance(graph, source, destination)
            print(source, destination, distance)


record_distance(graph)


# {"graph": "Chicago->Urbana,Urbana->Springfield,Chicago->Lafayette"}
def lambda_handler(event, context):
    # TODO implement
    # graph = event[graph]
    graph = parse_graph(event['graph'])

    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    table = dynamodb.Table('Distance')

    destination_list = []
    for source in graph:
        for destination in graph[source]:
            destination_list.append(destination)
    try:
        for source in graph:
            for destination in destination_list:
                distance = calcDistance(graph, source, destination)

                table.put_item(
                    Item={
                        'source': source,
                        'destination': destination,
                        'distance': str(distance)
                    }
                )
        return {
            'statusCode': 200,
            'body': json.dumps('Successful save the graph')
        }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('Not successf')
        }
