# Define the allowed operations
OPERATIONS = {"XOR": lambda x, y: not (x or y), 
              "NAND": lambda x, y: not (x and y),
			  "EQ": lambda x, y: x == y, 
			  "AND": lambda x, y: x and y,
			  "OR": lambda x, y: x or y}