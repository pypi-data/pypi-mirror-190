class Calculator():
    def __init__(self, num_1: float, num_2: float):  #constructor to initialize instance variables
        self.num_1 = num_1
        self.num_2 = num_2
    
    def add(self):
        return self.num_1 + self.num_2
    
    def subtract(self):
        return self.num_1 - self.num_2
    
    def multiply(self):
        return self.num_1 * self.num_2
    
    def divide(self):
        return self.num_1 / self.num_2
    
    def nth_root(self):
        return self.num_1 ** (1/self.num_2)
    
    def reset_memory(self):
        return 0


def calculator():
    """This function outputs instructions for the user on how to use
    the Calculator as well as the calculated answers. It also handles user
    inputs on operations and variables"""
    internal_memory = 0.0
    answer = 0.0
    instruction = 'This is Calculator. Enter: \n+ to add \n- to subtract \n* to '\
                    'multiply \n/ to divide \nn to take n(th) root of a number \nr to reset '\
                    'Calculator memory to 0 \nq to quit Calculator'

    print(instruction)

    while True:

        num_1 = internal_memory #assigment to do calculations on internal memory value
        user_input = input()

        if user_input == 'q': #user decision to quit calculator
            break

        if user_input == '+':
            num_2 = float(input())
            calculator = Calculator(num_1, num_2) #add always uses internal memory value
            answer = calculator.add()
            print(f'Answer: {answer}')
        
        elif user_input == '-':
            num_2 = float(input())
            calculator = Calculator(num_1, num_2) #subtract always uses internal memory value
            answer = calculator.subtract()
            print(f'Answer: {answer}')

        elif user_input == '*':
            if internal_memory == 0: #ask for a new multiplier to avoid always multiplying 0
                num_1 = float(input('Type a new multiplier: '))
                num_2 = float(input('Type a multiplicand: '))
            else:
                num_2 = float(input())
            calculator = Calculator(num_1, num_2)
            answer = calculator.multiply()
            print(f'Answer: {answer}')

        elif user_input == '/':
            if internal_memory == 0: #ask for a new dividend to avoid always dividing 0
                num_1 = float(input('Type a new dividend: '))
                num_2 = float(input('Type a non-zero divisor: '))
            else:
                num_2 = float(input('Type a non-zero divisor: ')) #remind to avoid division by 0
            calculator = Calculator(num_1, num_2)
            answer = calculator.divide()
            print(f'Answer: {answer}')

        elif user_input == 'n':
            if internal_memory < 0: #avoid complex numbers
                num_1 = float(input('Type a new positive radicand: '))
            num_2 = float(input('Type a root index: '))
            calculator = Calculator(num_1, num_2)
            answer = calculator.nth_root()
            print(f'Answer: {answer}')

        elif user_input == 'r':
            calculator = Calculator(num_1, num_2)
            answer = calculator.reset_memory()
            print(f'Internal memory sucessfully reset to {answer}')
        
        else:
            print(f'Operation unavailable in this Calculator. Try again. \n{instruction}')

        internal_memory = answer

calculator()
