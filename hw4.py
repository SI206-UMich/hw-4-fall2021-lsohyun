import unittest

# The Customer class
# The Customer class represents a customer who will order from the stalls.


class Customer:
    # Constructor
    def __init__(self, name, wallet=100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    def reload_money(self, deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases
    def validate_order(self, cashier, stall, item_name, quantity):
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):
            print("Our stall has run out of " + item_name +
                  " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity):
            print("Don't have enough money for that :( Please reload more money!")
        else:
            bill = cashier.place_order(stall, item_name, quantity)
            self.submit_order(cashier, stall, bill)

    # Submit_order takes a cashier, a stall and an amount as parameters,
    # it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    def submit_order(self, cashier, stall, amount):
        self.amount = amount
        self.wallet = self.wallet - amount
        cashier.receive_payment(stall, amount)

    # self.f2.submit_order(self.c1, self.s2, 30)

    # The __str__ method prints the customer's information.
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."


# The Cashier class
# The Cashier class represents a cashier at the market.
class Cashier:

    # Constructor
    def __init__(self, name, directory=[]):
        self.name = name
        self.directory = directory.copy()  # make a copy of the directory

    # Whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money

    # Places an order at the stall.
    # The cashier pays the stall the cost.
    # The stall processes the order
    # Function returns cost of the order, using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        return stall.compute_cost(quantity)

    # string function.
    def __str__(self):

        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

    ## Complete the Stall class here following the instructions in HW_4_instructions_rubric
class Stall:
    # A constructor (__init__) that initializes the instance variables name,
    # inventory, cost per food (default = 7), and earnings (default = 0).
    def __init__(self, name, inventory = {}, cost=7, earnings=0):
        self.name = name
        self.inventory = inventory
        self.cost = cost
        self.earnings = earnings

    # A process_order method that takes the food name and the quantity. If the stall has enough food,
    # it will decrease the quantity of that food in the inventory.
    # Questions for you to think about: should process_order take other actions? If so, add it in your code.
    def process_order(self, food_name, quantity):
        if self.inventory[food_name] >= quantity:
            self.inventory[food_name] -= quantity 

        #cashier = Cashier(self.name, self.inventory)
        #if cashier.has_stall(food_name):
        #    self.inventory[food_name] -= quantity

    # A has_item method that takes the food name and the quantity and
    # returns True if there is enough food left in the inventory
    # and False otherwise.

    def has_item(self, food_name, quantity):
        if food_name in self.inventory and quantity <= self.inventory[food_name]:
            return True
        else:
            return False

    # A stock_up method that takes the food name and the quantity.
    # It will add the quantity to the existing quantity if the item exists in the inventory dictionary
    # or create a new item in the inventory dictionary with the item name as the key and the quantity as the value.
    def stock_up(self, food_name, quantity):
        if food_name in self.inventory:
            self.inventory[food_name] += quantity
        else:
            self.inventory[food_name] = quantity

    # A compute_cost method that takes the quantity and returns the total for an order.
    # Since all the foods in one stall have the same cost, you only need to know the quantity of food items
    # that the customer has ordered.
    def compute_cost(self, quantity):
        return self.cost * quantity

    # A __str__ method that returns a string with the information in the instance variables using the format shown below:
    # Expected output for printing a stall object:
    # “Hello, we are [NAME]. This is the current menu [INVENTORY KEYS AS LIST].
    # We charge $[COST] per item. We have $[EARNINGS] in total.”
    def __str__(self):
        return '''
            Hello, we are {}. This is the current menu {}.
            We charge ${} per item. We have ${} in total."
        '''.format(self.name,
                   self.inventory.keys(),
                   self.cost,
                   self.earnings)


class TestAllMethods(unittest.TestCase):

    def setUp(self):
        inventory = {"Burger": 40, "Taco": 50}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Stall("The Grill Queen", inventory, cost=10)
        self.s2 = Stall("Tamale Train", inventory, cost=9)
        self.s3 = Stall("The Streatery", inventory)
        self.c1 = Cashier("West")
        self.c2 = Cashier("East")
        # the following codes show that the two cashiers have the same directory
        for c in [self.c1, self.c2]:
            for s in [self.s1, self.s2, self.s3]:
                c.add_stall(s)

        # Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

        # Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        # cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3)

        # Check to see whether constructors work
    def test_truck_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger": 40, "Taco": 50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

        # Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

        # Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})

    def test_make_payment(self):
        # Check to see how much money there is prior to a payment
        previous_custormer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings

        self.f2.submit_order(self.c1, self.s2, 30)

        # See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_custormer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)

        # Check to see that the server can serve from the different stalls

    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory=[self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1)) #boolian variable 
        self.assertFalse(c3.has_stall(self.s3))
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)

    # Test that computed cost works properly.
    def test_compute_cost(self):
        # what's wrong with the following statements?
        # can you correct them?
        # self.assertEqual(self.s1.compute_cost(self.s1, 5), 51)
        # self.assertEqual(self.s3.compute_cost(self.s3, 6), 45)
        self.assertEqual(self.s1.compute_cost(5), 50)
        self.assertEqual(self.s3.compute_cost(6), 42)

    # Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases

        # Test to see if has_item returns True when a stall has enough items left
        self.assertEqual(self.s1.has_item("Burger", 1), True)

        # Please follow the instructions below to create three different kinds of test cases
        # Test case 1: the stall does not have this food item:
        self.assertEqual(self.s2.has_item("Fries", 1), False)

        # Test case 2: the stall does not have enough food item:
        self.assertEqual(self.s1.has_item("Burger", 100), False)

        # Test case 3: the stall has the food item of the certain quantity:
        self.assertEqual(self.s2.has_item("Taco", 5), True)

    # Test Validate Order
    def test_validate_order(self):
        # case 1: test if a customer doesn't have enough money in their wallet to order
        self.assertEqual(self.f1.validate_order(self.c1, self.s3, "Burger", 4), None)

        # case 2: test if the stall doesn't have enough food left in stock
        self.assertEqual(self.s1.has_item("Burger", 400), False)
        
        # case 3: check if the cashier can order item from that stall
        self.assertEqual(self.c1.has_stall(self.s2), True)

    # Test if a customer can add money to their wallet
    def test_reload_money(self):
        # Reload 100 in f1 check if balance is 200
        self.f1.reload_money(100)
        self.assertEqual(self.f1.wallet, 200)

