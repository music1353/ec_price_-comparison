import queue
import threading

class crawler:
    def __init__(self, *crawler_algo):
        '''
        Args:
            *crawler_algo (func): 動態變數，傳入各ec平台的爬蟲演算法
        '''
        self.crawler_algo = crawler_algo # 存各ec的爬蟲演算法
    
    def show_algo(self):
        print(self.crawler_algo)

        
    def run(self, prod_name, data_num): # 執行多執行緒的爬蟲
        '''
            prod_name (String): 要爬蟲的商品名稱
            data_num (Int): 要爬的數量，一定要20的倍數 (總數量 = data_num * algo數)
        '''

        threads = []
        q = queue.Queue()
        
        for algo in self.crawler_algo:
            t = threading.Thread(target=algo, args=(q, prod_name, data_num))
            threads.append(t)
            
        for t in threads:
            print(t, 'thread start !')
            t.start()
            
        for t in threads:
            t.join()
        
        if not q.empty():
            result_prod_list = []

            while(not q.empty()):
                result_prod_list.append(q.get())
                
            return result_prod_list
        else:
            print('queue error')