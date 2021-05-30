from functools import reduce
import mysql.connector
from faker import Faker
import random
from operator import mul

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hellothere",
)

mycursor = mydb.cursor()
fake = Faker()
delete_on_beginning = True
# Delete all the previously loaded data(for debugging purposes).
if delete_on_beginning:
    mycursor.execute("drop database if exists RestaurantChain")
    mycursor.execute("create database RestaurantChain")
    mycursor.execute("use RestaurantChain")
    mycursor.execute("CREATE TABLE Branch (Location VARCHAR(100),City VARCHAR(100),OpeningYear VARCHAR(100),PRIMARY KEY (Location))")
    mycursor.execute("CREATE TABLE Chef (ID INT, Name VARCHAR(100), Location VARCHAR(100), Salary INT, Age INT, ChefRank INT, PRIMARY KEY (ID), FOREIGN KEY (Location) REFERENCES Branch(Location))")
    mycursor.execute("CREATE TABLE Staff (SID INT,Name VARCHAR(100),Location VARCHAR(100),Salary INT,Age INT,FOREIGN KEY (Location) REFERENCES Branch (Location),PRIMARY KEY (SID))")
    mycursor.execute("CREATE TABLE Customer (CID INT,Name VARCHAR(100),Location VARCHAR(100),Age INT,FOREIGN KEY (Location) REFERENCES Branch (Location),PRIMARY KEY (CID))")
    mycursor.execute("CREATE TABLE Recipe (RecipeName VARCHAR(100),Season VARCHAR(100),Calories INT,Price REAL,PRIMARY KEY (RecipeName))")
    mycursor.execute("CREATE TABLE Ingredient (IngredientName VARCHAR(100),Location VARCHAR(100),Season VARCHAR(100),Price REAL,Storage INT, FOREIGN KEY (Location) REFERENCES Branch(Location),PRIMARY KEY (IngredientName, Location))")
    mycursor.execute("CREATE TABLE RecipeIngredient (RecipeName VARCHAR(100),IngredientName VARCHAR(100),Amount INT,FOREIGN KEY (RecipeName) REFERENCES Recipe (RecipeName),FOREIGN KEY (IngredientName) REFERENCES Ingredient (IngredientName),PRIMARY KEY (RecipeName, IngredientName))")
    mycursor.execute("CREATE TABLE Menu (Number INT,Location VARCHAR(100),RecipeName VARCHAR(100),Language VARCHAR(100),Page INT,FOREIGN KEY (RecipeName) REFERENCES Recipe (RecipeName),FOREIGN KEY (Location) REFERENCES Branch (Location),PRIMARY KEY (Number, Location))")
    mycursor.execute("CREATE TABLE MenuHasRecipe (RecipeName VARCHAR(100),MenuNumber INT,FOREIGN KEY (RecipeName) REFERENCES Recipe(RecipeName),FOREIGN KEY (MenuNumber) REFERENCES Menu (Number),PRIMARY KEY (RecipeName, MenuNumber))")
    mycursor.execute("CREATE TABLE Orders (RecipeName VARCHAR(100),Location VARCHAR(100),CustomerID INT,StaffID INT,ChefID INT,Date VARCHAR(100),FOREIGN KEY (CustomerID) REFERENCES Customer(CID),FOREIGN KEY (StaffID) REFERENCES Staff (SID),FOREIGN KEY (ChefID) REFERENCES Chef (ID),FOREIGN KEY (Location) REFERENCES Branch (Location),FOREIGN KEY (RecipeName) REFERENCES Recipe(RecipeName),PRIMARY KEY (Location, RecipeName, CustomerID, StaffID, ChefID))")
    mycursor.execute("CREATE TABLE CustomerRatesBranch (CustomerID INT,Location VARCHAR(100),Comment VARCHAR(100),Rating REAL, FOREIGN KEY (Location) REFERENCES Branch (Location),FOREIGN KEY (CustomerID ) REFERENCES Customer (CID),PRIMARY KEY (CustomerID, Location))")

# First, I have to create lists of attributes of primary keys to make sure everything is consistent.
# If we randomly generate ChefID's in one table, and forget them, it would be impossible to create a consistent dataset.
"""
Primary Keys:
Key Name    |   Type    |   Qty
----------------------------------
ChefID      |   Integer |   200
Location    |   Char    |   50
StaffID     |   Integer |   400
CustID      |   Integer |   1000
RecipeName  |   Char    |   20
Ingr.Name   |   Char    |   40
MenuNumber  |   Integer |   50
"""
chefIDQty = 200
locationQty = 50
staffIDQty = 400
customerIDQty = 1000
recipeNameQty = 20
ingrNameQty = 40
menuNumberQty = 50

