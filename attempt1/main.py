import json
from engine import FulfillmentEngine
from models import Order, Warehouse

# Load sample data
with open('attempt1/sample_data.json', 'r') as file:
    data = json.load(file)
    # print(data)

#     warehouses = [Warehouse(**warehouse) for warehouse in data['warehouses']]
#     orders = [Order(**order) for order in data['orders']]

with open('database/orders.json', 'r') as orders_file:
    orders_data = json.load(orders_file)
    orders = [Order(**order) for order in orders_data]
with open('database/warehouses.json', 'r') as warehouses_file:
    warehouses_data = json.load(warehouses_file)
    warehouses = [Warehouse(**warehouse) for warehouse in warehouses_data]

def main():
    # Validate orders in parallel
    engine = FulfillmentEngine()
    validation_results = engine.is_valid(orders, warehouses)
    
    # Print validation results
    print("\nParallel Validation Results:")
    print("-" * 55)
    valid_status = "Invalid"
    processing_warehouse = "No warehouse"
    for order, is_valid, warehouse in validation_results:
        if is_valid:
            valid_status = "Valid"
            processing_warehouse = warehouse.warehouse_id
        
        print(f"Order: {order.order_id}\t{valid_status}\t{processing_warehouse}")

    # Fulfill valid orders sequentially with thread lock and second validation
    engine.fulfill_orders(warehouses, validation_results)
    
if __name__ == "__main__":
    main()
    

#idea for deducting inventory
def deduct_inventory(self, item_name, count):
    with self.lock:
        current = self.inventory.get(item_name, 0)
        if current < count:
            raise OutOfStockError("Not enough inventory")
        self.inventory[item_name] -= count