import time

import requests
import os
import json

from django.conf import settings
from dotenv import load_dotenv
from django.utils.crypto import get_random_string
import pandas as pd

load_dotenv()
# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def get_user_id(user_screen_name):
    url = f"https://api.twitter.com/2/users/by/username/{user_screen_name}"
    response = requests.request("GET", url, auth=bearer_oauth)
    try:
        user_id = response.json()['data']['id']
    except KeyError:
        user_id = False
    # return response
    if user_id:
        return user_id
    else:
        return 0


def get_params(**kwargs):
    # tweet_fields = {"tweet.fields": "attachments, author_id, context_annotations, conversation_id, created_at, "
    #                                 "entities, geo, id, in_reply_to_user_id, lang, non_public_metrics, "
    #                                 "organic_metrics, possibly_sensitive, promoted_metrics, public_metrics, "
    #                                 "referenced_tweets, source, text, and withheld"}
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    # return {"tweet.fields": "created_at"}
    # attachments, author_id, context_annotations, conversation_id, created_at, entities, geo, id, in_reply_to_user_id,
    # lang, non_public_metrics, organic_metrics, possibly_sensitive, promoted_metrics, public_metrics,
    # referenced_tweets, reply_settings, source, text, withheld
    if len(kwargs) != 0:
        pagination_token = kwargs['pagination_token']
        return {"tweet.fields": "author_id,created_at,geo,id,public_metrics,text",
                "max_results": 100,
                "pagination_token": pagination_token}
    else:
        return {"tweet.fields": "author_id,created_at,geo,id,public_metrics,text",
                "max_results": 100}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def save_list_of_dicts_to_csv(list_of_dicts, output_address):
    new_list = []
    list_of_keys = list(list_of_dicts[0].keys())
    for item in list_of_dicts:
        temp_dict = {}
        for key in list_of_keys:
            if key != 'public_metrics':
                temp_dict.update({key: item[key]})
            else:
                for sub_key in list(item['public_metrics'].keys()):
                    temp_dict.update({sub_key: item['public_metrics'][sub_key]})
        new_list.append(temp_dict)

    columns = ['id', 'author_id', 'created_at', 'text', 'like_count', 'quote_count', 'reply_count', 'retweet_count']
    df = pd.DataFrame(new_list, columns=columns).rename(columns={'id': 'tweet_id'})
    df.to_csv(output_address, index=False)


def main(user_id, twitter_handle):
    data = []
    i = 1
    while len(data) < 700:
        time.sleep(1)
        if i == 1:
            params = get_params()
        else:
            params = get_params(pagination_token=pagination_token)
        url = f"https://api.twitter.com/2/users/{user_id}/tweets"
        json_response = connect_to_endpoint(url, params)
        data += json_response['data']
        try:
            pagination_token = json_response['meta']['next_token']
        except:
            break

    random_dir_name = get_random_string(length=32)
    staticfiles_path = os.path.join(settings.BASE_DIR, 'static')
    os.mkdir(os.path.join(staticfiles_path, random_dir_name))

    json_output_file_rel_address = os.path.join(random_dir_name, f'{twitter_handle}.json')
    csv_output_file_rel_address = os.path.join(random_dir_name, f'{twitter_handle}.csv')

    with open(os.path.join(staticfiles_path, json_output_file_rel_address), 'w') as f:
        json.dump(data, f)

    save_list_of_dicts_to_csv(data, os.path.join(staticfiles_path, csv_output_file_rel_address))

    return json_output_file_rel_address, csv_output_file_rel_address
