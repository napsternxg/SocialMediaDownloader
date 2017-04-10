# Facebook downloader

## Usage
```bash
python fb_comments.py --help
usage: fb_comments.py [-h] [--credentials CREDENTIALS] --inputfile INPUTFILE
                      [--block-names BLOCK_NAMES] [--outdir OUTDIR]

Download facebook comments using ID.

optional arguments:
  -h, --help            show this help message and exit
  --credentials CREDENTIALS
                        Credentials file with the following lines:
                        access_token
  --inputfile INPUTFILE
                        Input file one comment id per line
  --block-names BLOCK_NAMES
                        Possible blocks in output data. Should be comma
                        seperated items with following values:
                        comments,reactions,likes
  --outdir OUTDIR       Directory to store output files.

```

**Example usage**
```bash
python fb_comments.py --credentials access_token.txt --inputfile post_ids.txt
```

## Get credentials
Get the access token from https://developers.facebook.com/tools/explorer/
