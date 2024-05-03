import csv
import sys

from util import Node, StackFrontier, QueueFrontier

directory = "/home/ubuntu/Conexi-n-de-actores/small"
# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)

people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}
# Load people
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
xx ="tom cruise"
pru = neighbors_for_person(xx)
print(pru)

