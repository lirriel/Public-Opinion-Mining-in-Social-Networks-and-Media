import time
import json
from TikTokApi import TikTokApi

api = TikTokApi.get_instance(custom_verifyFp="TODO", use_test_endpoints=True)

results = 1000
used_tags = []
to_use_tags = ['feminism']
counter = 0
ids = []
data = []
banned = ['fyp', 'comedy', 'facts', 'viral', 'xyzbca', 'ukpolitics', 'politics', 'uspolitics', 'storytime', 'foryoupage',
          'losangelesteam', 'spokenword', 'poetry', 'joywithpret', 'justdancemoves', 'talent', 'performance', 'singing',
          'funny', 'trump', 'partone', 'boseallout', 'ihatecapitalism', 'commentary', 'fypシ', 'levitating', '26',
          'geicolipsync', 'trump2020', 'industry', 'prank', 'troll', 'invade', 'saraheverard', 'greysanatomy',
          'hadtobedone', 'zodiacsign', '2021affirmations', 'skincare101', 'xyra', 'loganpaul', 'paulbrothers', 'jakepaul',
          'sad', 'happy', 'harrystyles', 'onedirection', 'blowup', 'goviral', 'ahs', 'dariussimpson', 'scoutbostley',
          'discrimination', 'ally', 'blacktok', 'jdwonderland', 'tfbornthisway', 'tiktokk', 'leftist', 'washingtondcteam',
          'standa', 'unclefrank', 'sophialillis', 'paulbettany', 'primevideo', 'unclefrankapv', 'fail',
          'dopacsun', 'makeitmini', 'ourtype', 'nbadraft', 'holidaycountdown', 'whereilive', 'immuneupvapedown', '4u',
          'era', 'biden2020', 'resin', 'cc', 'egalitarian', 'xybzca', 'cfrzg', 'nbaisback', 'stitched', 'closedcaptions',
          'politicsltiktok', 'satire', 'lol', 'jokes', 'rhymepov', 'venom', 'brother', 'proud', 'doritosduetroulette',
          'pourtoi', '14septembre', 'wedding', 'bridal', 'husaspitfacts', 'tiktokcommentary', 'greenscreen', 'leafyclone',
          'mexico', 'acoso', 'isthisavailable', 'greenscreenscan', 'niceguysfinishlast', 'boost', 'sa', 'highschool',
          'school', 'boys', 'greenscreen', 'chores', 'clean', 'greenscreenvideo', 'blacktiktoker', 'acab', 'huh',
          'drafts', 'toxic', 'standup', 'standupcomedy', 'dope', 'overshareinyourunderwear', 'foryoupageee', 'poetryslam',
          'slampoetry', 'colorcustomizer', 'makeuproutine', 'saam', 'misandry', 'fyi', 'history']

filename='tiktoks.json'
while to_use_tags is not None and len(to_use_tags) > 0 and len(used_tags) < 10000:
    tag = to_use_tags[0]
    print(tag)
    try:
        trending = api.by_hashtag(hashtag=tag, count=1000, custom_verifyFp="")
        print(len(trending))
        for tiktok in trending:
            data.append(tiktok)
            if 'textExtra' in tiktok:
                tiktok_tags = list(filter(lambda t: len(t) > 0 and t is not None and t not in to_use_tags and t not in used_tags and t not in banned,
                                 map(lambda t: t['hashtagName'], tiktok['textExtra'])))
            else:
                tiktok_tags = []
            print(tiktok_tags)
            if len(tiktok_tags) > 0:
                to_use_tags.extend(tiktok_tags)
            ids.append(tiktok['id'])
        time.sleep(120)
        counter += 1
        to_use_tags.remove(tag)
        used_tags.append(tag)
        if len(data) % 50 == 0:
            with open(filename, 'w') as f:
                json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        print('caught exception while ' + tag)
        print(e)
        to_use_tags.remove(tag)
        used_tags.append(tag)

with open(filename, 'w') as f:
    json.dump(data, f, ensure_ascii=False)

print(len(set(ids)))
print(used_tags)
print(to_use_tags)
