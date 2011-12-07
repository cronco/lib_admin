from la.models import Genre

class GenreTree:
	
	children = []

	def __init__(self, genre, children = []):

		self.genre = genre
		self.children.extend(children)

def buildGenreTree(parent = 0):
	result = [ GenreTree(x) for x in list(Genre.objects.filter(parent_genre = parent))]
	for genre in result:
		child_list = buildGenreTree(parent = genre.genre.id)
		genre.children = child_list
			#result.insert(i + 1, child_list)
	return result
