ratings = [5, 4, 3, 5, 2, 5, 4, 1, 5, 3]

average = sum(ratings) / len(ratings)

print("Average Rating:", average)
print("5-Star Ratings:", ratings.count(5))

ratings.sort()

print("Sorted Ratings:", ratings)