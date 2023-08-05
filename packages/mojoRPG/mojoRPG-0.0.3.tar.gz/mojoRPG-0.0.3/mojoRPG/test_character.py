import pytest
from mojoRPG.character import Character

def test_init():
    c = Character("Billy")
    assert c.name == "Billy"
