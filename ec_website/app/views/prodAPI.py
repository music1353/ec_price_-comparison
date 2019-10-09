from app import app
from flask import Flask, request, jsonify, render_template
from config import BASE_DIR
from app.modules.ec_crawler.algo import pchome, umall
from app.modules.ec_crawler.engine import crawler

crawler = crawler(pchome, umall)

@app.route('/api/prod')
def prodapi_get_prod():
    q = request.args.get('q')
    num = 20

    if int(num)%20 == 0:
        prod_list = crawler.run(q, num)
        return render_template('search.html', prod_list=prod_list)