#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from time import sleep
import requests
import json
import smtplib
from email.mime.text import MIMEText

SHOPEE_H = "https://shopee.tw/api/v2/search_items/?by=relevancy&keyword="
SHOPEE_T = "&limit=50&newest=0&order=desc&page_type=search"
PCHOME = "https://ecshweb.pchome.com.tw/search/v3.3/all/results?q="
HEADER = {'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 10895.56.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.95 Safari/537.36'}
IMG_HTTP_HEAD = "https://b.ecimg.tw"
SHOPEE_IMG_H = "https://cf.shopee.tw/file/"
PROD_URL = "https://24h.pchome.com.tw/prod"
SHOPEE_LINK = "https://shopee.tw/"

for_demo = False

def find_kw(target, kw_str):
    keywords = kw_str.split(" ")

    for kw in keywords:
        if target.find(kw) >= 0:
            return True

    return False

def notify(find_item_n, pre_price, cur_price, to_addrs):
    print ("Detected price changed (%s -> %s) of [%s]" % (pre_price, cur_price, find_item_n))
    print ("Sending email to notify ...")
    
    username = "jj1un0326@gmail.com"
    password = "xxx8520258"

    from_addr = "jj1un0326@gmail.com"

    msg = "\r".join([
          "From: jj1un0326@gmail.com",
          "To: %s" % to_addrs,
          "Subject: [%s] price updated" % find_item_n,
          "",
          "Find [%s] price updated: [%s] --> [%s]" % (find_item_n, pre_price, cur_price)
          ])

    #print msg

    #print isinstance(msg, unicode)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, msg)
    server.quit()

def read_data_from_file():
    fp = open("data.txt", "r")
    data = fp.read()
    fp.close()

    return data

def query_pchome(kw):
    url = PCHOME + kw
    try:
        if for_demo:
            print ("Querying production from local file ...")
            # Read data from disk
            res = read_data_from_file()
            data = json.loads(res)
        else:
            print ("Querying production from [%s] ..." % url)
            # Read data from PCHome
            res = requests.get(url, headers=HEADER)
            data = json.loads(res.text)
            fp = open("data.txt", "w")
            fp.write(res.text)
            fp.close()

    except Exception:
        return

    #for k, v in data.iteritems():
    #   print k

    for item in data["prods"]:
        item["picS"] = IMG_HTTP_HEAD + item["picS"]
        item["link"] = PROD_URL + "/" + item["Id"]

    return data["prods"]

def query_shapee(kw, acc_items):
    url = SHOPEE_H + kw + SHOPEE_T

    if for_demo:
        print ("Querying production from local file ...")
        # Read data from disk
        res = read_data_from_file()
        data = json.loads(res)
    else:
        print ("Querying production from [%s] ..." % url)
        # Read data from PCHome
        res = requests.get(url, headers=HEADER)
        data = json.loads(res.text)

        for item in data["items"]:
            print item
            shopee_result = {}
            shopee_result["name"] = item["name"]
            shopee_result["Id"] = str(item["itemid"])
            shopee_result["price"] = str(item["price"])
            shopee_result["picS"] = SHOPEE_IMG_H + item["image"] + "_tn"
            shopee_result["link"] = SHOPEE_LINK + item["name"] + "-i." + str(item["shopid"]) + "." + str(item["itemid"])
            acc_items.append(shopee_result)

    #for k, v in data.iteritems():
    #   print k

    return acc_items


def scrapy_key(kw, watch_price={}, email=None):
    result = "<table><tr><td>Product</td><td>Price</td><td>watch</td></tr>"

    items = query_pchome(kw)
    items = query_shapee(kw, items)

    searching_kw = kw.lower()
    not_detect = True
    for i in range(0, len(items)):
        #for k, v in items[i].iteritems():
        #   print k

        find_item_n = items[i]["name"].encode("utf-8")
        find_item_id = items[i]["Id"].encode("utf-8")
        item_price = items[i]["price"]
        link = items[i]["link"].encode("utf-8")
        pic_s = items[i]["picS"].encode("utf-8")

        if find_kw(find_item_n.lower(), searching_kw):
            result += "<tr><td>"
            result += "<img src='%s' width=128>" % pic_s
            result += "</td>"
            result += "<td><a href='%s' target=_blank>%s</a>" % (link, find_item_n)
            result += "<br><br>NT$ %s</td>" % item_price
            result += "<td align=center>"
            result += "<input type='checkbox' name='%s' value='%s'>" % (find_item_id, item_price)
            result += "</td></tr>"
            if find_item_id in watch_price.keys():
                print "compare [%s] -> [%s]" % (watch_price[find_item_id], item_price)
                if int(watch_price[find_item_id]) != int(item_price):
                    print "Detect price changed: %s -> %s" % (watch_price[find_item_id], item_price)
                    not_detect = False
                    notify(find_item_n, watch_price[find_item_id], item_price, email)
                    watch_price[find_item_id] = item_price

    if not_detect:
        print ("No price updated.")

    result += "</table>"
    result += "<input type='hidden' name='searched_kw' value='%s'>" % kw
    return result

def main():
    global for_demo
    parser = ArgumentParser()
    parser.add_argument("keyword", help="search keyword")
    parser.add_argument("--demo", dest='demo', help="for demo", default="false")
    args = parser.parse_args()
    
    if args.demo == "true":
        for_demo = True

    while True:
        scrapy_key(args.keyword)
        sleep(5)

if __name__ == "__main__":
    main()
