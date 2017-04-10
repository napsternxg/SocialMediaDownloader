## Tweet Downloaded

```
$ python tweet_downloader.py --help
usage: tweet_downloader.py [-h] --credentials CREDENTIALS --inputfile
                           INPUTFILE [--inputformat {json,tsv}]
                           [--resumefile RESUMEFILE] [--outdir OUTDIR]
                           [--outputtype {json,IdTweet}]

A simple tweet downloader for WNUT-NORM shared task.

optional arguments:
  -h, --help            show this help message and exit
  --credentials CREDENTIALS
                        Credential file which consists of four lines in the
                        following order: consumer_key consumer_secret
                        access_token access_token_secret
  --inputfile INPUTFILE
                        Input file one tweet id per line
  --inputformat {json,tsv}
                        Format of input: (1) json: json per line with key
                        tweet_id corresponding to tweet id (2) tsv: headless
                        tab seperated file with first column as tweet id
  --resumefile RESUMEFILE
                        Resume file one tweet json per line
  --outdir OUTDIR       Output directory
  --outputtype {json,IdTweet}
                        Output data type: (1) json: raw JSON data from Twitter
                        API; (2) IdTweet: tweet ID and raw tweet messages
                        (default)

```

Create a file with all unique tweet ids (makes the download faster), one per line

Run the following command:
```
$PATH_TO_TWEETDOWNLOADER="<set path to folder>"
python "${PATH_TO_TWEETDOWNLOADER}/tweet_downloader.py" --credentials "${PATH_TO_TWEETDOWNLOADER}/cred.txt" --inputfile all_ids.txt --inputformat tsv --outputtype json > download.log 2>&1 &
```

`cred.txt` file should contain your authentication details
```
python "${PATH_TO_TWEETDOWNLOADER}/tweet_downloader.py" --help
```

Output will be saved in `all_ids.txt.json` if the output format is json
