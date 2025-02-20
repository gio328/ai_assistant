import json

ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499", "philippines": "$1300"}

# tool function
def get_ticket_price(destination_city):
    print(f"get_ticket_price tool called for Destination: {destination_city}")
    return ticket_prices.get(destination_city.lower(), "Unknown")


# There's a particular dictionary structure that's required to describe our function:
price_function = {
    "name": "get_ticket_price",
    "description": """Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, 
                    for example when a customer asks 'How much is a ticket to this city' """,
    "parameters": {
        "destination_city": {
            "type": "string",
            "description": "The city that the customer wants to travel to"
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

# And this is included in a list of tools:
tools = [{"type": "function", "function": price_function}]

def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get('destination_city')
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city,"price": price}),
        "tool_call_id": tool_call.id
    }
    return response, city

# ticket_price = get_ticket_price("philippines")
# print(f"Ticket price for Philippines: {ticket_price}")