#!/usr/bin/env python3

from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Recipe, User

fake = Faker()

with app.app_context():

    print("Deleting all records...")
    Recipe.query.delete()
    User.query.delete()

    fake = Faker()

    print("Creating users...")

users = []
usernames = []

for i in range(20):
    username = fake.first_name()
    while not username or username in usernames:
        username = fake.first_name()
    usernames.append(username)

    user = User(
        username=username,
        bio=fake.paragraph(nb_sentences=3),
        image_url=fake.url(),
    )

    # ✅ Securely hash password
    user.password_hash = username + 'password'

    # ✅ Debug check
    if not user._password_hash:
        print(f"[DEBUG] MISSING PASSWORD for user: {username}")

    users.append(user)

# ✅ Filter out any with missing hash (just in case)
valid_users = [user for user in users if user._password_hash]
db.session.add_all(valid_users)

print("Creating recipes...")
recipes = []
for i in range(100):
    instructions = fake.paragraph(nb_sentences=8)
    
    recipe = Recipe(
        title=fake.sentence(),
        instructions=instructions,
        minutes_to_complete=randint(15,90),
    )

    recipe.user = rc(users)

    recipes.append(recipe)

db.session.add_all(recipes)

db.session.commit()

print("Complete.")
