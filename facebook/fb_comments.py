
# coding: utf-8

import pandas as pd
import requests

import json
import os


BASE_URL="https://graph.facebook.com/v2.8/"
QUERY_URL="{post_id}?fields=created_time,from,id,comments.limit({num_comments}){created_time,from,id,comment_count,like_count,message},likes{id,link,name,profile_type,pic_large},reactions{name,link,type,pic_large},source&summary=true"

def check_next(block):
    if "paging" not in block:
        return False
    if "next" not in block["paging"]:
        return False
    return True


class Post(object):
    block_names = ["comments", "likes", "reactions"]
    def __init__(self, post_id, access_token, out_dir, num_comments=100):
        self.post_id = post_id
        self.access_token = access_token
        self.out_dir=out_dir
        if not os.path.exists(self.out_dir):
            print(f"Output directory {self.out_dir} doesn't exist. Creating now.")
            os.makedirs(self.out_dir)
        final_query_url = QUERY_URL.format(post_id=post_id, num_comments=num_comments)
        self.base_query = f"{BASE_URL}/{final_query_url}&access_token={self.access_token}"
        
    def get_block_filename(self, block_name="base", suffix="json"):
        base_filename = f"{self.post_id}.{block_name}.{suffix}"
        filename = os.path.join(self.out_dir, base_filename)
        return filename

    def get_base_data(self):
        response = requests.get(self.base_query)
        print(response)
        data = response.json()
        self.base_data = data
        self.comments = data["comments"]["data"]
        self.likes = data["likes"]["data"]
        self.reactions = data["reactions"]["data"]
        filename = self.get_block_filename(block_name="base")
        with open(filename, "w+") as fp:
            json.dump(self.base_data, fp)
        
    def get_block_data(self, block_name="comments"):
        curr_block = self.base_data[block_name]
        block_data = getattr(self, block_name)
        print(f"fetching {block_name} block")
        while check_next(curr_block):
            response = requests.get(curr_block["paging"]["next"])
            curr_block = response.json()
            block_data.extend(curr_block["data"])
        
        print(f"Extracted {len(block_data)} {block_name} data")
        filename = self.get_block_filename(block_name)

        with open(filename, "w+") as fp:
            json.dump(block_data, fp)            
            
    def get_all_data(self):
        self.get_base_data()
        for block_name in Post.block_names:
            self.get_block_data(block_name=block_name)


    def comments_to_df(self):
        block_name = "comments"
        comments_file = self.get_block_filename(block_name)
        df = pd.read_json(comments_file, orient="records")
        print(df.shape)
        df = pd.concat([df, df["from"].apply(lambda x: pd.Series(x)).rename(columns={
            "id": "from_id",
            "name": "from_name",
        })], axis=1)
        print(df.shape)
        output_file = self.get_block_filename(block_name, suffix="txt")
        df.drop("from", axis=1).to_csv(output_file, sep="\t", index=False, encoding='utf-8')


def main(post_ids, access_token, block_names=("comments",), out_dir="./"):
    Post.block_names = list(block_names)
    params={
            "access_token": access_token,
            "out_dir": out_dir,
    }
    for post_id in post_ids:
        print(f"Processing data for: {post_id}")
        post_obj = Post(post_id, **params)
        post_obj.get_all_data()
        post_obj.comments_to_df()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = "Download facebook comments using ID.")
    parser.add_argument('--credentials', type=str, default="access_token.txt", help = '''\
            Credentials file with the following lines:
            access_token
        ''')
    parser.add_argument('--inputfile', type=str, required = True, help = 'Input file one comment id per line')
    parser.add_argument('--block-names', type=str, default="comments", help = '''
            Possible blocks in output data. Should be comma seperated items with following values:
            comments,reactions,likes
            ''')
    parser.add_argument('--outdir', type=str, default="./", help = 'Directory to store output files.')
    args = parser.parse_args()
    block_names = args.block_names.split(",")
    with open(args.inputfile) as fp:
        post_ids = set([pid.strip() for pid in fp.readlines()])

    """
    post_ids = ["10155506732127908", "10155860203081509", "10154403950906051", "10155855812666509", "10154885717379099",
            "10154162006545823", "1162040757216852"
            ]
    """
    access_token=""
    with open(args.credentials) as fp:
        access_token=fp.read().strip()


    main(post_ids, access_token, block_names, args.outdir)
