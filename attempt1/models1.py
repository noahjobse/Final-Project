from exceptions import OutofStockError

class Product:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

    # def remove_from_inventory(self, product_id, amount):
    #     if self.product_id == product_id:
    #         if self.quantity >= amount:
    #             self.quantity -= amount
    #             return True

class Order:
    def __init__(self, order_id, items, warehouse_id=None):
        self.order_id = order_id
        # Convert items dict to list of Product objects
        if isinstance(items, dict):
            self.items = [Product(product_id=pid, quantity=qty) for pid, qty in items.items()]
        else:
            self.items = items
        self.warehouse_id = warehouse_id

class Warehouse:
    def __init__(self, warehouse_id, inventory):
        self.warehouse_id = warehouse_id
        # Convert inventory dict to list of Product objects
        if isinstance(inventory, dict):
            self.inventory = [Product(product_id=pid, quantity=qty) for pid, qty in inventory.items()]
        else:
            self.inventory = inventory

    def in_inventory(self, product_id, order_quantity):
        
        for product in self.inventory:
            # print(product.product_id)
            if product.product_id == product_id:
                if product.quantity > order_quantity:
                    return True
        raise OutofStockError(f"Not enough inventory for product {product_id}")        
        return False
    
    def remove_from_inventory(self, order_product_id, order_quantity):
        # print(self.inventory)
        for product in self.inventory:
            if product.product_id == order_product_id:
                if product.quantity >= order_quantity:
                    product.quantity -= order_quantity
            return True
                # return product.remove_from_inventory(product_id, amount)
        return False
    
    # def remove_from_inventory(self, product_id, amount):
    #     pass
        # current = self.product_id
        # if current < amount:
        #     raise OutOfStockError(f"Not enough inventory")
        # self.inventory[product_id] = current - amount
