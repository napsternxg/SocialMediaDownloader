"""
Description: 
    Download tweets using tweet ID, downloaded from https://noisy-text.github.io/files/tweet_downloader.py

Usage example (in linux):
    clear;python tweet_downloader.py --credentials ../data/credentials.txt --inputfile ../data/input.tids --outputtype IdTweetTok

Inputfile contains training/validation data whose first column is tweetID

credentials.txt stores the Twitter API keys and secrects in the following order:
consumer_key
consumer_secret
access_token
access_token_secret

Required Python library: 
    ujson, twython and twokenize (https://github.com/myleott/ark-twokenize-py)

An example output with whitespace tokenised text and tweet id in JSON format
    {"text":"@SupGirl whoaaaaa .... childhood flashback .","id_str":"470363741880463362"}
"""

try:
    import ujson as json
except ImportError:
    import json
import sys
import time
import argparse
from twython import Twython, TwythonError
from collections import OrderedDict

MAX_LOOKUP_NUMBER = 100
#SLEEP_TIME = 15 + 1
SLEEP_TIME = 5
PRINT_EVERY = 10000
twitter = None
arguments = None
tid_list = None


def get_creds(filename):
    credentials = []
    with open(filename) as fp:
        for l in fp:
            credentials.append(l.strip())
    twitter = Twython(credentials[0], credentials[1], credentials[2], credentials[3])
    return twitter


def parse_input_json(line):
    jobj = json.loads(line.strip())
    tid = jobj['tweet_id']
    return tid

def parse_input_tsv(line):
    tid = line.strip().split('\t')[0]
    return tid

def download(arguments, twitter):
    parse_input_line = parse_input_tsv
    if arguments.inputformat == "json":
        parse_input_line = parse_input_json

    with open(arguments.inputfile + "." + arguments.outputtype, "w") as fw:
        resume_id = None
        resumed_number = 0
        corrupted_lines = 0
        if arguments.resumefile is not None and arguments.resumefile != '':
            with open(arguments.resumefile) as fp:
                for l in fp:
                    try:
                        l = l.strip()
                        t = json.loads(l)
                    except ValueError:
                        corrupted_lines += 1
                        print "Skipping corrupt line [%s]:\n%s" % (corrupted_lines, l)
                        continue
                    resume_id = t["id_str"]
                    resumed_number += 1
                    if arguments.outputtype == "json":
                        fw.write(json.dumps(t))
                    else:
                        tweet = jobj["text"]
                        tid = jobj["id_str"]
                        dic_tweet = (('tweet_id', tid), ('text', tweet))
                        fw.write(json.dumps(OrderedDict(dic_tweet)))
                    fw.write("\n")
                print "Processing resumes after tid [%s corrupted lines]: %s" % (corrupted_lines, resume_id)
        resumed = False
        with open(arguments.inputfile) as fr:
            tid_number = 0
            tids = []
            for l in fr:
                #jobj = json.loads(l.strip())
                #tid = jobj['tweet_id']
                tid = parse_input_line(l)
                tid_number += 1
                if not resumed and resume_id is not None:
                    if tid == resume_id:
                        resumed = True
                        print "Resume file contains %d / %d tweets. Resuming after tweed id: %s" % (resumed_number, tid_number, tid)
                        continue
                    continue
                tids.append(tid)
                if len(tids) == MAX_LOOKUP_NUMBER:
                    jobjs = []
                    fetching = True
                    while(fetching):
                        try:
                            jobjs = twitter.lookup_status(id = tids)
                            fetching = False
                        except TwythonError:
                            print "Twitter error: sleeping for %s" % (SLEEP_TIME)
                            time.sleep(SLEEP_TIME)
                    ## Process downloaded tweets
                    for jobj in jobjs:
                        if arguments.outputtype == "json":
                            fw.write(json.dumps(jobj))
                        else:
                            tweet = jobj["text"]
                            tid = jobj["id_str"]
                            dic_tweet = (('tweet_id', tid), ('text', tweet))
                            fw.write(json.dumps(OrderedDict(dic_tweet)))
                        fw.write("\n")
                    tids = []
                    time.sleep(SLEEP_TIME)
                if tid_number % PRINT_EVERY == 0:
                    print "Downloaded %s tweets" % tid_number 

def main(arguments):
    twitter = get_creds(arguments.credentials)
    download(arguments, twitter)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "A simple tweet downloader for WNUT-NORM shared task.")
    parser.add_argument('--credentials', type=str, required = True, help = '''\
        Credential file which consists of four lines in the following order:
        consumer_key
        consumer_secret
        access_token
        access_token_secret
        ''')
    parser.add_argument('--inputfile', type=str, required = True, help = 'Input file one tweet id per line')
    parser.add_argument('--inputformat', type=str, default='tsv', choices = ['json', 'tsv'],
            help = '''Format of input:
            (1) json: json per line with key tweet_id corresponding to tweet id
            (2) tsv: headless tab seperated file with first column as tweet id
            ''')
    parser.add_argument('--resumefile', type=str, required = False, help = 'Resume file one tweet json per line')
    parser.add_argument('--outputtype', type=str, default='IdTweet', choices = ['json', 'IdTweet'], help = '''\
        Output data type:
        (1) json: raw JSON data from Twitter API;
        (2) IdTweet: tweet ID and raw tweet messages (default)
        ''')
    arguments = parser.parse_args()
    main(arguments)
