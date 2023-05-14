from json import JSONEncoder

class RecipeEncoder(JSONEncoder):

    def default(self, obj):
        return obj.__dict__

