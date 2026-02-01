def get_rating():
  while True:
    try:
      points = float(input("Rating: "))
      return points
    except ValueError:
      print("Invalid Input!!!")

def classify_rating(points):

  if points > 4.5:
    print("Extraordinary")
  elif points > 4:
    print("Excellent")
  elif points > 3:
    print("Good")
  elif points > 2:
    print("Fair")
  else:
    print("Poor")


def main():
  points = get_rating()
  classify_rating(points)

main()