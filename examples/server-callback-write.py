# Import the necessary modules
import asyncio
from asyncua import Server
# Import the DataChangeHandler class from the asyncua.common.subscription module
from asyncua.common.subscription import DataChangeHandler


# Define a callback function for data change event
def data_change_callback(node, val, data):
    # Print the node and the value
    print(f"Node {node} has value {val}")
    # Do something else with the node and the value, such as logging, updating a database, etc.

# Override the datachange_notification method
def datachange_notification(self, node, val, data):
    # Print the node and the value
    print(f"Node {node} has value {val}")
    # Do something else with the node and the value, such as logging, updating a database, etc.

# Define an async function for creating and running the server
async def main():
    # Create the server object
    server = Server()
    # Initialize the server
    await server.init()
    # Create an instance of the DataChangeHandler class
    handler = DataChangeHandler()

    # Set the endpoint and the name of the server
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_server_name("AsyncUA Test Server")
    # Get the root node of the server
    root = server.get_root_node()
    # Get the objects node of the server
    objects = server.get_objects_node()
    # Add a new node under the objects node
    myobj = await objects.add_object(3, "MyObject")
    # Add a new variable under the new node
    myvar = await myobj.add_variable(3, "MyVariable", 6.7)
    # Set the variable to be writable by clients
    await myvar.set_writable()
    # # Create a subscription object from the server object
    # sub = await server.create_subscription(1000, data_change_callback)
    # # Subscribe to data change event of the variable using the subscription object
    # handle = await sub.subscribe_data_change(myvar)

    # Create a subscription object from the server object using the handler instance
    sub = await server.create_subscription(1000, handler)
    # Subscribe to data change event of the variable using the subscription object
    handle = await sub.subscribe_data_change(myvar)

    # Start the server
    await server.start()
    # Keep the server running until interrupted by keyboard or signal
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass

# Run the async function using asyncio.run
if __name__ == "__main__":
    asyncio.run(main())
