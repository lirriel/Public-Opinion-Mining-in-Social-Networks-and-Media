import praw
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import time
from multiprocessing import Process, Pool
import pika

def get_comment_json(comment):
    comment_fields = ('body', 'created_utc', 'id', 'is_submitter', 'link_id', 'parent_id', 'score', 'subreddit_id')
    to_dict_comment = vars(comment)
    comment_dict = {field: to_dict_comment[field] for field in comment_fields}
    author = {}
    try:
        author['name'] = comment.author.name
        try:
            author['id'] = comment.author.id
        except Exception:
            r = 1
            # print(f'problems with {comment.author}')
        comment_dict['author'] = author
    except Exception as e:
        print(e)
    return comment_dict


def get_comments(submission):
    submission.comments.replace_more(limit=None)
    comments = []
    # print('Loading comments...')
    for top_level_comment in submission.comments:
        comment_dict = get_comment_json(top_level_comment)
        second_lvls = []
        for second_level_comment in top_level_comment.replies:
            second_level_comment_dict = get_comment_json(second_level_comment)
            thrd_lvls = []
            for third_level_comment in second_level_comment.replies:
                third_level_comment_dict = get_comment_json(third_level_comment)
                thrd_lvls.append(third_level_comment_dict)
            second_level_comment_dict['comments'] = thrd_lvls
            second_lvls.append(second_level_comment_dict)
        comment_dict['comments'] = second_lvls
        comments.append(comment_dict)
        # print(f'Uploaded comment {count}')
    return comments


def get_ts(dt):
    return time.mktime(dt.timetuple())


def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()


def getSubreddit(subreddit):
    reddit = praw.Reddit(client_id='client_id', \
                         client_secret='client_secret', \
                         user_agent='user_agent', \
                         username='username', \
                         password='passwordT')
    now_before_ts = str(int(get_ts(datetime.now())))
    after_ts = str(int(get_ts(datetime.today() - timedelta(days=6 * 365))))
    fields = ('title', 'id', 'selftext', 'url', 'score', 'created_utc', 'num_comments')

    list_of_items = []
    filename = subreddit + '.json'
    before_ts = now_before_ts
    min_dta = -1
    rec_count = 1000
    while rec_count == 1000:
        url = "https://api.pushshift.io/reddit/submission/search/?after=" + \
              after_ts + "&before=" + before_ts + "&" + \
              "sort_type=score&sort=desc&subreddit=" + subreddit + \
              "&limit=1000"
        print(url)
        r = requests.get(url=url)
        if r.status_code == 200:
            dta = r.json()
            ids = list(map(lambda t: t['id'], dta['data']))
            rec_count = len(ids)
            if rec_count > 0:
                count = 0
                print(f'Records: {rec_count}')
                min_dta = min(dta['data'], key=lambda x: int(x['created_utc']))['created_utc']
                before_ts = str(min_dta)
                print(f'Min data: {datetime.utcfromtimestamp(min_dta)}')
                for _id in ids:
                    submission = reddit.submission(id=_id)
                    print(f'comments: {submission.num_comments}')
                    to_dict = vars(submission)
                    sub_dict = {field: to_dict[field] for field in fields}
                    sub_dict['comments'] = get_comments(submission)
                    try:
                        sub_dict['author'] = submission.author.id
                    except Exception:
                        sub_dict['author'] = None
                    list_of_items.append(sub_dict)
                    count += 1
                    print(f'{subreddit}: count = {count}')
                    if count % 10 == 0:
                        print(count)
                        with open(filename, 'w') as f:
                            json.dump(list_of_items, f, ensure_ascii=False)

            with open(filename, 'w') as f:
                json.dump(list_of_items, f, ensure_ascii=False)
        print("\n")

if __name__ == '__main__':
    agents = 10
    chunksize = 1
    with Pool(processes=agents) as pool:

        parameters = pika.URLParameters('RMQ_LINK')
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue='NAME_OF_QUEUE', durable=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')


        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            time.sleep(body.count(b'.'))
            tag = body.decode("utf-8")
            print(f'running for {tag}')

            pool.map(getSubreddit, [tag], chunksize)

            print(" [x] Done")
            ch.basic_ack(delivery_tag=method.delivery_tag)


        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='NAME_OF_QUEUE', on_message_callback=callback, auto_ack=True)

        channel.start_consuming()

