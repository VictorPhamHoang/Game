I – Installation Instructions
The game folder to download consists of three files:

The Python script,
A SQLite file,
And a SQL script file for creating the database.
To play the game, you must first install Python (preferably a recent version) and add it to the PATH.

Open a command terminal, navigate to the game folder directory using the cd command, then execute the Python script jeu.py with the command python jeu.py.

It is not necessary to install SQLite unless you want to view the database data. However, database management is handled using Python’s sqlite3 module.

II – Game Explanation
Game Rules:
The user plays as a restaurant owner who has taken out a loan of €1150 and must repay it within four months.

The restaurant has only one dish and one employee. The cost of resources (electricity, raw materials, etc.) varies depending on the month.

The game is played over four rounds (representing four months).

First three rounds (months): The player must set the price for their dish for the current month.
A low price will increase customer satisfaction but reduce profit, and vice versa.
After setting the price, the game calculates the profit made and the average customer satisfaction score for the current month, as well as the total profit and the overall average customer satisfaction score for all months combined.
Based on these results, the player can adjust the price of their dish for the following month.

Fourth round (final month): The player only has the option to decide whether to fire their employee.

The player must make strategic choices and avoid setting prices randomly. The cost of each resource (rent, employee salary, raw materials, electricity, personal expenses) is provided at the start of month one, and some resources are updated throughout the different months.
This means the player will need to perform some calculations.

At the end of the fourth round, the total profit and the average customer satisfaction score over the four months are displayed.
The game assigns a score based on whether:

The player successfully repaid the loan (total profit > €1150),
The restaurant’s average customer satisfaction score.
Database Integration
All games are stored in the database. This means that all restaurants are recorded in the entreprise table with the player’s username associated with the restaurant.

When the program starts, the user is prompted to provide a username.

If the username already exists in the database, all games they created are displayed, and they are asked whether they want to continue an existing game or start a new one.
Otherwise, a new player is created using the provided username as the primary key, and the player’s name is also requested and stored in the joueur database.
The current month of the restaurant is also stored in the entreprise table, allowing the player to resume an ongoing game later.

Program Information
At the start, a set of functions is defined to keep the code clean and facilitate easier updates. Each function is described in comments.
Whenever the user provides a value, the program verifies that the value’s type matches what is expected.
