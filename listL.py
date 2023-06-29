class Node:
    def __init__(self, price, title, stock, vendor):
        self.price = price
        self.title = title
        self.stock = stock
        self.vendor = vendor
        self.nextval = None

    def __str__(self):
        print("$%-*s %-*s %-*s %-*s" % (10, str(self.price), 10, self.stock, 20, self.vendor, 0, self.title))
        return ''

class List:
    def __init__(self):
        self.headval = None

    def listprint(self):
        print("\n\n%-*s %-*s %-*s %-*s\n" % (10, "Price", 10, "Stock", 20, "Vendor", 0, "Title"))
        printval = self.headval
        while printval is not None:
            print (printval)
            printval = printval.nextval

    def insert(self, price, title, stock, vendor):
        new_node = Node(price, title, stock, vendor)

        # If the linked list is empty
        if self.headval is None:
            self.headval = new_node

        # If the price is smaller than the head
        elif self.headval.price >= new_node.price:
            new_node.nextval = self.headval
            self.headval = new_node

        else:
            # Locate the node before the insertion point
            current = self.headval
            while current.nextval and new_node.price > current.nextval.price:
                current = current.nextval

            # Insertion
            new_node.nextval = current.nextval
            current.nextval = new_node