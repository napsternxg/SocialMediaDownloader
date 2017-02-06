## Tweet Downloaded

Create a file with all unique tweet ids (makes the download faster), one per line

Run the following command:
```
$PATH_TO_TWEETDOWNLOADER="<set path to folder>"
python "${PATH_TO_TWEETDOWNLOADER}/tweet_downloader_2.py" --credentials "${PATH_TO_TWEETDOWNLOADER}/cred.txt" --inputfile all_ids.txt --inputformat tsv --outputtype json > download.log 2>&1 &
```

`cred.txt` file should contain your authentication details
```
python "${PATH_TO_TWEETDOWNLOADER}/tweet_downloader_2.py" --help
```

Output will be saved in `all_ids.txt.json` if the output format is json
