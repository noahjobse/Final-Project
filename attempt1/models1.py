from exceptions import OutofStockError

class Product:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity
    
    #We don't need logic here anymore, the Warehouse handles it.
    def __repr__(self):
        return f"{self.product_id}: {self.quantity}"

class Order:
    def __init__(self, order_id, items, warehouse_id=None):
        self.order_id = order_id
        # Handles both dict inputs and list inputs safely
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

    def in_inventory(self, order_product):
        # for product in self.inventory:
        #     if product.product_id == product_id:
        #         return product.quantity > 0  
        #check specific quantity here
        #find the product object in the warehouse list
        product_in_stock = None
        for wp in self.inventory:
            if wp.product_id == order_product.product_id:
                product_in_stock = wp
                break
        # Check if it exists and has enough
        if not product_in_stock or product_in_stock.quantity < order_product.quantity:
            return True
        return False
    
    def remove_from_inventory(self, order_product_id, order_quantity):
        #Search for the product in the list
        for product in self.inventory:
            if product.product_id == order_product_id:
                
                #Check if we have enough
                if product.quantity >= order_quantity:
                    product.quantity -= order_quantity
                    return True # Success
                else:
                    #Found item, but not enough stock
                    raise OutofStockError(f"Warehouse {self.warehouse_id}: Not enough {order_product_id} (Requested: {order_quantity}, Have: {product.quantity})")
        
        #If loop finishes, we never found the item
        raise OutofStockError(f"Warehouse {self.warehouse_id}: Product {order_product_id} not found")