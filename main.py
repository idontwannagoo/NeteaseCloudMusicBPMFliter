import requests
import json



def get_list_data():


    url = "http://127.0.0.1:3000/playlist/detail?id="
    json_data = requests.get(url).text

    data = json.loads(json_data)

    songIdList = []
    for each in data['playlist']['trackIds']:
        songIdList.append(each['id'])
    print(songIdList)
    return songIdList

def get_songs_bpm():
    up_bpm = 91  # *2 = 182
    down_bpm = 89  # *2 = 178
    good_songs = []
    for each in get_list_data():
        url = "http://127.0.0.1:3000/song/detail?ids={}".format(str(each))
        url_baike = "http://127.0.0.1:3000/song/wiki/summary?id={}".format(str(each))
        # print(url)
        json_data = requests.get(url).text
        # print(json_data)
        data = json.loads(json_data)

        json_data_baike = requests.get(url_baike).text
        # print("    " + json_data_baike)
        data_baike = json.loads(json_data_baike)
        bpm = "0"
        for i in range(0, 6):
            try:
                if data_baike['data']['blocks'][1]['creatives'][i]['creativeType'] == "bpm":
                    bpm = data_baike['data']['blocks'][1]['creatives'][i]['uiElement']['textLinks'][0]['text']
            except IndexError:
                pass
        print(data['songs'][0]['name'] + " - " + data['songs'][0]['ar'][0]['name'] + " - " + bpm)


        if (down_bpm <= int(bpm) <= up_bpm) or (down_bpm * 2 <= int(bpm) <= up_bpm * 2):
            print("    " + "符合要求")
            good_songs.append(data['songs'][0]['name'] + " - " + data['songs'][0]['ar'][0]['name'])
            print(add_music_to_list(str(each), ""))

    print("符合要求的歌曲有：" + str(len(good_songs)) + "首")
    for each in good_songs:
        print(each)

def add_music_to_list(songId, playlistId):
    url = "http://127.0.0.1:3000/playlist/tracks?op=add&pid={}&tracks={}&cookie={}".format(playlistId, songId, "MUSIC_U=")
    return requests.get(url).text




get_songs_bpm()
