from enum import Enum
import sys
from BurgerMachineExceptions import ExceededRemainingChoicesException, InvalidChoiceException, InvalidStageException, NeedsCleaningException, OutOfStockException
from BurgerMachineExceptions import InvalidPaymentException

class Usable:
    name = ""
    quantity = 0
    cost = 99

    def __init__(self, name, quantity = 10, cost=99):
        self.name = name
        self.quantity = quantity
        self.cost = cost

    def use(self):
        self.quantity -= 1
        if (self.quantity < 0):
            raise OutOfStockException
        return self.quantity 
#UCID: ac298 date: 03/25/23

    def in_stock(self):
        return self.quantity > 0
    def __repr__(self) -> str:
        return self.name

class Bun(Usable):
    pass

class Patty(Usable):
    pass

class Topping(Usable):
    pass

class STAGE(Enum):
    Bun = 1
    Patty = 2
    Toppings = 3
    Pay = 4

class BurgerMachine:
    # Constants https://realpython.com/python-constants/
    USES_UNTIL_CLEANING = 15
    MAX_PATTIES = 3
    MAX_TOPPINGS = 3


    buns = [Bun(name="No Bun", cost=0), Bun(name="White Burger Bun", cost=1), Bun("Wheat Burger Bun", cost=1.25),Bun("Lettuce Wrap", cost=1.5)]
    patties = [Patty(name="Turkey", quantity=2, cost=1), Patty(name="Veggie", quantity=10, cost=1), Patty(name="Beef", quantity=10, cost=1)]
    toppings = [Topping(name="Lettuce", quantity=10, cost=.25), Topping(name="Tomato", quantity=10, cost=.25), Topping(name="Pickles", quantity=10, cost=.25), \
    Topping(name="Cheese", quantity=10, cost=.25), Topping(name="Ketchup", quantity=10, cost=.25),
     Topping(name="Mayo", quantity=10, cost=.25), Topping(name="Mustard", quantity=10, cost=.25),Topping(name="BBQ", quantity=10, cost=.25)] 


    # variables
    remaining_uses = USES_UNTIL_CLEANING
    remaining_patties = MAX_PATTIES
    remaining_toppings = MAX_TOPPINGS
    total_sales = 0
    total_burgers = 0

    inprogress_burger = []
    currently_selecting = STAGE.Bun

    # rules
    # 1 - bun must be chosen first
    # 2 - can only use items if there's quantity remaining
    # 3 - patties can't exceed max
    # 4 - toppings can't exceed max
    # 5 - proper cost must be calculated and shown to the user
    # 6 - cleaning must be done after certain number of uses before any more burgers can be made
    # 7 - total sales should calculate properly based on cost calculation
    # 8 - total_burgers should increment properly after a payment
    

    def pick_bun(self, choice):
        if self.currently_selecting != STAGE.Bun:
            raise InvalidStageException
        for c in self.buns:
            if c.name.lower() == choice.lower():
                c.use()
                self.inprogress_burger.append(c)
                return
        raise InvalidChoiceException
#ucid: ac298   date: 03/25/23


    def pick_patty(self, choice):
        if self.currently_selecting != STAGE.Patty:
            raise InvalidStageException
        if self.remaining_uses <= 0:
            raise NeedsCleaningException
        if self.remaining_patties <= 0:
            raise ExceededRemainingChoicesException
        for f in self.patties:
            if f.name.lower() == choice.lower():
                f.use()
                self.inprogress_burger.append(f)
                self.remaining_patties -= 1
                self.remaining_uses -= 1
                return
        raise InvalidChoiceException
#ucid: ac298   date: 03/25/23

    def pick_toppings(self, choice):
        if self.currently_selecting != STAGE.Toppings:
            raise InvalidStageException
        if self.remaining_toppings <= 0:
            raise ExceededRemainingChoicesException
        for t in self.toppings:
            if t.name.lower() == choice.lower():
                t.use()
                self.inprogress_burger.append(t)
                self.remaining_toppings -= 1
                return
        raise InvalidChoiceException
#ucid: ac298   date: 03/25/23


    def reset(self):
        self.remaining_patties = self.MAX_PATTIES
        self.remaining_toppings = self.MAX_TOPPINGS
        self.inprogress_burger = []
        self.currently_selecting = STAGE.Bun
#ucid: ac298   date: 03/25/23

    def clean_machine(self):
        self.remaining_uses = self.USES_UNTIL_CLEANING
#ucid: ac298   date: 03/25/23
        
    def handle_bun(self, bun):
        self.pick_bun(bun)
        self.currently_selecting = STAGE.Patty
#ucid: ac298   date: 03/25/23

    def handle_patty(self, patty):
        if patty == "next":
            self.currently_selecting = STAGE.Toppings
        else:
            self.pick_patty(patty)
