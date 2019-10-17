import requests
import json
import time

def pchome(q, name, num):
    '''
    Args:
        q (Queue): 存放演算法爬出的商品列表
        name (String): 商品名稱
        num (Int): 要爬的商品數量

    Result:
        把商品都存到q(Queue)
    '''

    # base
    PCHOME_PROD_LINK_URL = 'https://24h.pchome.com.tw/prod/'
    PCHOME_PIC_URL = 'https://d.ecimg.tw'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Connection': 'close'
    }
    
    # main
    for page_num in range(1, int(int(num)/20)+1):
        PCHOME_URL = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q='+ name +'&page='+ str(page_num) +'&sort=sale/dc'
        resp = requests.get(PCHOME_URL, headers=header)
        
        if resp.status_code == 200: # 如果請求成功，則去抓產品列表
            data = json.loads(resp.text)
            prods = data['prods']

            for item in prods: # 抓細項
                prod_id = item['Id']
                prod_name = item['name']
                prod_price = str(item['price'])
                prod_url = PCHOME_PROD_LINK_URL + prod_id
                prod_pic = PCHOME_PIC_URL + item['picS']

                obj = {
                    'from': 'pchome',
                    'id': prod_id,
                    'name': prod_name,
                    'prod_price': prod_price,
                    'url': prod_url,
                    'prod_pic': prod_pic
                }
                q.put(obj)

            time.sleep(0.5) 
        else:
            print('error')
            break


def umall(q, name, num):
    '''
    Args:
        q (Queue): 存放演算法爬出的商品列表
        name (String): 商品名稱
        num (Int): 要爬的商品數量

    Result:
        把商品都存到q(Queue)
    '''

    # base
    UMALL_URL = 'https://www.u-mall.com.tw/Search/Get'
    UMALL_PROD_LINK_URL = 'https://www.u-mall.com.tw/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Connection': 'close'
    }
    
    # main
    POST_HEADER = {
        'keyword': name,
        'model[cateName]': '全站',
        'model[pageSize]': int(num)
    }
    resp = requests.post(UMALL_URL, headers=header, data=POST_HEADER)
    
    if resp.status_code == 200:
        ori_data = json.loads(resp.text)
        data = ori_data['searchResult']['products']

        for item in data:
            prod_id = str(item['id'])
            prod_name = item['title']
            prod_price = item['finalPrice']
            prod_url = UMALL_PROD_LINK_URL + item['pageLink']
            prod_pic = 'https:' + item['imageUrl']

            obj = {
                'from': 'umall',
                'id': prod_id,
                'name': prod_name,
                'prod_price': prod_price,
                'url': prod_url,
                'prod_pic': prod_pic
            }
            q.put(obj)
    else:
        print('error')


def friday(q, name, num):
    '''
    Args:
        q (Queue): 存放演算法爬出的商品列表
        name (String): 商品名稱
        num (Int): 要爬的商品數量

    Result:
        把商品都存到q(Queue)
    '''

    # base
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Connection': 'close'
    }
    
    # main
    for page_num in range(1, int(int(num)/20)+1):
        FRIDAY_URL = 'https://mservice-event.shopping.friday.tw/api/v1/search?search='+ name + '&keyword='+ name +'&page='+ str(page_num)
        resp = requests.get(FRIDAY_URL, headers=header)
        
        if resp.status_code == 200: # 如果請求成功，則去抓產品列表
            data = json.loads(resp.text)
            prods = data['data']

            for item in prods: # 抓細項
                prod_id = item['pid']
                prod_name = item['name']
                prod_price = str(item['price'])
                prod_url = item['link']
                prod_pic = item['imgurl']

                obj = {
                    'from': 'friday',
                    'id': prod_id,
                    'name': prod_name,
                    'prod_price': prod_price,
                    'url': prod_url,
                    'prod_pic': prod_pic
                }
                q.put(obj)

            time.sleep(0.5) 
        else:
            print('error')
            break