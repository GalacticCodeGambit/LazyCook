from Database import addRecipe, addIngredient, addIngredientToRecipe, getConnection

def getOrCreateIngredient(name: str, amountType: str) -> int:
    con = getConnection()
    try:
        cur = con.cursor()
        cur.execute("SELECT id FROM Ingredient WHERE name = ?", (name,))
        row = cur.fetchone()
        if row:
            return row["id"]
    finally:
        con.close()
    return addIngredient(name, amountType)

recipes = [
    ("Spaghetti Bolognese", "Klassische italienische Pasta mit Fleischsauce.", [("Spaghetti","g"),("Ground Beef","g"),("Tomato Sauce","ml"),("Onion","pcs"),("Garlic","pcs")]),
    ("Caesar Salad", "Knackiger Salat mit Caesar Dressing.", [("Romaine Lettuce","g"),("Parmesan","g"),("Croutons","g"),("Caesar Dressing","ml")]),
    ("Chicken Curry", "Würziges indisches Curry.", [("Chicken Breast","g"),("Curry Paste","tbsp"),("Coconut Milk","ml"),("Onion","pcs"),("Garlic","pcs")]),
    ("Pancakes", "Fluffige amerikanische Pancakes.", [("Flour","g"),("Egg","pcs"),("Milk","ml"),("Butter","g"),("Baking Powder","tsp")]),
    ("Tomato Soup", "Cremige Tomatensuppe.", [("Tomatoes","g"),("Onion","pcs"),("Garlic","pcs"),("Vegetable Broth","ml"),("Cream","ml")]),
    ("Beef Stir Fry", "Schnelles Rindfleisch mit Gemüse.", [("Beef Strips","g"),("Broccoli","g"),("Soy Sauce","ml"),("Ginger","g"),("Garlic","pcs")]),
    ("Omelette", "Einfaches Frühstücksomelette.", [("Egg","pcs"),("Butter","g"),("Salt","tsp"),("Pepper","tsp"),("Cheese","g")]),
    ("French Onion Soup", "Klassische französische Zwiebelsuppe.", [("Onion","pcs"),("Beef Broth","ml"),("Butter","g"),("Baguette","slices"),("Gruyere","g")]),
    ("Tiramisu", "Italienisches Dessert mit Kaffee.", [("Mascarpone","g"),("Egg","pcs"),("Sugar","g"),("Espresso","ml"),("Ladyfingers","pcs")]),
    ("Beef Burger", "Saftiger Rindfleischburger.", [("Ground Beef","g"),("Burger Bun","pcs"),("Lettuce","g"),("Tomato","pcs"),("Cheese","g")]),
    ("Fried Rice", "Gebratener Reis mit Gemüse.", [("Rice","g"),("Egg","pcs"),("Soy Sauce","ml"),("Carrot","pcs"),("Green Onion","g")]),
    ("Lemon Chicken", "Zitronenhähnchen aus dem Ofen.", [("Chicken Breast","g"),("Lemon","pcs"),("Garlic","pcs"),("Olive Oil","ml"),("Thyme","tsp")]),
    ("Vegetable Curry", "Cremiges Gemüsecurry.", [("Potato","pcs"),("Chickpeas","g"),("Coconut Milk","ml"),("Curry Paste","tbsp"),("Onion","pcs")]),
    ("Chocolate Mousse", "Luftiges Schokoladenmousse.", [("Dark Chocolate","g"),("Egg","pcs"),("Sugar","g"),("Cream","ml"),("Butter","g")]),
    ("Banana Bread", "Saftiges Bananenbrot.", [("Banana","pcs"),("Flour","g"),("Sugar","g"),("Egg","pcs"),("Butter","g")]),
    ("Minestrone", "Herzhafter italienischer Gemüseeintopf.", [("Tomatoes","g"),("Zucchini","pcs"),("Carrot","pcs"),("Pasta","g"),("Vegetable Broth","ml")]),
    ("Quiche Lorraine", "Französischer Speck-Käse-Kuchen.", [("Bacon","g"),("Egg","pcs"),("Cream","ml"),("Cheese","g"),("Pie Crust","pcs")]),
    ("Shakshuka", "Nordafrikanische Eier in Tomatensauce.", [("Tomatoes","g"),("Egg","pcs"),("Onion","pcs"),("Paprika","tsp"),("Garlic","pcs")]),
    ("Pad Thai", "Thailändische Reisnudeln.", [("Rice Noodles","g"),("Shrimp","g"),("Egg","pcs"),("Bean Sprouts","g"),("Peanuts","g")]),
    ("Lasagna", "Klassische Lasagne.", [("Lasagna Sheets","pcs"),("Ground Beef","g"),("Tomato Sauce","ml"),("Bechamel Sauce","ml"),("Parmesan","g")]),
    ("Gazpacho", "Spanische Kaltsuppe.", [("Tomatoes","g"),("Cucumber","pcs"),("Bell Pepper","pcs"),("Garlic","pcs"),("Olive Oil","ml")]),
    ("Waffles", "Knusprige Waffeln.", [("Flour","g"),("Egg","pcs"),("Milk","ml"),("Butter","g"),("Sugar","g")]),
    ("Ramen", "Japanische Nudelsuppe.", [("Ramen Noodles","g"),("Chicken Broth","ml"),("Soy Sauce","ml"),("Soft Boiled Egg","pcs"),("Green Onion","g")]),
    ("Bruschetta", "Knoblaucbrot mit Tomaten.", [("Baguette","slices"),("Tomatoes","g"),("Garlic","pcs"),("Basil","g"),("Olive Oil","ml")]),
    ("Paella", "Spanischer Reistopf.", [("Rice","g"),("Chicken Breast","g"),("Shrimp","g"),("Saffron","tsp"),("Bell Pepper","pcs")]),
    ("Coleslaw", "Cremiger Krautsalat.", [("Cabbage","g"),("Carrot","pcs"),("Mayonnaise","ml"),("Vinegar","ml"),("Sugar","tsp")]),
    ("Beef Tacos", "Mexikanische Rindfleischtacos.", [("Ground Beef","g"),("Taco Shells","pcs"),("Cheese","g"),("Sour Cream","ml"),("Salsa","ml")]),
    ("Pumpkin Soup", "Cremige Kürbissuppe.", [("Pumpkin","g"),("Onion","pcs"),("Vegetable Broth","ml"),("Cream","ml"),("Ginger","g")]),
    ("Fish and Chips", "Britischer Klassiker.", [("Cod Fillet","g"),("Potato","pcs"),("Flour","g"),("Beer","ml"),("Oil","ml")]),
    ("Risotto", "Cremiges Reisotto.", [("Arborio Rice","g"),("Vegetable Broth","ml"),("Parmesan","g"),("Onion","pcs"),("White Wine","ml")]),
    ("Spring Rolls", "Knusprige Frühlingsrollen.", [("Rice Paper","pcs"),("Carrot","pcs"),("Cucumber","pcs"),("Shrimp","g"),("Mint","g")]),
    ("Beef Stroganoff", "Russisches Rindfleischgericht.", [("Beef Strips","g"),("Mushrooms","g"),("Sour Cream","ml"),("Onion","pcs"),("Butter","g")]),
    ("Apple Pie", "Klassischer amerikanischer Apfelkuchen.", [("Apple","pcs"),("Flour","g"),("Sugar","g"),("Butter","g"),("Cinnamon","tsp")]),
    ("Falafel", "Nahost Kichererbsenbällchen.", [("Chickpeas","g"),("Onion","pcs"),("Garlic","pcs"),("Cumin","tsp"),("Parsley","g")]),
    ("Nachos", "Überbackene Tortillachips.", [("Tortilla Chips","g"),("Cheese","g"),("Jalapeños","g"),("Sour Cream","ml"),("Salsa","ml")]),
    ("Chicken Wings", "Würzige Hühnerflügel.", [("Chicken Wings","g"),("Hot Sauce","ml"),("Butter","g"),("Garlic Powder","tsp"),("Paprika","tsp")]),
    ("Tzatziki", "Griechischer Joghurtdip.", [("Greek Yogurt","ml"),("Cucumber","pcs"),("Garlic","pcs"),("Dill","g"),("Olive Oil","ml")]),
    ("Moussaka", "Griechischer Auflauf.", [("Ground Beef","g"),("Eggplant","pcs"),("Tomato Sauce","ml"),("Bechamel Sauce","ml"),("Parmesan","g")]),
    ("Cheesecake", "Cremiger New Yorker Käsekuchen.", [("Cream Cheese","g"),("Sugar","g"),("Egg","pcs"),("Graham Crackers","g"),("Butter","g")]),
    ("Bibimbap", "Koreanischer Reistopf.", [("Rice","g"),("Beef Strips","g"),("Spinach","g"),("Carrot","pcs"),("Gochujang","tbsp")]),
    ("Hummus", "Cremiger Kichererbsendip.", [("Chickpeas","g"),("Tahini","ml"),("Lemon","pcs"),("Garlic","pcs"),("Olive Oil","ml")]),
    ("Chicken Shawarma", "Nahost Hähnchen im Fladenbrot.", [("Chicken Breast","g"),("Pita Bread","pcs"),("Yogurt","ml"),("Cumin","tsp"),("Garlic","pcs")]),
    ("Baklava", "Türkisches Gebäck mit Nüssen.", [("Phyllo Dough","g"),("Walnuts","g"),("Honey","ml"),("Butter","g"),("Cinnamon","tsp")]),
    ("Borscht", "Russische rote Beete Suppe.", [("Beets","g"),("Cabbage","g"),("Potato","pcs"),("Beef Broth","ml"),("Sour Cream","ml")]),
    ("Enchiladas", "Mexikanische gefüllte Tortillas.", [("Tortillas","pcs"),("Chicken Breast","g"),("Enchilada Sauce","ml"),("Cheese","g"),("Sour Cream","ml")]),
    ("Creme Brulee", "Französisches Karamell-Dessert.", [("Cream","ml"),("Egg","pcs"),("Sugar","g"),("Vanilla","tsp")]),
    ("Kimchi Fried Rice", "Koreanischer Kimchi-Reis.", [("Rice","g"),("Kimchi","g"),("Egg","pcs"),("Soy Sauce","ml"),("Sesame Oil","ml")]),
    ("Goulash", "Ungarisches Rindfleischgulasch.", [("Beef","g"),("Onion","pcs"),("Paprika","tsp"),("Tomato Paste","tbsp"),("Beef Broth","ml")]),
    ("Pho", "Vietnamesische Nudelsuppe.", [("Rice Noodles","g"),("Beef Broth","ml"),("Beef Strips","g"),("Bean Sprouts","g"),("Lime","pcs")]),
    ("Eggs Benedict", "Amerikanisches Frühstück.", [("English Muffin","pcs"),("Egg","pcs"),("Canadian Bacon","g"),("Hollandaise Sauce","ml")]),
    ("Dim Sum", "Chinesische Teigtaschen.", [("Dumpling Wrappers","pcs"),("Ground Pork","g"),("Shrimp","g"),("Soy Sauce","ml"),("Ginger","g")]),
    ("Crêpes", "Dünne französische Pfannkuchen.", [("Flour","g"),("Egg","pcs"),("Milk","ml"),("Butter","g"),("Sugar","g")]),
    ("Pulled Pork", "Amerikanisches BBQ Schweinefleisch.", [("Pork Shoulder","g"),("BBQ Sauce","ml"),("Brown Sugar","g"),("Paprika","tsp"),("Garlic Powder","tsp")]),
    ("Tuna Salad", "Leichter Thunfischsalat.", [("Canned Tuna","g"),("Mayonnaise","ml"),("Celery","g"),("Onion","pcs"),("Lemon","pcs")]),
    ("Lentil Soup", "Herzhafte Linsensuppe.", [("Lentils","g"),("Carrot","pcs"),("Onion","pcs"),("Vegetable Broth","ml"),("Cumin","tsp")]),
    ("Tabouli", "Arabischer Petersiliensalat.", [("Parsley","g"),("Bulgur","g"),("Tomatoes","g"),("Lemon","pcs"),("Olive Oil","ml")]),
    ("Butter Chicken", "Indisches Butterhuhn.", [("Chicken Breast","g"),("Butter","g"),("Tomato Sauce","ml"),("Cream","ml"),("Garam Masala","tsp")]),
    ("Spanakopita", "Griechischer Spinatkuchen.", [("Spinach","g"),("Feta Cheese","g"),("Phyllo Dough","g"),("Egg","pcs"),("Onion","pcs")]),
    ("Carbonara", "Pasta mit Speck und Ei.", [("Spaghetti","g"),("Bacon","g"),("Egg","pcs"),("Parmesan","g"),("Black Pepper","tsp")]),
    ("Shrimp Tacos", "Mexikanische Garnelentacos.", [("Shrimp","g"),("Taco Shells","pcs"),("Cabbage","g"),("Lime","pcs"),("Sour Cream","ml")]),
    ("Vegetable Stir Fry", "Schnelles Gemüsegericht.", [("Broccoli","g"),("Bell Pepper","pcs"),("Carrot","pcs"),("Soy Sauce","ml"),("Garlic","pcs")]),
    ("Mango Smoothie", "Frischer Mangosmoothie.", [("Mango","pcs"),("Yogurt","ml"),("Milk","ml"),("Honey","ml"),("Ice","g")]),
    ("Potato Wedges", "Knusprige Kartoffelspalten.", [("Potato","pcs"),("Olive Oil","ml"),("Paprika","tsp"),("Garlic Powder","tsp"),("Salt","tsp")]),
    ("Chicken Noodle Soup", "Klassische Hühnersuppe.", [("Chicken Breast","g"),("Egg Noodles","g"),("Carrot","pcs"),("Celery","g"),("Chicken Broth","ml")]),
    ("Stuffed Peppers", "Gefüllte Paprika.", [("Bell Pepper","pcs"),("Ground Beef","g"),("Rice","g"),("Tomato Sauce","ml"),("Cheese","g")]),
    ("Banana Smoothie", "Cremiger Bananenshake.", [("Banana","pcs"),("Milk","ml"),("Yogurt","ml"),("Honey","ml"),("Ice","g")]),
    ("Chocolate Cake", "Saftiger Schokoladenkuchen.", [("Flour","g"),("Cocoa Powder","g"),("Sugar","g"),("Egg","pcs"),("Butter","g")]),
    ("Avocado Toast", "Trendy Frühstück.", [("Bread","slices"),("Avocado","pcs"),("Lemon","pcs"),("Salt","tsp"),("Red Pepper Flakes","tsp")]),
    ("Tom Yum Soup", "Thailändische Sauersuppe.", [("Shrimp","g"),("Lemongrass","g"),("Mushrooms","g"),("Lime","pcs"),("Chicken Broth","ml")]),
    ("Meatballs", "Saftige Fleischbällchen.", [("Ground Beef","g"),("Egg","pcs"),("Breadcrumbs","g"),("Garlic","pcs"),("Parsley","g")]),
    ("Caprese Salad", "Italienischer Tomaten-Mozzarella Salat.", [("Tomatoes","g"),("Mozzarella","g"),("Basil","g"),("Olive Oil","ml"),("Balsamic Vinegar","ml")]),
    ("Lamb Chops", "Gegrillte Lammkoteletts.", [("Lamb Chops","g"),("Garlic","pcs"),("Rosemary","g"),("Olive Oil","ml"),("Lemon","pcs")]),
    ("Corn Chowder", "Cremige Maissuppe.", [("Corn","g"),("Potato","pcs"),("Onion","pcs"),("Cream","ml"),("Chicken Broth","ml")]),
    ("Granola", "Selbstgemachtes Müsli.", [("Oats","g"),("Honey","ml"),("Nuts","g"),("Dried Fruit","g"),("Coconut Oil","ml")]),
    ("Quesadilla", "Mexikanische Käsetortilla.", [("Tortillas","pcs"),("Cheese","g"),("Bell Pepper","pcs"),("Chicken Breast","g"),("Sour Cream","ml")]),
    ("Gazpacho Blanco", "Weiße Gazpacho.", [("Almonds","g"),("Cucumber","pcs"),("Garlic","pcs"),("Olive Oil","ml"),("Vinegar","ml")]),
    ("Duck Confit", "Französische Entenkeule.", [("Duck Legs","g"),("Garlic","pcs"),("Thyme","tsp"),("Salt","tsp"),("Duck Fat","g")]),
    ("Penne Arrabbiata", "Scharfe Tomatenpasta.", [("Penne","g"),("Tomato Sauce","ml"),("Chili Flakes","tsp"),("Garlic","pcs"),("Olive Oil","ml")]),
    ("Chicken Parmesan", "Überbackenes Hähnchen.", [("Chicken Breast","g"),("Tomato Sauce","ml"),("Mozzarella","g"),("Breadcrumbs","g"),("Parmesan","g")]),
    ("Lobster Bisque", "Cremige Hummerssuppe.", [("Lobster","g"),("Cream","ml"),("Butter","g"),("Onion","pcs"),("Cognac","ml")]),
    ("Fettuccine Alfredo", "Pasta in Sahnesauce.", [("Fettuccine","g"),("Cream","ml"),("Parmesan","g"),("Butter","g"),("Garlic","pcs")]),
    ("Stuffed Mushrooms", "Gefüllte Champignons.", [("Mushrooms","g"),("Cream Cheese","g"),("Garlic","pcs"),("Parsley","g"),("Breadcrumbs","g")]),
    ("Chicken Fajitas", "Mexikanische Hähnchenpfanne.", [("Chicken Breast","g"),("Bell Pepper","pcs"),("Onion","pcs"),("Tortillas","pcs"),("Sour Cream","ml")]),
    ("Beet Salad", "Roter Beete Salat.", [("Beets","g"),("Goat Cheese","g"),("Walnuts","g"),("Arugula","g"),("Balsamic Vinegar","ml")]),
    ("Mushroom Soup", "Cremige Pilzsuppe.", [("Mushrooms","g"),("Onion","pcs"),("Cream","ml"),("Vegetable Broth","ml"),("Thyme","tsp")]),
    ("Salmon Teriyaki", "Japanischer Lachs.", [("Salmon Fillet","g"),("Soy Sauce","ml"),("Honey","ml"),("Ginger","g"),("Garlic","pcs")]),
    ("Greek Salad", "Griechischer Salat.", [("Cucumber","pcs"),("Tomatoes","g"),("Feta Cheese","g"),("Olives","g"),("Red Onion","pcs")]),
    ("Blueberry Muffins", "Saftige Heidelbeermuffins.", [("Flour","g"),("Blueberries","g"),("Sugar","g"),("Egg","pcs"),("Butter","g")]),
    ("Coq au Vin", "Französisches Schmorhuhn.", [("Chicken Legs","g"),("Red Wine","ml"),("Mushrooms","g"),("Bacon","g"),("Onion","pcs")]),
    ("Sushi Rolls", "Japanische Maki Rollen.", [("Sushi Rice","g"),("Nori","pcs"),("Salmon Fillet","g"),("Cucumber","pcs"),("Avocado","pcs")]),
    ("Croissant", "Butteriges französisches Gebäck.", [("Flour","g"),("Butter","g"),("Milk","ml"),("Sugar","g"),("Yeast","tsp")]),
    ("Prawn Cocktail", "Britische Garnelenvorspeise.", [("Shrimp","g"),("Mayonnaise","ml"),("Ketchup","ml"),("Lemon","pcs"),("Lettuce","g")]),
    ("Beef Wellington", "Englisches Rinderfilet.", [("Beef Tenderloin","g"),("Puff Pastry","g"),("Mushrooms","g"),("Dijon Mustard","tbsp"),("Prosciutto","g")]),
    ("Veggie Pizza", "Pizza mit buntem Gemüse.", [("Pizza Dough","g"),("Tomato Sauce","ml"),("Mozzarella","g"),("Bell Pepper","pcs"),("Zucchini","pcs")]),
    ("Chicken Caesar Wrap", "Wrap mit Caesar Salad.", [("Tortillas","pcs"),("Chicken Breast","g"),("Romaine Lettuce","g"),("Parmesan","g"),("Caesar Dressing","ml")]),
    ("Spinach Salad", "Frischer Spinatsalat.", [("Spinach","g"),("Strawberries","g"),("Almonds","g"),("Feta Cheese","g"),("Balsamic Vinegar","ml")]),
    ("Baked Potatoes", "Ofenkartoffeln.", [("Potato","pcs"),("Sour Cream","ml"),("Cheese","g"),("Bacon","g"),("Chives","g")]),
    ("Fruit Salad", "Bunter Obstsalat.", [("Strawberries","g"),("Mango","pcs"),("Kiwi","pcs"),("Banana","pcs"),("Orange","pcs")]),
    ("Miso Soup", "Japanische Misosuppe.", [("Miso Paste","tbsp"),("Tofu","g"),("Seaweed","g"),("Green Onion","g"),("Dashi Stock","ml")]),
    ("Cornbread", "Amerikanisches Maisbrot.", [("Cornmeal","g"),("Flour","g"),("Egg","pcs"),("Milk","ml"),("Butter","g")]),
    ("Beef Rendang", "Indonesisches Schmorrindfleisch.", [("Beef","g"),("Coconut Milk","ml"),("Lemongrass","g"),("Galangal","g"),("Chili","pcs")]),
]

print("Starte Seed...")
for name, description, ingredients in recipes:
    try:
        rid = addRecipe(name, description, None)
        for ingName, ingType in ingredients:
            zid = getOrCreateIngredient(ingName, ingType)
            try:
                addIngredientToRecipe(zid, rid, 1.0)
            except Exception:
                pass
        print(f"✅ {name}")
    except Exception as e:
        print(f"⚠️ {name} übersprungen: {e}")

print("Fertig!")