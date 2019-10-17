from app import app
from flask import Flask, request, jsonify, render_template
from config import BASE_DIR
from app.modules.ec_crawler.algo import pchome, umall, friday
from app.modules.ec_crawler.engine import crawler

crawler = crawler(pchome, umall, friday)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        q = request.args.get('q')
        sort = request.args.get('sort')

        if q == '':
            return '商品不能是空的！'

        num = 40
        if int(num)%20 == 0:
            prod_list = crawler.run(q, num)

            if sort == '1': # 低至高
                prod_list = sorted(prod_list, key=lambda k:int(k['prod_price']))
            elif sort == '2': # 高至低
                prod_list = sorted(prod_list, key=lambda k:int(k['prod_price']), reverse=True)
            
            return render_template('search.html', prod_list=prod_list)
    else:
        return '404'
        
