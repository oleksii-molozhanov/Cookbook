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



import os
import json
from encoders import RecipeEncoder
import datetime

class Cookbook:

	_recipe_persistance_location = os.environ.get("RECIPES_FOLDER_PATH") or "recipes/"
	_recipe_persistance_removed_location = os.environ.get("RECIPES_REMOVED_FOLDER_PATH") or "recipes/removed/"	


	def __init__(self):
		self._recipe_list = {}

		Cookbook._make_dir_if_absent(Cookbook._recipe_persistance_location)
		Cookbook._make_dir_if_absent(Cookbook._recipe_persistance_removed_location)

		existing = Cookbook._retrieve_all()
		for r in existing: self._add_recipe(r)
		

	@property
	def recipe_list(self):
		return self._recipe_list


	def add_new_recipe(self, name: str, description = "" , ingredients = []) -> Recipe:
		if(name in self.recipe_list.keys()): raise DuplicateKeyError(f"Recipe exists: {name}")

		new_r = Recipe(name, description, ingredients)
		self._add_recipe(new_r)
		Cookbook._store(new_r)		
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
		Cookbook._rename_persistant_copy(name)


	def _store(recipe: Recipe) -> None:
		file_name = Cookbook._recipe_persistance_location + recipe.name + ".json"
		content = json.dumps(recipe, cls=RecipeEncoder)		
		with open(file_name, 'w') as file:
			file.write(content)

		print(f"Recipe {recipe.name} was written to: {file_name}")


	def _rename_persistant_copy(name: str) -> None:
		full_path = os.path.join(Cookbook._recipe_persistance_location, f"{name}.json")
		if os.path.isfile(full_path):
			new_path = os.path.join(Cookbook._recipe_persistance_removed_location, f"removed_{name}_{int(datetime.datetime.now().timestamp())}.json")
			os.rename(full_path, new_path)


	def _retrieve_all():
		recipes = []
		for path in os.listdir(Cookbook._recipe_persistance_location):			
			full_path = os.path.join(Cookbook._recipe_persistance_location, path)
			if os.path.isfile(full_path):
				# Ignore system files
				if path[0] == ".": continue

				with open(full_path) as file:
					recipe = Recipe(**json.loads(file.read()))
					recipes.append(recipe)

		return recipes


	def _make_dir_if_absent(path: str) -> None:
		if not os.path.exists(path): os.makedirs(path)


class DuplicateKeyError(Exception): pass

