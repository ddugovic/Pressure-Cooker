# Define game window and area regions
WindowGame = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
HSRegion = \
        {'top': [29],
         'left': [336, 458, 580, 702, 824, 946, 1068, 1190],
         'width': 112,
         'height': 39}
ServeRegion = \
        {'top': [102, 168, 234, 300, 366, 432, 498, 564, 630, 696, 762, 828, 894, 960],
         'left': [0],
         'width': 44,
         'height': 56}
CookRegion = \
        {'top': [131, 197, 263, 329, 395, 461, 527, 593, 659, 725, 791, 857, 923, 989],
         'left': [66],
         'width': 258,
         'height': 33}
TextRegions = \
        {'top': [155, 245, 340, 430],
         'left': [1625, 1785],
         'width': 48,
         'height': 48}
FoodRecipe = \
        {'top': [875],
         'left': [460],
         'width': 1000,
         'height': 115}

# Define non-obvious keypresses
SpecialKeyBinds = {'Chicken': 'k', 'Scrambled': 'c', 'Popcorn Shrimp': 'p',
                   'Shrimp': 'h', 'Corn': 'r', 'Ground Meat': 'm',
                   'Onions': 'n', 'Red Beans': 'b', 'Carrots': 'a',
                   'Lobster': 'b', 'Clam Bits': 'l', 'S.Pork': 'p',
                   'Wh.Rice': 'r', 'G.Beans': 'e', 'Bowtie N.': 'n',
                   'B.Tortilla': 't', 'B.Broccoli': 'r', 'Wheat B.': 'h',
                   'Close': 'l', 'Turkey': 'u', 'Paper Liner': 'n',
                   'Blueberry': 'l', 'Banana': 'a', 'Chocolate': 'h',
                   'Raw Chop': 'l', 'Sauce': 'a', "Pig's Blood": 'b',
                   'Fine Peanut': 'p', 'P.Onions': 'n', 'Cauliflower': 'a',
                   'Cucumber': 'u', 'Cut Parsley': 'p', 'Choc. Cr.': 'h',
                   'Coconut Mer.': 'o', 'Coconut Shav.': 'o', 'Covered': 'v',
                   'R.Chow. Mein': 'h', 'O.Shoots': 's', 'Cucumbers': 'u',
                   'Butter': 'u', 'Black Beans': 'a', 'Cooking Oil': 'o',
                   'Chow Mein': 'h', 'Wheat Bread': 'h', 'Steak Fr.': 't',
                   'Shoestring': 'h', 'Onion Rings': 'n', 'D.Potatoes': 'p',
                   'Paprika': 'r', 'Black Rice': 'r', 'Brown Rice': 'r',
                   'Corn': 'r', 'Croutons': 'r', 'Mixed Veg': 'v',
                   'Tuscan Beans': 'b', 'Candy Cookie': 'a', 'White Rice': 'r',
                   'Wild Rice': 'r', 'Soy Sauce': 'o', 'Clam': 'l',
                   'Raw Chop': 'l', 'Gr. Chicken': 'k', 'Top Bun': 'o',
                   'Guacemole': 'u', 'Sprouts': 'p', 'Pineapple': 'i',
                   'Avocado': 'v', 'Peas': 'e', 'Cranberry': 'r',
                   'Spicy Chk.': 's', 'Biscuit': 'i',
                   'Croissant': 'r', 'Pecan': 'e', 'S.Pasta': 'p',
                   'Grd.Meat': 'm', 'B.Sugar': 's', 'Chili': 'h',
                   'Lobster Sauce': 'o', 'Citrus Mayo': 'm', 'Lemon Aioli': 'a',
                   'Arti.Sauce': 'r', 'C.Apple': 'a', 'Drumstick': 'r',
                   'Oysters': 'y', 'Caviar': 'a', 'Cocktail': 'o',
                   'C.Dates': 'd', 'C.Green': 'g', 'C.Red': 'r', 'C.White': 'w',
                   'C.Tamarind': 't', 'Peach': 'e', 'Texas': 'x',
                   'Pretzel Bun': 'z', 'Pumpkin': 'u', 'Olives': 'v',
                   'Refried Beans': 'b', 'Black Beans': 'a', 'Guac': 'u',
                   'S.Mushrooms': 'm', 'S.Onions': 'n', 'Fr.iEgg': 'e',
                   'Peppermint': 'm', 'Choc.Chips': 'h', 'Caramel': 'a',
                   'P.Sugar': 's', 'Chocolate S.': 'o', 'Blueberries': 'l',
                   'Choe Crisps': 'h', 'Texas Tea': 'x', '[tsl': 'r',
                   'After placing the ingredients. Dunk & Cook.': 'd',
                   'Peach Tea': 'e'}

ChoreInstructions = {'The restroom needs attention. thank you.':
                     [['Flush', 1, 'f'], ['Sanitise', 1, 's']],
                     'Throw the trash. Thanks!':
                     [['Throw', 1, 't'], ['Sanitise', 1, 's']],
                     'Throw the trash, Be sure to mash it in there!':
                     [['Throw', 1, 't'], ['Mash', 20, 'm'], ['Sanitise', 1, 's']],
                     'Please set the roach traps. thank you.':
                     [['Set Traps', 1, 't'], ['Sanitise', 1, 's']],
                     'Please set the rat traps. thank you.':
                     [['Lock', 1, 'l'], ['Cheese', 1, 'c'], ['Set', 1, 's']],
                     'Load the dirty dishes into the rack. Wash. wait for the green light.' +
                     ' and then  release the washer and unload the dishes.':
                     [['Dishes', 1, 'd'], ['Wash', 30, 'w'], ['Release', 1, 'r'], ['Unload', 1, 'u'], ['Sanitise', 1, 's']],
                     'Please clean the pest light trap. thank you.':
                     [['Open Trap', 1, 't'], ['Close Trap', 1, 'c'], ['Sanitise', 1, 's']]}

ServingKeyBinds = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                   '6': '6', '7': '7', '8': '8', '9': '9', '10': '0',
                   '11': '-', '12': '=', '13': '[', '14': ']'}
