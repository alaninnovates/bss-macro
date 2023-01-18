#  Stumpy Macro - Easy to use macro for Bee Swarm Simulator
#  Copyright (C) 2023 Alan Chen
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from paths.goto import go_to_pine_tree, go_to_stump, go_to_pineapple, go_to_rose
from paths.walkfrom import walk_from_pine_tree


def go_to_field(field):
    if field == "Pine Tree":
        go_to_pine_tree()
    elif field == "Stump":
        go_to_stump()
    elif field == "Pineapple":
        go_to_pineapple()
    elif field == "Rose":
        go_to_rose()


def walk_from_field(field):
    if field == "Pine Tree":
        walk_from_pine_tree()
