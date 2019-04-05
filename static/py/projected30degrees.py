import math


class ProjectedPrice():
    def __init__(self):
        pass
    def price_at_30_degrees(self):
        days = input("Please enter the days: ")
        diagonalDist = int(days)/math.cos(19)
        priceIncrease = math.sqrt(diagonalDist**2 - int(days)**2)/100
        return priceIncrease

if __name__ == '__main__':
    pred = ProjectedPrice()
    print (pred.price_at_30_degrees())