# Write main function


def main():
    # Create different objects
    # Create at least two inventory dictionaries with at least 3 different types of food.
    # The dictionary keys are the food items and the values are the quantity for each item.
    inventory1 = {"Chicken": 100, "Fish": 200, "Pork": 300}
    inventory2 = {"Potato": 10, "Tomato": 20, "Cucumber": 30}
    inventory3 = {"Banana": 5, "Berry": 10, "Peach": 15}

    # Create at least 3 Customer objects. Each should have a unique name and unique amount of money in their wallet.
    customer1 = Customer("Kanye", 250)
    customer2 = Customer("Cardi", 100)
    customer3 = Customer("Drake", 300)

    # Create at least 2 Stall objects. Each should have a unique name, inventory (use the inventory that you just created), and cost.
    stall1 = Stall("Spotify", inventory1, cost=5)
    stall2 = Stall("Apple", inventory2, cost=10)
    stall3 = Stall("Pandora", inventory3, cost=20)

    # Create at least 2 Cashier objects. Each should have a unique name and directory (a list of stalls).
    cashier1 = Cashier("Tim", [stall1, stall2])
    cashier2 = Cashier("Eric", [stall2, stall3])

    # Have each customer place at least one order (by calling validate_order)
    # and try all cases in the validate_order function above. See starter code for hints of all cases.
    # Try all cases in the validate_order function
    # Below you need to have *each customer instance* try the four cases

    # case 1: the cashier does not have the stall
    customer1.validate_order(cashier1, stall3, "Chicken", 5)
    customer2.validate_order(cashier2, stall1, "Fish", 10)
    customer3.validate_order(cashier1, stall3, "Pork", 15)

    # case 2: the casher has the stall, but not enough ordered food or the ordered food item
    customer1.validate_order(cashier2, stall3, "Banana", 20)
    customer2.validate_order(cashier1, stall1, "Potato", 20)
    customer3.validate_order(cashier1, stall2, "Chicken", 10)

    # case 3: the customer does not have enough money to pay for the order:
    customer1.validate_order(cashier1, stall1, "Chicken", 75)
    customer2.validate_order(cashier2, stall2, "Cucumber", 10)
    customer3.validate_order(cashier1, stall1, "Pork", 250)

    # case 4: the customer successfully places an order
    customer1.validate_order(cashier1, stall1, "Fish", 10)
    customer2.validate_order(cashier2, stall2, "Potato", 10)
    customer3.validate_order(cashier1, stall2, "Tomato", 10)

    
if __name__ == "__main__":
    main()
    print("\n")
    unittest.main(verbosity=2)
