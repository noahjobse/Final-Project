import json
from engine import FulfillmentEngine
from models1 import Order, Warehouse

def load_data():
    #Helper function to load data safely.
    
    #Load Orders
    with open('database/orders.json', 'r') as f:
        orders_data = json.load(f)
        # Assuming JSON keys match Order(order_id, items)
        orders = [Order(**order) for order in orders_data]

    # 2. Load Warehouses
    with open('database/warehouses.json', 'r') as f:
        warehouses_data = json.load(f)
        warehouses = []
        for w in warehouses_data:
            #Handle if JSON uses "id" but Class uses "warehouse_id"
            w_id = w.get('warehouse_id') or w.get('id')
            warehouses.append(Warehouse(warehouse_id=w_id, inventory=w['inventory']))

    return orders, warehouses

def main():
    #Load the data
    try:
        orders, warehouses = load_data()
        print(f"Loaded {len(orders)} orders and {len(warehouses)} warehouses.")
    except FileNotFoundError:
        print("Error: Could not find database files in 'database/' folder.")
        return
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Initialize Engine
    engine = FulfillmentEngine()

    #Validate orders in parallel
    print("\nValidating Orders...")
    validation_results = engine.is_valid(orders, warehouses)
    
    #Print  results
    print("\nParallel Validation Results:")
    print("-" * 60)
    print(f"{'Order ID':<15} {'Status':<10} {'Assigned Warehouse'}")
    print("-" * 60)

    for order, is_valid, warehouse in validation_results:
        #put status INSIDE the loop so it resets for every order
        if is_valid and warehouse:
            valid_status = "Success"
            given_warehouse = warehouse.warehouse_id
        else:
            valid_status = "Failed"
            given_warehouse = "None"
        
        print(f"{order.order_id:<15} {valid_status:<10} {given_warehouse}")

    #Fulfill valid orders sequentially
    print("\n" + "="*60)
    print("Fulfilling Orders! Please hold...")
    print("="*60)
    
    #assuming the engine.fulfill_orders method handles the loop and printing
    engine.fulfill_orders(warehouses, validation_results)
    
if __name__ == "__main__":
    main()