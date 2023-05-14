from recipe_repository_interface import Recipe_repository
from recipe import Recipe

class Cookbook:

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

