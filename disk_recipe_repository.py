from domain import Recipe_repository
from recipe import Recipe
import os
import json
from encoders import RecipeEncoder
from datetime import datetime

class Repo(Recipe_repository):

	_storage_folder_path = os.environ.get("RECIPES_FOLDER_PATH") or "recipes/"
	_removed_storage_folder_path = os.environ.get("RECIPES_REMOVED_FOLDER_PATH") or "recipes/removed/"	


	def __init__(self):
		Repo._make_dir_if_absent(Repo._storage_folder_path)
		Repo._make_dir_if_absent(Repo._removed_storage_folder_path)


	def persist(self, recipe: Recipe) -> None:
		file_name = Repo._storage_folder_path + recipe.name + ".json"
		content = json.dumps(recipe, cls=RecipeEncoder)		
		with open(file_name, 'w') as file:
			file.write(content)

		print(f"Recipe {recipe.name} was written to: {file_name}")


	def retrieve(self, key: str) -> Recipe:
		print(f"Recipe {key} retrieved")


	def retrieve_all(self) -> list[Recipe]:
		recipes = []
		for path in os.listdir( Repo._storage_folder_path ):
			full_path = os.path.join( Repo._storage_folder_path, path )
			if os.path.isfile(full_path):
				# Ignore system files
				if path[0] == ".": continue

				with open(full_path) as file:
					recipe = Recipe(**json.loads(file.read()))
					recipes.append(recipe)

		return recipes


	def move_to_removed(self, key: str) -> None:
		full_path = os.path.join(Repo._storage_folder_path, f"{key}.json")
		if os.path.isfile(full_path):
			new_path = os.path.join(Repo._removed_storage_folder_path, f"removed_{key}_{int(datetime.now().timestamp())}.json")
			os.rename(full_path, new_path)


	def _make_dir_if_absent(path: str) -> None:
		if not os.path.exists(path): os.makedirs(path)