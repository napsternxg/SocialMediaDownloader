import requests
import json
import regex as re


WIKIDATA_SPARQL_ENDPOINT = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'

def download_data(query, data_format="json"):
    print "Downloading data from %s using query:\n%s\n\n" % (WIKIDATA_SPARQL_ENDPOINT, query)
    data = requests.get(WIKIDATA_SPARQL_ENDPOINT, params={'query': query, 'format': data_format})
    print "Downloaded %s records in %s format" % (len(data["results"]["bindings"]), data_format)
    return data

def get_query(queryfile):
    query = ""
    with open(queryfile) as fp:
        query = fp.read().strip()
    return query

def main(queryfile, outputfile, data_format="json"):
    query = get_query(queryfile)
    data = download_data(query, data_format)
    with open(outputfile, "wb+") as fp:
        fp.write(data)
    print "Written data to %s" % (outputfile)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Download data from wikidata sparql endpoint")
    parser.add_argument("--queryfile", help="query file path")
    parser.add_argument("--outputfile", default="wikidata_output.txt", help="output file path")
    parser.add_argument("--data-format", default="json", help="format can be either json or xml")

    args = parser.parse_args()
    main(args.queryfile, args.outputfile, args.data_format)





