class FulfillmentError(Exception):
    """Base class for all exceptions in this project.
    inheriting from should let us catch all exceptions
    with one except block. (if we wanted to)
    """
    pass

class OutofStockError(FulfillmentError):
    """raised when a warehouse doesn't have enough stock 
    to fulfill an order.
    """
    print("Out of stock error raised")

class InvalidOrderError(FulfillmentError):
    """This is raised when an order asks for a product that isn't found in the catalog.""
    """
    pass
