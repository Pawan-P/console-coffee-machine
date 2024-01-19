import resources as Res

user_input = ""
is_off = False
storage = Res.resources
storage["bank"] = 0
items = ["espresso", "latte", "cappuccino"]


def print_resources(res):
    """Function to print available resources"""
    print(f'''
        Water: {res["water"]}ml
        Milk: {res["milk"]}ml
        Coffee: {res["coffee"]}g
        Money: ${res["bank"]}
    ''')


def check_resources(_choice):
    """Function to accept user choice and verify with available stock"""
    dct = {"flag": True, "message": ""}
    required = Res.menu[_choice]["ingredients"]
    for key in required:
        if required[key] > storage[key]:
            dct["flag"] = False
            dct["message"] = f"Sorry there is not enough {key}."
    return dct


def compare_prices(payment, choice):
    """Function to verify user payment to order cost if true deduct order cost from payment"""
    price_obj = {}
    cost = Res.menu[choice]["cost"]
    price_obj["fulfill"] = cost <= payment
    price_obj["change"] = payment - cost if payment > cost else 0.00
    if cost <= payment:
        storage["bank"] += cost
        order_process(choice)
    return price_obj


def order_process(choice):
    """Function to process order and manage product quantity"""
    ingredients = Res.menu[choice]["ingredients"]
    for item in ingredients:
        storage[item] -= ingredients[item]


while not is_off:
    user_input = input("What would you like? (espresso/latte/cappuccino):")
    if user_input == "off":
        is_off = user_input == "off"
        continue
    elif user_input == "report":
        print_resources(storage)
    else:
        if user_input not in items:
            print("Invalid Input!")
            continue
        dct = check_resources(user_input)
        if dct["flag"]:
            user_money = 0
            print("Insert coins")
            # Remember that quarters = $0.25, dimes = $0.10, nickles = $0.05, pennies = $0.01
            user_money += int(input("How many pennies?")) * 0.01
            user_money += int(input("How many nickles?")) * 0.05
            user_money += int(input("How many dimes?")) * 0.10
            user_money += int(input("How many quarters?")) * 0.25
            process_order = compare_prices(user_money, user_input)
            if not process_order["fulfill"]:
                print("Sorry that's not enough money. Money refunded.")
                continue
            if process_order["change"] > 0:
                print(f"Here is ${process_order["change"]} dollars in change.")
            print(f"Here is your {user_input}. Enjoy")
        else:
            print(dct["message"])