#ucid: ac298   date: 03/25/23

    def handle_toppings(self, toppings):
        if toppings == "done":
            self.currently_selecting = STAGE.Pay
        else:
            self.pick_toppings(toppings)
#ucid: ac298   date: 03/25/23

    def handle_pay(self, expected, total):
        # print(expected. total)
        if self.currently_selecting != STAGE.Pay:
            raise InvalidStageException
        if total == str(expected):
            print("Thank you! Enjoy your burger!")
            self.total_burgers += 1
            self.total_sales += expected # only if successful
            #print(f"Total sales so far {self.total_sales}")
            self.reset()
        else:
            raise InvalidPaymentException
#ucid: ac298   date: 03/25/23
        
    def print_current_burger(self):
        print(f"Current Burger: {','.join([x.name for x in self.inprogress_burger])}")
#ucid: ac298   date: 03/25/23


    def calculate_cost(self):
        cost = 0
        for component in self.inprogress_burger:
            cost += component.cost
        formatted_cost = "${:,.2f}".format(cost) # format cost as a currency
        print(f"The total cost of the burger is {formatted_cost}")
        return cost
#UCID: ac298  Date: 03/27/23
    
    def restart(self):
        self.inprogress_burger = []
        self.currently_selecting = STAGE.Bun
        print("Burger machine has been restarted")
#ucid: ac298   date: 03/25/23
        
    def run(self):
        try:
            if self.currently_selecting == STAGE.Bun:
                bun = input(f"What type of bun would you like {', '.join(list(map(lambda c:c.name.lower(), filter(lambda c: c.in_stock(), self.buns))))}?\n")
                self.handle_bun(bun)
                self.print_current_burger()
            elif self.currently_selecting == STAGE.Patty:
                patty = input(f"Would type of patty would you like {', '.join(list(map(lambda f:f.name.lower(), filter(lambda f: f.in_stock(), self.patties))))}? Or type next.\n")
                self.handle_patty(patty)
                self.print_current_burger()
            elif self.currently_selecting == STAGE.Toppings:
                toppings = input(f"What topping would you like {', '.join(list(map(lambda t:t.name.lower(), filter(lambda t: t.in_stock(), self.toppings))))}? Or type done.\n")
                self.handle_toppings(toppings)
                self.print_current_burger()
            elif self.currently_selecting == STAGE.Pay:
                expected = self.calculate_cost()
                # show expected value as currency format
                # require total to be entered as currency format
                total = input(f"Your total is ${expected}, please enter the exact value.\n")
                self.handle_pay(expected, total)                
                choice = input("What would you like to do? (order or quit)\n")
                if choice == "quit":
                    #exit() in recursive functions creates stackoverflow
                    # use return 1 to exit
                    print("Quitting the burger machine")
                    return 1
        except KeyboardInterrupt:
            # quit
            print("Quitting the burger machine")
            sys.exit()
        # handle OutOfStockException
        except OutOfStockException:
            print(f"{str(self.currently_selecting)[6:]}: Out of Stock")
            # show an appropriate message of what stage/category was out of stock
        #UCID: ac298 date: 03/25/23
        
        # handle NeedsCleaningException
        except NeedsCleaningException:
            print("needs cleaning")
            while True:
                needs_cleaning = input("Type clean to clean the machine:")
                if needs_cleaning.lower() == "clean":
                    self.clean_machine()
                    print("Machine cleaned")
                    break
                else:
                    print("Machine not cleaned")
            # prompt user to type "clean" to trigger clean_machine()
            # any other input is ignored
            # print a message whether or not the machine was cleaned
            #UCID: ac298 date: 03/25/23
            
        # handle InvalidChoiceException
        except InvalidChoiceException:
            print(f"{str(self.currently_selecting)[6:]}: Invalid Choice")
            # show an appropriate message of what stage/category was the invalid choice was in
        # handle ExceededRemainingChoicesException
        except ExceededRemainingChoicesException:
            print(f"{str(self.currently_selecting)[6:]}: Exceeded Remaining Choices")
            if str(self.currently_selecting)[6:] == "Patty":
                print("Moving to Stage Toppings")
                self.currently_selecting = STAGE.Toppings
            elif str(self.currently_selecting)[6:] == "Toppings":
                print("Moving to Stage Payments")
                self.currently_selecting = STAGE.Pay
            #UCID: ac298 date: 03/25/23
            
                
            # show an appropriate message of which stage/category was exceeded
            # move to the next stage/category
        
        # handle InvalidPaymentException
        except InvalidPaymentException:
            print("please enter the exact amount")
            # show an appropriate message
        except:
            # this is a default catch all, follow the steps above
            print("Something went wrong")        
        self.run()
#UCID: ac298 date: 03/25/23

    def start(self):
        self.run()

    
if __name__ == "__main__":
    bm = BurgerMachine()
    bm.start()
    #UCID: ac298 date: 03/25/23