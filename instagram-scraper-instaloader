import instaloader
import json

if __name__ == '__main__':
    tags = ['feminist', 'feminism', 'equality', 'girlpower', 'womenempowerment', 'women', 'love', 'feminista',
            'feminismo', 'lgbt', 'womensupportingwomen', 'lgbtq', 'blacklivesmatter', 'womensrights',
            'prochoice', 'woman', 'metoo', 'selflove', 'feministart', 'humanrights', 'empowerment',
            'intersectionalfeminism', 'genderequality', 'equalrights', 'femaleempowerment',
            'abortion', 'bhfyp', 'instafeminist', 'feminismisforeverybody', 'slutshaming', 'female',
            'mybodymychoice', 'textmewhenyougethome', 'protectwomen', 'stopharassment', 'saraheverard', 'metoo',
            'endingviolenceagainstwomen', 'shewaswalkinghome', 'itseveryonesproblem', 'endsexualassault',
            'BelieveWomen', 'WhyIDidntReport', 'WomensReality', 'TimesUp', 'MeAt14', 'NeverMoore', 'IAmANastyWoman',
            'ImWithHer', 'EverydaySexism', 'ToTheGirls', 'HeForShe', 'EffYourBeautyStandards', 'strongwomen',
            'girlpower', 'feministe', 'smashthepatriarchy', 'challengeaccepted', 'antifeminismpk', 'womeninbusiness',
            'girlsruntheworld', 'SheTransformsTech', 'FeministRealities', 'womenintechnology', 'womenintech',
            'internationalwomensday', 'womenhealingtheworld', 'WomenAccessToInternet', 'worldpulse', 'womenleaders',
            'TheFutureIsFemale', 'MenstrualEquity', 'MenstruationMatters', 'abortioncare', 'feministagenda',
            'yourbodyyourchoice', 'YoungFeminists']

    profiles = ['jameelajamilofficial', 'the_female_lead', 'chimamanda_adichie', 'cecilerichards', 'supermajority',
                'emmawatson', 'rachel.cargle', 'malala', 'blairimani', 'beyonce', 'kamalaharris', 'sadgirlsclub',
                'bodyposipand', 'feminist', 'astro_jessica', 'lesbianherstoryarchives', 'salty.world', 'fiercebymitu',
                'aoc', 'asiangirlsunite', 'feministvoice', 'feminist.herstory', 'freethenipple', 'wearehere',
                'crisistextline', 'themoodyactivist', 'thestoriesofwomen']


    L = instaloader.Instaloader(download_videos=False, download_pictures=False, download_video_thumbnails=False,
                                download_geotags=True, download_comments=True, save_metadata=False,
                                max_connection_attempts=30, request_timeout=5)

    L.login('LOGIN', 'PASSWORD')
    print(L.test_login())
    for p in profiles:
        print(p)
        counter = 0
        posts = []
        filename = 'instagram_' + p + '.json'
        posts_info = instaloader.Profile.from_username(L.context, p).get_posts()
        for post in posts_info:
            counter+=1
            print(counter)
            _comments = []
            comms = post.get_comments()
            for c in comms:
                _comment = {
                    'id': c.id,
                    'created_at_utc': c.created_at_utc.timestamp(),
                    'likes_count': c.likes_count,
                    'text': c.text
                }
                _comments.append(_comment)
            _post = {
                'user': p,
                'hashtags': post.caption_hashtags,
                'mentions': post.caption_mentions,
                'likes_count': post.likes,
                'text': post.caption,
                'created_at_utc': post.date_utc.timestamp(),
                'comments': _comments
            }
            posts.append(_post)
            with open(filename, 'w') as f:
                json.dump(posts, f, ensure_ascii=False)
