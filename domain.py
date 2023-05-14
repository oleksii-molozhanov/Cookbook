# Application + Domain
# For complex domains it is beneficial to separate Application services and Domain objects.
# Currently this code is simple enogh to keep things coupled.

class Recipe:

	_default_ingredients = ["Only love is needed"]
	_spacing = "    "

	
	def __init__(self, name: str, description = "" , ingredients = []):
		self.name = name
		self.description = description
		self.ingredients = ingredients
		print(f"New recipe created: {self.name}")
		return

	# For easy json decoding
	def __init__(self, name: str, description = "" , _ingredients = []):
		self.name = name
		self.description = description
		self.ingredients = _ingredients
		print(f"New recipe created: {self.name}")
		return


	@property
	def ingredients(self):
		return self._ingredients if len(self._ingredients) > 0 else self._default_ingredients


	@ingredients.setter
	def ingredients(self, value):
		self._ingredients = value


	# This is a converter function that ideally deserves a separate place/file
	def pretty(self) -> str:
		result = f"""Receipt: {self.name}
    {self.description}
Ingredients ({len(self.ingredients)}):
"""
		result += '\n'.join( Recipe._spacing + x for x in self.ingredients)
		return result



from abc import ABC, abstractmethod

class Recipe_repository(ABC):

	@abstractmethod
	def persist(self, recipe: Recipe) -> None:
		pass


	@abstractmethod
	def retrieve(self, key: str) -> Recipe:
		pass


	@abstractmethod
	def retrieve_all(self) -> list[Recipe]:
		pass


	@abstractmethod
	def move_to_removed(self, key: str) -> None:
		pass




import os
import json
from encoders import RecipeEncoder
import datetime

class Cookbook:

	_recipe_persistance_location = os.environ.get("RECIPES_FOLDER_PATH") or "recipes/"
	_recipe_persistance_removed_location = os.environ.get("RECIPES_REMOVED_FOLDER_PATH") or "recipes/removed/"	


	def __init__(self, recipe_repository: Recipe_repository):
		# This is actually a cache. Repo should probably be used directly instead
		self._recipe_list = {}
		self._repo = recipe_repository		

		existing = self._repo.retrieve_all()
		for r in existing: self._add_recipe(r)
		

	@property
	def recipe_list(self):
		return self._recipe_list


	def add_new_recipe(self, name: str, description = "" , ingredients = []) -> Recipe:
		if(name in self.recipe_list.keys()): raise DuplicateKeyError(f"Recipe exists: {name}")

		new_r = Recipe(name, description, ingredients)
		self._add_recipe(new_r)
		self._repo.persist(new_r)
		return new_r


	def _add_recipe(self, recipe: Recipe) -> None:
		if(recipe.name in self.recipe_list.keys()): raise DuplicateKeyError(f"Recipe exists: {recipe.name}")

		self.recipe_list[recipe.name] = recipe
		print(f"Recipe {recipe.name} added to cookbook for a total of {len(self.recipe_list)} recipes")



	# This is a converter function that ideally deserves a separate place/file
	def list_known_recipes(self) -> str:
		if( len(self.recipe_list) == 0 ): return "No known recipes, only wind blows here"

		return "Known recipes:\n" + "\n".join( Recipe._spacing + r.name for r in self.recipe_list.values())			


	def get_recipe(self, name: str) -> Recipe:
		return self.recipe_list[name]


	def remove_recipe(self, name: str) -> None:
		self.recipe_list.pop(name)
		self._repo.move_to_removed(name)



class DuplicateKeyError(Exception): pass

