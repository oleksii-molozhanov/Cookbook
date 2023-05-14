from abc import ABC, abstractmethod
from recipe import Recipe

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