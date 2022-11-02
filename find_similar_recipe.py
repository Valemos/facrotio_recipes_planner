from factorio.game_environment.game_environment import GameEnvironment

env = GameEnvironment.load_default()

# %%
env.recipe_collection.search_maximum_similar_name('big electric motor')
