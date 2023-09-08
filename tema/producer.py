"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        #initializare thread
        Thread.__init__(self, **kwargs)

        #initilizare produse
        self.products = products

        #initializare marketplace
        self.marketplace = marketplace
        
        #initializare wait_timer
        self.republish_wait_time = republish_wait_time

        #generare id unic produs
        self.product_id = marketplace.register_producer()

    def run(self):

        #infinite loop
        while True:
            for (product, n_products, wait_time) in self.products:
                #iteram in numarul de produse
                for _ in range(n_products):
                    #setam un flag de wait pe True
                    inner_flag = True
                    #asteptam cat timp trebuie pentru a putea publica
                    while inner_flag:
                        if self.marketplace.publish(self.product_id, product):
                            #exit flag
                            inner_flag = False
                        else:
                            time.sleep(self.republish_wait_time)
                        time.sleep(wait_time)
