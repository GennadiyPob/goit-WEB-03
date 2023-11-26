""" Визначення дільників чисел """

number = int(input('Enter whole number :'))

dev = 1
deviders = []
while dev <= number:
    
    if number % dev == 0: 
        deviders.append(dev)
    dev = dev + 1

print(f'Deviders of {number} is {deviders}')

