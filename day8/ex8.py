num = int(input("Enter a number: "))

sum_digits = 0
remaining = abs(num)

while remaining > 0:
    digit = remaining % 10
    sum_digits += digit
    remaining //= 10

print("Sum of digits =", sum_digits)