num = int(input("Enter a number: "))

reverse = 0
remaining = abs(num)

while remaining > 0:
    digit = remaining % 10
    reverse = reverse * 10 + digit
    remaining //= 10

if num < 0:
    reverse = -reverse

print("Reversed Number:", reverse)