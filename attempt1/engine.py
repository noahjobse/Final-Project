from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from models import Product, Order, Warehouse

class FulfillmentEngine:
    def __init__(self):
        self.state = "initialized"
        # Thread lock for mutual exclusion during order fulfillment process
        self.lock = Lock()

    def start(self):
        self.state = "running"
        print("Fulfillment engine started.")

    def stop(self):
        self.state = "stopped"
        print("Fulfillment engine stopped.")

    def get_status(self):
        return self.state

    # Check if orders can be fulfilled from available warehouses, and return order, bool, warehouse
    def validate_order(self, order, warehouses):
        valid_warehouse = None

        for warehouse in warehouses:
            all_items_available = True

            for product in order.items:
                if not warehouse.in_inventory(product.product_id):
                    all_items_available = False
                    break

            if all_items_available:
                valid_warehouse = warehouse
                break

        # Tuple (order: Orderis_valid: bool, warehouse: Warehouse or None)
        return (order, valid_warehouse is not None, valid_warehouse)


    # Validate orders in parallel w/ ThreadPoolExecutor, and return list of results
    def is_valid(self, orders, warehouses):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.validate_order, order, warehouses) for order in orders]
            results = [future.result() for future in futures]
            # print(results)

        return results


    # Fulfill valid orders sequentially with thread lock
    def fulfill_orders(self,warehouses, validation_results):
        for order, is_valid, warehouse in validation_results:
            if is_valid:
                with self.lock:
                    print(f"\nFulfilling Order: {order.order_id}) from Warehouse: {warehouse.warehouse_id}...")
                    print("-" * 55)
                    
                    # Remove items from warehouse inventory after second validation
                    for order_product in order.items:
                        second_validation_result = self.validate_order(order, warehouses)
                        # Check if still valid before fulfilling
                        is_still_valid = second_validation_result[1]

                        if is_still_valid:
                            warehouse.remove_from_inventory(order_product.product_id, order_product.quantity)
                            print(f"Product:{order_product.product_id}\tRemoved Quantity: {order_product.quantity}")

                        else:
                            print(f"Product:{order_product.product_id}\tNot enough inventory to fulfill the order.")
        
