cart = []

while True:

    print("\n1.Add Product")
    print("2.Remove Product")
    print("3.Update Product")
    print("4.Display Cart")
    print("5.Checkout")
    print("6.Exit")

    choice = int(input("Choice: "))

    if choice == 1:
        product = input("Product Name: ")
        qty = int(input("Quantity: "))
        cart.append([product, qty])

    elif choice == 2:
        product = input("Product to Remove: ")

        for item in cart:
            if item[0] == product:
                cart.remove(item)
                break

    elif choice == 3:
        product = input("Product Name: ")
        qty = int(input("New Quantity: "))

        for item in cart:
            if item[0] == product:
                item[1] = qty

    elif choice == 4:
        print("\nShopping Cart")
        for item in cart:
            print(item[0], "-", item[1])

    elif choice == 5:
        cart.clear()
        print("Checkout Successful")

    else:
        break