chefIDLowerLimit = 10000
chefIDUpperLimit = 100000
staffIDLowerLimit = 10000
staffIDUpperLimit = 100000
customerIDLowerLimit = 10000
customerIDUpperLimit = 100000
menuNumberLowerLimit = 1
menuNumberUpperLimit = 100

chefIDs = random.sample(range(chefIDLowerLimit, chefIDUpperLimit), chefIDQty)
locations = [fake.address().replace("\n", " , ") for i in range(locationQty)]
staffIDs = random.sample(range(staffIDLowerLimit, staffIDUpperLimit), staffIDQty)
customerIDs = random.sample(range(customerIDLowerLimit, customerIDUpperLimit), customerIDQty)
recipeNamesLong = ["African Bean Soup", "Alu Piajer Chorchori", "Apple Chutney", "Apple Pie", "Baked Beans",
                   "Banana Cream Pie", "Bean and Fruit Bake", "Beer Bread", "Black Bean Chili",
                   "Boston Baked Blackeye Peas", "Button Onions with Sultanas", "Casablanca Couscous",
                   "Chickpea and Potato Curry", "Chinese Pickled Garlic", "Cold Strawberry/Banana Pie",
                   "Curried Mushrooms", "Dosai", "Baked Brie", "Shrimp Wrapped in Pea Pods", "Russian Stuffed Eggs",
                   "Boboli Pizza", "Mini Quiche", "Roquefort-Leek Filling", "Crab Filling", "Sourdough Baguettes",
                   "Bacon and Cream Cheese Stuffed Mushrooms", "Trota Piccante", "Turkish Leeks", "Mushroom Pate",
                   "Roasted Garlic", "Grilled Jamaican Jerk Chicken"]
random.shuffle(recipeNamesLong)
recipeNames = recipeNamesLong[:recipeNameQty]
ingredLong = ["Margarine", "Carrots", "Black Eyed Peas", "Green Pepper", "Salt", "Basil Leaves", "Ground Corriander",
              "Potatoes", "Chili Paste", "Oil", "Parsley", "Olive Oil", "Sugar", "Apples", "Cinnamon", "Clover",
              "Cider", "Garlic", "Butter", "Flour", "Balsamic Vinegar", "Tofu", "Bananas", "Maple Syrup", "Eggplants",
              "Horseradish", "Kidney Beans", "Celery", "Molasses", "Mustard", "Thyme", "Cranberries",
              "Chocolate Chips", "Couscous", "Sliced Mushrooms", "Chickpeas", "Curry Powder", "Tomatoes", "Tarragon",
              "Wine", "Shrimp", "Pesto Sauce", "Grated Cheese", "Crab Meat", "Minced Leeks", "Cumin", "Rump Steak",
              "Mayonnaise", "Paprika", "Bacon", "Teriyaki Sauce", "Tahini", "Rice", "Lemon Juice", "Scallops",
              "Worcestershire Sauce", "Sherry", "Cream Cheese", "Ginger", "Parmesan"]
random.shuffle(ingredLong)
ingredients = ingredLong[:ingrNameQty]
menuNumbers = random.sample(range(menuNumberLowerLimit, menuNumberUpperLimit), menuNumberQty)

seasons = ["Fall", "Spring", "Summer", "Winter"]


def randomAge(lowerLimit=20, upperLimit=100):
    return random.randint(lowerLimit, upperLimit)


def randomName():
    return fake.name()


def randomLocation():
    return locations[random.randint(0, locationQty-1)]


def randomSalary(lowerLimit=100, upperLimit=3000):
    return random.randint(lowerLimit, upperLimit)


def randomRank(lowerLimit=1, upperLimit=6):
    return random.randint(lowerLimit, upperLimit)


def randomCity():
    return fake.city()


def randomYear():
    return fake.year()


def randomRating(lowerLimit=0.0, upperLimit=5.0):
    return round(random.uniform(lowerLimit, upperLimit), 1)


def randomText(length=100):
    return fake.text(length)


def randomSeason():
    return random.choice(seasons)


def randomPrice(lowerLimit=20.0, upperLimit=200.0):
    return round(random.uniform(lowerLimit, upperLimit), 1)


def randomStorageQty(lowerLimit=0, upperLimit=1000):
    return random.randint(lowerLimit, upperLimit)


