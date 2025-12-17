class Order:
    def __init__(self, order_id, items, warehouse_number):
        self.order_id = order_id
        self.items = items
        self.warehouse_number = warehouse_number
    
class Product:
    def __init__(self, product_id, name, quantity):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity

    def reduce_inventory(self, product_id, amount):
        if self.product_id == product_id:
            if self.quantity >= amount:
                self.quantity -= amount
                return True

class Warehouse:
    def __init__(self, warehouse_number, inventory):
        self.warehouse_number = warehouse_number
        self.inventory = inventory # inventory is a list of Product objects

    def check_inventory(self, product_id):
        for product in self.inventory:
            if product.product_id == product_id:
                if product.quantity > 0:
                    return True
        return False