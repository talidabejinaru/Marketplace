"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        #mproducer este dictionarul pt producatori si produse
        #mconsumer este pt cosurile de cumparaturi si produse 
        #mid_removed_producer este dictionarul pentru a tine minte id producatorului pt produsele adaugate intr-un cos pentru a stii in caz de remove unde sa adaug produsul respectiv

        self.queue_size_per_producer = queue_size_per_producer
        self.mid_removed_producer = dict()
        
        #este pt cosurile de cumparaturi si produse 
        self.mconsumer = dict()
        #dictionarul pt producatori si produse
        self.mproducer = dict()

        self.lid_consumer = list(range(0, 2048))
        self.lid_producer = list(range(0, 2048))

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.lid_producer.remove(self.lid_producer[1])
        self.mproducer[str(self.lid_producer[1])] = []
        return str(self.lid_producer[1])

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        #produsul curent a atins limita de produse publicate
        if self.queue_size_per_producer < len(self.mproducer[producer_id]):
            return False

        #adaugarea produsului
        self.mproducer[producer_id].append(product)
        
        #succes
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.lid_consumer.remove(self.lid_consumer[1])
        self.mconsumer[int(self.lid_consumer[1])] = []
        return int(self.lid_consumer[1])

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        #inner_flag = False
        #return True
        for dict_idlist, dictprodlist in self.mproducer.items():
            if product in dictprodlist:
                dictprodlist.remove(product)
                self.mid_removed_producer[cart_id] = dict_idlist
                self.mconsumer[cart_id].append(product)
                return True
        return False


    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        if product in self.mconsumer[cart_id]:
            self.mconsumer[cart_id].remove(product)
            self.mproducer[self.mid_removed_producer[cart_id]].append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        temp = self.mconsumer[cart_id]
        return temp