def randomRecipe():
    return random.choice(recipeNames)


def randomLanguage():
    return fake.language_name()


def randomAmount(lowerLimit=1, upperLimit=10):
    return random.randint(lowerLimit, upperLimit)


def randomCalories(lowerLimit=100, upperLimit=1500):
    return random.randrange(lowerLimit, upperLimit, 10)


def randomDate():
    return fake.iso8601()


def generateUniqueRandomNTuples(*args):
    seen = set()
    ntuple = tuple([random.randint(0, arg-1) for arg in args])
    while True:
        seen.add(ntuple)
        yield ntuple
        ntuple = tuple([random.randint(0, arg-1) for arg in args])
        while ntuple in seen:
            ntuple = tuple([random.randint(0, arg-1) for arg in args])


def getCombinationRange(*args):
    return random.randint(min(args), reduce(mul, args))

"""
Branch
Location    :   Char(100)   *
City        :   Char(100)
OpeningYear :   Char(100)
"""
for i in range(locationQty):
    sql = "insert into Branch(Location, City, OpeningYear) values (%s, %s, %s)"
    val = (locations[i], randomCity(), randomYear())
    mycursor.execute(sql, val)
    mydb.commit()

"""
Chef
ID      :   Integer     *
Name    :   Char(100)
Location:   Char(100)   +
Salary  :   Integer
Age     :   Integer
ChefRank:   Integer
"""
for i in range(chefIDQty):
    sql = "insert into Chef(ID, Name, Location, Salary, Age, ChefRank) values (%s, %s, %s, %s, %s, %s)"
    val = (chefIDs[i], randomName(), randomLocation(), randomSalary(), randomAge(), randomRank())
    mycursor.execute(sql, val)
    mydb.commit()

"""
Customer
CID     :   Integer     *
Name    :   Char(100)
Location:   Char(100)   +
Age     :   Integer
"""
for i in range(customerIDQty):
    sql = "insert into Customer(CID, Name, Location, Age) values (%s, %s, %s, %s)"
    val = (customerIDs[i], randomName(), randomLocation(), randomAge())
    mycursor.execute(sql, val)
    mydb.commit()

"""
CustomerRatesBranch
CustomerID  :   Integer     *
Location    :   Char(100)   *
Comment     :   Char(100)
Rating      :   Double
"""
g = generateUniqueRandomNTuples(customerIDQty, locationQty)
for i in range(getCombinationRange(customerIDQty, locationQty)):
    customerLocationPair = next(g)
    sql = "insert into CustomerRatesBranch(CustomerID, Location, Comment, Rating) values (%s, %s, %s, %s)"
    val = (customerIDs[customerLocationPair[0]], locations[customerLocationPair[1]], randomText(), randomRating())
    mycursor.execute(sql, val)
    mydb.commit()

"""
for i in range(customerIDQty):
    for j in range(locationQty):
        sql = "insert into CustomerRatesBranch(CustomerID, Location, Comment, Rating) values (%s, %s, %s, %s)"
        val = (customerIDs[i], locations[j], randomText(), randomRating())
        mycursor.execute(sql, val)
        mydb.commit()       
"""
"""
Ingredient
IngredientName  :   Char(100)   *
Location        :   Char(100)   *
Season          :   Char(100)
Price           :   Double
Storage         :   Integer
"""
"""
g = generateUniqueRandomNTuples(ingrNameQty, locationQty)
for i in range(getCombinationRange(ingrNameQty, locationQty)):
    ingredientLocationPair = next(g)
    sql = "insert into Ingredient(IngredientName, Location, Season, Price, Storage) values (%s, %s, %s, %s, %s)"
    val = (ingredients[ingredientLocationPair[0]], locations[ingredientLocationPair[1]], randomSeason(), randomPrice(), randomStorageQty())
    mycursor.execute(sql, val)
    mydb.commit()
"""
for i in range(ingrNameQty):
    for j in range(locationQty):
        sql = "insert into Ingredient(IngredientName, Location, Season, Price, Storage) values (%s, %s, %s, %s, %s)"
        val = (ingredients[i], locations[j], randomSeason(), randomPrice(), randomStorageQty())
        mycursor.execute(sql, val)
        mydb.commit()
"""
Recipe
RecipeName  :   Char(100)   *
Season      :   Char(100)
Calories    :   Integer
Price       :   Double
"""
for i in range(recipeNameQty):
    sql = "insert into Recipe(RecipeName, Season, Calories, Price) values (%s, %s, %s, %s)"
    val = (recipeNames[i], randomSeason(), randomCalories(), randomPrice())
    mycursor.execute(sql, val)
    mydb.commit()

