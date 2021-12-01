# Test Only

# Ce fichier ne doit être utilisé qu'à des fin de test.
# Le code répondant à une question devrait être directement
# dans le fichier correspondant à la question
# avec un "if __name__ == "__main__"


import numpy as np


def test_1():
    print("Hi Orlando")
    pass
    pass


var = 12

if __name__ == "__main__":
    arr = np.ones(10) * var
    test_1()
    print(arr)
