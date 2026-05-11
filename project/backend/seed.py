from Database import addRecipe, addIngredient, addIngredientToRecipe

# Fresh Pesto Pasta
r1 = addRecipe("Fresh Pesto Pasta", "Classic Italian basil pesto with linguine.", None)
i1 = addIngredient("Linguine", "grams")
i2 = addIngredient("Fresh Basil", "grams")
i3 = addIngredient("Pine Nuts", "grams")
i4 = addIngredient("Parmesan", "grams")
addIngredientToRecipe(i1, r1, 200.0)
addIngredientToRecipe(i2, r1, 50.0)
addIngredientToRecipe(i3, r1, 30.0)
addIngredientToRecipe(i4, r1, 40.0)


# --- 2. Beef Tacos ---
r2 = addRecipe("Beef Tacos", "Street-style seasoned beef tacos.", 302)
i5 = addIngredient("Corn Tortillas", "pieces")
i6 = addIngredient("Ground Beef", "grams")
i7 = addIngredient("Cumin", "teaspoons")
addIngredientToRecipe(i5, r2, 3.0)
addIngredientToRecipe(i6, r2, 150.0)
addIngredientToRecipe(i7, r2, 1.0)

# --- 3. Greek Salad ---
r3 = addRecipe("Greek Salad", "Refreshing cucumber and feta salad.", 303)
i8 = addIngredient("Cucumber", "pieces")
i9 = addIngredient("Feta Cheese", "grams")
i10 = addIngredient("Kalamata Olives", "pieces")
addIngredientToRecipe(i8, r3, 1.0)
addIngredientToRecipe(i9, r3, 100.0)
addIngredientToRecipe(i10, r3, 10.0)

# --- 4. Mushroom Risotto ---
r4 = addRecipe("Mushroom Risotto", "Creamy arborio rice with wild mushrooms.", 304)
i11 = addIngredient("Arborio Rice", "grams")
i12 = addIngredient("Mushrooms", "grams")
i13 = addIngredient("Vegetable Broth", "ml")
addIngredientToRecipe(i11, r4, 150.0)
addIngredientToRecipe(i12, r4, 200.0)
addIngredientToRecipe(i13, r4, 500.0)

# --- 5. French Toast ---
r5 = addRecipe("French Toast", "Brioche soaked in cinnamon egg wash.", 305)
i14 = addIngredient("Brioche Bread", "slices")
i15 = addIngredient("Cinnamon", "teaspoons")
# Reusing 'Egg' and 'Milk' from previous datasets if they exist
addIngredientToRecipe(14, r5, 2.0) # Brioche
addIngredientToRecipe(2, r5, 2.0)  # Egg (zid 2)
addIngredientToRecipe(15, r5, 0.5) # Cinnamon

# --- 6. Margherita Pizza ---
r6 = addRecipe("Margherita Pizza", "Simple pizza with tomato, mozzarella, and basil.", 306)
i16 = addIngredient("Pizza Dough", "grams")
i17 = addIngredient("Mozzarella", "grams")
addIngredientToRecipe(i16, r6, 250.0)
addIngredientToRecipe(i17, r6, 120.0)
addIngredientToRecipe(i2, r6, 10.0) # Basil

# --- 7. Salmon with Asparagus ---
r7 = addRecipe("Baked Salmon", "Lemon-butter salmon with roasted asparagus.", 307)
i18 = addIngredient("Salmon Fillet", "grams")
i19 = addIngredient("Asparagus", "grams")
i20 = addIngredient("Lemon", "pieces")
addIngredientToRecipe(i18, r7, 200.0)
addIngredientToRecipe(i19, r7, 150.0)
addIngredientToRecipe(i20, r7, 0.5)

# --- 8. Chicken Stir-fry ---
r8 = addRecipe("Chicken Stir-fry", "Quick soy-ginger chicken and veggies.", 308)
i21 = addIngredient("Soy Sauce", "ml")
i22 = addIngredient("Ginger", "grams")
i23 = addIngredient("Broccoli", "grams")
addIngredientToRecipe(5, r8, 200.0)  # Chicken Breast (zid 5)
addIngredientToRecipe(i21, r8, 30.0)
addIngredientToRecipe(i22, r8, 10.0)
addIngredientToRecipe(i23, r8, 100.0)

# --- 9. Guacamole ---
r9 = addRecipe("Guacamole", "Chunky avocado dip with lime.", 309)
i24 = addIngredient("Avocado", "pieces")
i25 = addIngredient("Lime Juice", "ml")
addIngredientToRecipe(i24, r9, 3.0)
addIngredientToRecipe(i25, r9, 15.0)
addIngredientToRecipe(4, r9, 0.25) # Salt

# --- 10. Chocolate Chip Cookies ---
r10 = addRecipe("Chocolate Cookies", "Chewy cookies with dark chocolate chips.", 310)
i26 = addIngredient("Chocolate Chips", "grams")
i27 = addIngredient("Vanilla Extract", "ml")
addIngredientToRecipe(1, r10, 250.0)  # Flour
addIngredientToRecipe(14, r10, 150.0) # Butter
addIngredientToRecipe(11, r10, 100.0) # Sugar
addIngredientToRecipe(i26, r10, 100.0)
addIngredientToRecipe(i27, r10, 5.0)

print("Fertig!")