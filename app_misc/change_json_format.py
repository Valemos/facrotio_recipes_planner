import json
from pathlib import Path

from factorio.types.recipes_collection import RecipesCollection

edit_file_path = Path("../recipes/recipes.json")

with edit_file_path.open("r") as fin:
    j = json.load(fin)

    # for composite in j["composite"]:
    #     composite["results"] = composite["products"]
    #     del composite["products"]

    rec = RecipesCollection.from_json(j)

    j = rec.to_json()

    with edit_file_path.open("w") as fout:
        json.dump(j, fout)
