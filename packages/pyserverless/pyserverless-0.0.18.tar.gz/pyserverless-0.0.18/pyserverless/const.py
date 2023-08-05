import codefast as cf

class Const(object):
    redis = cf.mydb('/tmp/redis.db', max_len=100000, max_age_seconds=86400 * 120)
    bark = type(
        'bark', (object, ), {
            'host':
                cf.b64decode('aHR0cDovL2Rkb3QuZnVuOjgwODAvdGNpbWF2WTZvbUFTOWR6TDV6WlZtWi9TZXJ2ZXJBbGVydHMvCg=='),
            'icon': 'https://s3.bmp.ovh/imgs/2022/04/08/ceeadaf9afb375e3.jpeg'
        })
    nlp_list = "NLP_LIST"
    texts = type('texts', (object, ), {"sentence": "我楚天一一天不打工人民就不答应！"})

class const(Const):
    pass 

class numbers(object):
    pi:float = 3.1415926
    
    
    