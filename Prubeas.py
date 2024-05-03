import csv
import sys

# Agrega las clases Node, StackFrontier y QueueFrontier de util.py
# Asegúrate de que util.py esté en el mismo directorio o en un directorio accesible
from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

directory = "/home/ubuntu/Conexi-n-de-actores/large"

# Load data from CSV files into memory
with open(f"{directory}/people.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        people[row["id"]] = {
            "name": row["name"],
            "birth": row["birth"],
            "movies": set()
        }
        if row["name"].lower() not in names:
            names[row["name"].lower()] = {row["id"]}
        else:
            names[row["name"].lower()].add(row["id"])

# Load movies
with open(f"{directory}/movies.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        movies[row["id"]] = {
            "title": row["title"],
            "year": row["year"],
            "stars": set()
        }

# Load stars
with open(f"{directory}/stars.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            people[row["person_id"]]["movies"].add(row["movie_id"])
            movies[row["movie_id"]]["stars"].add(row["person_id"])
        except KeyError:
            pass

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]

def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

person1 = "marlon brando"
person2 = "john gielgud"
source = person_id_for_name(person1)
if source is None:
    sys.exit("Person not found.")
target = person_id_for_name(person2)
if target is None:
    sys.exit("Person not found.")

# Crear el nodo inicial con el actor fuente
start = Node(state=source, parent=None, action=None)
# Inicializar la frontera con el nodo inicial
frontier = QueueFrontier()
frontier.add(start)
print(frontier)
# Inicializar un conjunto para mantener un registro de los nodos explorados
explored = set()
path = None
print(explored)



"""
# Iterar hasta que la frontera esté vacía
while not frontier.empty():
    # Extraer un nodo de la frontera
    node = frontier.remove()

    # Si el nodo es el objetivo, reconstruir y devolver el camino
    if node.state == target:
        path = []
        while node.parent is not None:
            path.append((node.action, node.state))
            node = node.parent
        path.reverse()
        break  # Salir del bucle mientras

    # Agregar el nodo al conjunto de nodos explorados
    explored.add(node.state)

    # Obtener los vecinos del nodo actual
    neighbors = neighbors_for_person(node.state)

    # Agregar vecinos no explorados a la frontera
    for movie_id, neighbor_person_id in neighbors:
        if not frontier.contains_state(neighbor_person_id) and neighbor_person_id not in explored:
            child = Node(state=neighbor_person_id, parent=node, action=movie_id)
            frontier.add(child)

# Si no se encuentra ningún camino posible
if path is None:
    print("Not connected.")
else:
    degrees = len(path)
    print(f"{degrees} degrees of separation.")
    path = [(None, source)] + path
    for i in range(degrees):
        person1 = people[path[i][1]]["name"]
        person2 = people[path[i + 1][1]]["name"]
        movie = movies[path[i + 1][0]]["title"]
        print(f"{i + 1}: {person1} and {person2} starred in {movie}")
"""
