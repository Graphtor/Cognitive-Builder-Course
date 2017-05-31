
import sys
import os
import json
import time
import pandas as pd
from watson_developer_cloud import DiscoveryV1
import argparse

# BEGIN of python-dotenv section
from os.path import join, dirname
from dotenv import load_dotenv
import os
# END of python-dotenv section


def read_json_file(file_path):
    """Reads and parse a json file.

    Parameters
    ----------
    file_path : {str} the path to the json file.

    Returns
    -------
    dict : a dictionary containing the json structure read from the file.
    """
    with open(file_path) as json_file:
        json_content = json_file.read()
        json_data = json.loads(json_content)

    return(json_data)


def display_results(response):
    """Reads and parse a json file.

    Parameters
    ----------
    file_path : {str} the path to the json file.

    Returns
    -------
    dict : a dictionary containing the json structure read from the file.
    """
    #print(json.dumps(response, indent=2))
    #print()
    print("*************RESULTS************")
    print()

    print('Total results retruned: ',response['matching_results'])
    print()
    print('************** Aggregations Results ******************')
    try:
        for agg_sums in response['aggregations'][0]['results']:
            #print (agg_sums)
            for key in agg_sums:
                print(key,':',agg_sums[key])
            print()
    except KeyError:
        print('NO RESULTS FOUND FOR AGGREGATIONS')
        print()



    #print (response.keys()) # --dict_keys(['matching_results', 'results'])
    #print (type(response['results'])) #dict
    if len(response['results']) < 20:
        print('********** TOP REVIEWS ************')
        for review in response['results']:
            print('Title: ',review['title']) # prints the name of the book reviewed
            try:
                print('Price: ',review['price'])
            except KeyError:
                print('Price: No Price Data')
            try:
                print('relivance score: ',review['score'])
            except KeyError:
                print('relivance score: no score data')
            print('* DocSentiment Data *')
            try:
                for k,v in review['enriched_text']['docSentiment'].items():
                    print(k,': ',v)
            except KeyError:
                print('no DocSentiment Data Available')
            print('REVIEW')
            try:
                print(review['text'])
            except KeyError:
                print('no review data available')
            print()
            print('****************************************')
    for i in range(10):
        print()

    # review_scores = []
    # for review in response['results']:
    #     review_score = {review['title'] : review['enriched_text']['docSentiment']['score']}
    #     review_scores.append(review_score)
    #     for i in review_scores:
    #         print(i)
    #         print()















if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query_file", help="path to the query file")
    args = parser.parse_args()

    # BEGIN of python-dotenv section
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    # END of python-dotenv section


    # opening query file specified as argument of script
    query_json = read_json_file(args.query_file)
    # connects to Discovery
    discovery = DiscoveryV1(
      username=os.environ.get("DISCOVERY_USERNAME"),
      password=os.environ.get("DISCOVERY_PASSWORD"),
      version="2016-12-01"
    )

    collection_id = os.environ.get('DISCOVERY_COLLECTION_ID')
    configuration_id = os.environ.get('DISCOVERY_CONFIGURATION_ID')
    environment_id = os.environ.get('DISCOVERY_ENVIRONMENT_ID')

    # sends the query to Discovery
    response = discovery.query(environment_id,
                               collection_id,
                               query_json)

    display_results(response)
