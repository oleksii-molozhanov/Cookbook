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