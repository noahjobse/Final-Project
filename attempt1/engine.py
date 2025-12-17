from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from models1 import Product, Order, Warehouse
from exceptions import OutofStockError
class FulfillmentEngine:
    def __init__(self):
        self.state = "initialized"
        self.lock = Lock()

    def start(self):
        self.state = "running"
        print("Fulfillment engine started.")

    def stop(self):
        self.state = "stopped"
        print("Fulfillment engine stopped.")

    def get_status(self):
        return self.state

    def validate_order(self, order, warehouses):
        valid_warehouse = None

        for warehouse in warehouses:
            all_items_available = True

            for product in order.items:
                #check specific quantity here
                #find the product object in the warehouse list
                product_in_stock = None
                for wp in warehouse.inventory:
                    if wp.product_id == product.product_id:
                        product_in_stock = wp
                        break
                
                # Check if it exists and has enough
                if not product_in_stock or product_in_stock.quantity < product.quantity:
                    all_items_available = False
                    break

            if all_items_available:
                valid_warehouse = warehouse
                break

        return (order, valid_warehouse is not None, valid_warehouse)

    def is_valid(self, orders, warehouses):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.validate_order, order, warehouses) for order in orders]
            results = [future.result() for future in futures]
        return results

    def fulfill_orders(self, warehouses, validation_results):
        for order, is_valid, warehouse in validation_results:
            if is_valid:
                with self.lock:
                    #We validate ONCE per order, not per item
                    #Because stock might have changed since the parallel check
                    recheck_order, recheck_valid, recheck_warehouse = self.validate_order(order, warehouses)
                    
                    if recheck_valid and recheck_warehouse.warehouse_id == warehouse.warehouse_id:
                        print(f"\nFulfilling Order: {order.order_id} from Warehouse: {warehouse.warehouse_id}...")
                        print("-" * 55)
                        
                        try:
                            #Deduct stock for all items
                            for order_product in order.items:
                                warehouse.remove_from_inventory(order_product.product_id, order_product.quantity)
                                print(f"Product: {order_product.product_id}\tRemoved Quantity: {order_product.quantity}")
                            
                            print(f"Order {order.order_id} Fulfilled Successfully.")

                        except OutofStockError as e:
                            print(f"there was an error fullfilling your order: {e}")
                    else:
                        print(f"\nSkipping Order {order.order_id}: Inventory changed, no longer valid.")