"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.name = kwargs['name']
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def print_products(self, temp):
        for product in temp:
            print (str(self.name) + " " + "bought" + " " +  str(product))

    def run(self):

        for cart in self.carts:
            #generez un id unic
            id_cart = self.marketplace.new_cart()

            #parcurg lista de operatii
            for prod in cart:
                i = 0
                #in cazul in care nu pot adauga in cos astept si incerc din nou
                while i < prod['quantity']:
                    #incrementez index-ul
                    i+=1
                    if prod['type'] != "add":
                        self.marketplace.remove_from_cart(id_cart, prod['product'])
                    else:
                        inner_flag = self.marketplace.add_to_cart(id_cart, prod['product'])
                        while not inner_flag:
                            inner_flag = self.marketplace.add_to_cart(id_cart, prod['product'])
                            time.sleep(self.retry_wait_time)

            final_list = self.marketplace.place_order(id_cart)
            self.print_products(final_list)
