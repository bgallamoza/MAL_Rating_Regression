import requests
import pandas as pd
import time
import numpy as np

def get_anime_ranks(access_token: str, rank_type: str, limit: int, offset: int) -> dict:
    limit = str(limit)
    offset = str(offset)
    url = 'https://api.myanimelist.net/v2/anime/ranking'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'ranking_type':rank_type,
        'limit':limit,
        'offset':offset,
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    anime_ranks = response.json()
    response.close()

    print(f"GET anime/ranking request successful.")

    return anime_ranks

def get_anime_details(access_token: str, id: str, fields: list) -> dict:
    url = f'https://api.myanimelist.net/v2/anime/{id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    params = {
        'fields': ','.join(fields)
    }

    print(f"Sending GET request for anime ID:{id}.")
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    anime_details = response.json()
    response.close()

    print(f"GET anime ID:{id} details request successful.")

    return anime_details

def get_rank_df(access_token: str, intervals: int) -> pd.DataFrame:
    id_list = []
    title_list = []

    for offset in range(intervals):
        ranks = get_anime_ranks(access_token, 'tv', 500, 500*offset)

        for i in range(len(ranks['data'])):
            id_list.append(ranks['data'][i]['node']['id'])
            title_list.append(ranks['data'][i]['node']['title'])

    print(">>> Anime Ranking DataFrame successfully generated. <<<")
    return pd.DataFrame.from_dict({"id":id_list, "Title":title_list})

def get_details_df(access_token: str, id_list: list, fields: list) -> pd.DataFrame:
    df = pd.DataFrame(columns=fields)

    for row_id in id_list:
        row_data = {}
        details = get_anime_details(access_token, row_id, fields)
        for col in fields:
            try:
                row_data[col] = details[col]
            except:
                row_data[col] = np.nan
        df = df.append(row_data, ignore_index=True)
        time.sleep(1.5)
    
    print(">>> Anime Details DataFrame successfully generated. <<<")
    return df

def generate_df(access_token: str, intervals: int, fields: list, path: str):
    rank_df = get_rank_df(access_token, intervals)
    details_df = get_details_df(access_token, rank_df.id, fields)

    rank_df.to_csv(path + "anime_id.csv", index=False)
    details_df.to_csv(path + "anime_details.csv", index=False)

    rank_df.to_pickle(path + "anime_id.p")
    details_df.to_pickle(path + "anime_details.p")

    print(f">>> DataFrames successfully saved to \"{path}\" directory. <<<")