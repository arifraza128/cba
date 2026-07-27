num = int(input("Enter a number: "))

original = num
reverse = 0
remaining = abs(num)

while remaining > 0:
    digit = remaining % 10
    reverse = reverse * 10 + digit
    remaining //= 10

if original == reverse and original >= 0:
    print("Palindrome")
else:
    print("Not Palindrome")