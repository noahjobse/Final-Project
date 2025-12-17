import json
from engine import FulfillmentEngine
from models import Order, Warehouse

# Load sample data
with open('attempt1/sample_data.json', 'r') as file:
    data = json.load(file)
    # print(data)

    warehouses = [Warehouse(**warehouse) for warehouse in data['warehouses']]
    orders = [Order(**order) for order in data['orders']]


def main():
    # Validate orders in parallel
    engine = FulfillmentEngine()
    validation_results = engine.is_valid(orders, warehouses)
    
    # Print validation results
    print("\nParallel Validation Results:")
    for order, is_valid, warehouse in validation_results:
        if is_valid:
            print(f"Order {order.order_id}\tValid\tWarehouse {warehouse.warehouse_id}")
        else:
            print(f"Order {order.order_id}\tInvalid\tNo warehouse") 

    # Fulfill valid orders sequentially with lock
    engine.fulfill_orders(warehouses, validation_results)
    
if __name__ == "__main__":
    main()