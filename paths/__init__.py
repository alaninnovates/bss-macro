from paths.goto import go_to_pine_tree, go_to_stump, go_to_pineapple
from paths.walkfrom import walk_from_pine_tree


def go_to_field(field):
    if field == "Pine Tree":
        go_to_pine_tree()
    elif field == "Stump":
        go_to_stump()
    elif field == "Pineapple":
        go_to_pineapple()


def walk_from_field(field):
    if field == "Pine Tree":
        walk_from_pine_tree()