"""
Menu
Number      :   Integer     *
Location    :   Char(100)   *
RecipeName  :   Char(100)   +
Language    :   Char(100)
Page        :   Integer
"""
"""
g = generateUniqueRandomNTuples(menuNumberQty, locationQty)
for i in range(getCombinationRange(menuNumberQty, locationQty)):
    menuNumberLocationPair = next(g)
    sql = "insert into Menu(Number, Location, RecipeName, Language, Page) values (%s, %s, %s, %s, %s)"
    val = (menuNumbers[menuNumberLocationPair[0]], locations[menuNumberLocationPair[1]], randomRecipe(), randomLanguage(), randomPrice())
    mycursor.execute(sql, val)
    mydb.commit()
"""
for i in range(menuNumberQty):
    for j in range(locationQty):
        sql = "insert into Menu(Number, Location, RecipeName, Language, Page) values (%s, %s, %s, %s, %s)"
        val = (menuNumbers[i], locations[j], randomRecipe(), randomLanguage(), randomPrice())
        mycursor.execute(sql, val)
        mydb.commit()

"""
MenuHasRecipe
RecipeName  :   Char(100)   *
MenuNumber  :   Integer     *
"""

g = generateUniqueRandomNTuples(recipeNameQty, menuNumberQty)
for i in range(getCombinationRange(recipeNameQty, menuNumberQty)):
    recipeNameMenuNumberPair = next(g)
    sql = "insert into MenuHasRecipe(RecipeName, MenuNumber) values (%s, %s)"
    val = (recipeNames[recipeNameMenuNumberPair[0]], menuNumbers[recipeNameMenuNumberPair[1]])
    mycursor.execute(sql, val)
    mydb.commit()

"""
for i in range(recipeNameQty):
    for j in range(menuNumberQty):
        sql = "insert into MenuHasRecipe(RecipeName, MenuNumber) values (%s, %s)"
        val = (recipeNames[i], menuNumbers[j])
        mycursor.execute(sql, val)
        mydb.commit()
"""
"""
Staff   
SID     :   Integer     *
Name    :   Char(100)
Location:   Char(100)   +
Salary  :   Integer
Age     :   Integer
"""
for i in range(staffIDQty):
    sql = "insert into Staff(SID, Name, Location, Salary, Age) values (%s, %s, %s, %s, %s)"
    val = (staffIDs[i], randomName(), randomLocation(), randomSalary(), randomAge())
    mycursor.execute(sql, val)
    mydb.commit()

"""
Orders
RecipeName  :   Char(100)   *+
Location    :   Char(100)   *+
CustomerID  :   Integer     *+
StaffID     :   Integer     *+
ChefID      :   Integer     *+
Date        :   Char(100)
"""
g = generateUniqueRandomNTuples(recipeNameQty, locationQty, customerIDQty, staffIDQty, chefIDQty)
numOrders = getCombinationRange(recipeNameQty, locationQty, customerIDQty, staffIDQty, chefIDQty)
# Turns out, a random number between minimum qty of primary keys and the permutation of all primary key qtys is just way too much.
# I use 10,000 as the upper bound.
for i in range(min(numOrders, 10000)): 
    theQuintuple = next(g)
    sql = "insert into Orders(RecipeName, Location, CustomerID, StaffID, ChefID, Date) values (%s, %s, %s, %s, %s, %s)"
    val = (recipeNames[theQuintuple[0]], locations[theQuintuple[1]], customerIDs[theQuintuple[2]], staffIDs[theQuintuple[3]], chefIDs[theQuintuple[4]], randomDate())
    mycursor.execute(sql, val)
    mydb.commit()

"""
RecipeIngredient
RecipeName      :   Char(100)   *+
IngredientName  :   Char(100)   *+
Amount          :   Integer
"""
g = generateUniqueRandomNTuples(recipeNameQty, ingrNameQty)
for i in range(getCombinationRange(recipeNameQty, ingrNameQty)):
    recipeNameIngredientPair = next(g)
    sql = "insert into RecipeIngredient(RecipeName, IngredientName, Amount) values (%s, %s, %s)"
    val = (recipeNames[recipeNameIngredientPair[0]], ingredients[recipeNameIngredientPair[1]], randomAmount())
    mycursor.execute(sql, val)
    mydb.commit()
