from settings import CookRegion
from settings import FoodRecipe
from settings import HSRegion
from settings import ServeRegion
from settings import TextRegions
from settings import WindowGame


def test():
    assert len(WindowGame) == 4
    assert len(HSRegion) == 4
    assert len(ServeRegion) == 4
    assert len(CookRegion) == 4
    assert len(TextRegions) == 4
    assert len(FoodRecipe) == 4
