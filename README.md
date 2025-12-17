# CMPP 3020 Final Project - Online Order Fulfillment Optimizer
### By: Noah, Umaya, Jazmin

## Overview
This system determines how customer orders are fulfilled by checking which available warehouses have enough inventory to process the orders.

## Model Classes
Product - the blueprint for each item in a warehouse's inventory, and the items in each order. Each product has an ID and quantity.

Order - stores the order_id and a list of items/products represented as Product objects

Warehouse - stores the warehouse_id and the inventory which is a list of Product objects. Checks if a product or ordered amount exists in inventory and removes product quantity from the inventory during order fulfillment.

## Engine
method is_valid(self, orders, warehouses) takes the list of orders and warehouse, and validates orders in parallel using the ThreadPoolExecutor class. Calls validate_order().

validate_order(self, order, warehouses) checks if the products in an order exist in any of the warehouses, and also checks if the requested quantity is available.

fulfill_orders(self, warehouses, validation_results) takes the valid orders and uses a thread lock to sequentially process the orders. Before fullfilling the order, it checks if the order is valid again because the stock will change due to previously processed orders

# main()
Reads the orders, products, and warehouses from the JSON files and stores them as lists. After going through all orders, it updates the warehouse's inventory.

