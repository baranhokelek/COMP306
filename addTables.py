import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "hellothere",
    database = "RestaurantChain"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE Branch (Location VARCHAR(100),City VARCHAR(100),OpeningYear VARCHAR(100),PRIMARY KEY (Location))")

mycursor.execute("CREATE TABLE Chef (ID INT, Name VARCHAR(100), Location VARCHAR(100), Salary INT, Age INT, ChefRank INT, PRIMARY KEY (ID), FOREIGN KEY (Location) REFERENCES Branch(Location))")

mycursor.execute("CREATE TABLE Staff (SID INT,Name VARCHAR(100),Location VARCHAR(100),Salary INT,Age INT,FOREIGN KEY (Location) REFERENCES Branch (Location),PRIMARY KEY (SID))")

mycursor.execute("CREATE TABLE Customer (CID INT,Name VARCHAR(100),Location VARCHAR(100),Age INT,FOREIGN KEY (Location) REFERENCES Branch (Location),PRIMARY KEY (CID))")

mycursor.execute("CREATE TABLE Recipe (RecipeName VARCHAR(100),Season VARCHAR(100),Calories INT,Price INT,PRIMARY KEY (RecipeName))")

mycursor.execute("CREATE TABLE Ingredient (IngredientName VARCHAR(100),Location VARCHAR(100),Season VARCHAR(100),Price INT,Storage INT, FOREIGN KEY (Location) REFERENCES Branch(Location),PRIMARY KEY (IngredientName, Location))")

mycursor.execute("CREATE TABLE RecipeIngredient (RecipeName VARCHAR(100),IngredientName VARCHAR(100),Amount INT,FOREIGN KEY (RecipeName) REFERENCES Recipe (RecipeName),FOREIGN KEY (IngredientName) REFERENCES Ingredient (IngredientName),PRIMARY KEY (RecipeName, IngredientName))")

mycursor.execute("CREATE TABLE Menu (Number INT,Location VARCHAR(100),RecipeName VARCHAR(100),Language VARCHAR(100),Page INT,FOREIGN KEY (RecipeName) REFERENCES Recipe (RecipeName),FOREIGN KEY (Location) REFERENCES Branch (Location),PRIMARY KEY (Number, Location))")

mycursor.execute("CREATE TABLE MenuHasRecipe (RecipeName VARCHAR(100),MenuNumber INT,FOREIGN KEY (RecipeName) REFERENCES Recipe(RecipeName),FOREIGN KEY (MenuNumber) REFERENCES Menu (Number),PRIMARY KEY (RecipeName, MenuNumber))")

mycursor.execute("CREATE TABLE Orders (RecipeName VARCHAR(100),Location VARCHAR(100),CustomerID INT,StaffID INT,ChefID INT,Date VARCHAR(100),FOREIGN KEY (CustomerID) REFERENCES Customer(CID),FOREIGN KEY (StaffID) REFERENCES Staff (SID),FOREIGN KEY (ChefID) REFERENCES Chef (ID),FOREIGN KEY (Location) REFERENCES Branch (Location),FOREIGN KEY (RecipeName) REFERENCES Recipe(RecipeName),PRIMARY KEY (Location, RecipeName, CustomerID, StaffID, ChefID))")

mycursor.execute("CREATE TABLE CustomerRatesBranch (CustomerID INT,Location VARCHAR(100),Comment VARCHAR(100),Rating VARCHAR(100),FOREIGN KEY (Location) REFERENCES Branch (Location),FOREIGN KEY (CustomerID ) REFERENCES Customer (CID),PRIMARY KEY (CustomerID, Location))")

mycursor.execute("show tables")

for x in mycursor:
    print(x)