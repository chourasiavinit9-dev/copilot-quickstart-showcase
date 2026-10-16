import pytest
from adventure_game import Player, STORY_NODES, play_game


def test_player_initial_state():
    p = Player("Neo")
    assert p.name == "Neo"
    assert p.hp == 100
    assert p.stealth == 80
    assert p.credits == 250
    assert "Cyberdeck Mk-II" in p.inventory
    assert p.is_alive() is True


def test_player_damage_and_healing():
    p = Player("Trinity")
    p.take_damage(30)
    assert p.hp == 70
    p.heal(20)
    assert p.hp == 90
    p.heal(50)  # Capped at 100
    assert p.hp == 100
    p.take_damage(150)  # Floor at 0
    assert p.hp == 0
    assert p.is_alive() is False


def test_player_inventory_operations():
    p = Player("Morpheus")
    assert p.add_item("Red Pill") is True
    assert p.add_item("Red Pill") is False  # No duplicates
    assert p.has_item("Red Pill") is True
    assert p.remove_item("Red Pill") is True
    assert p.has_item("Red Pill") is False
    assert p.remove_item("Nonexistent") is False


def test_story_nodes_integrity():
    assert "start" in STORY_NODES
    for node_key, data in STORY_NODES.items():
        assert "text" in data
        if not data.get("ending"):
            assert "options" in data, f"Node {node_key} must have options"
            assert len(data["options"]) > 0
            for text, next_node in data["options"]:
                assert next_node in STORY_NODES, f"Invalid target node {next_node} from {node_key}"


def test_game_flow_architect_ending():
    hero = Player("Ghost")
    # Path: start -> vent_shaft (1) -> drone_hack (2) -> server_corridor (1) -> keycard_pass (1) -> ai_core_antechamber (1) -> ending_architect (2)
    inputs = ["1", "2", "1", "1", "1", "2"]
    result = play_game(hero, mock_inputs=inputs)
    assert result == "ending_architect"
    assert hero.is_alive() is True


def test_game_flow_death_game_over():
    hero = Player("Rookie")
    hero.hp = 10
    # vent_shaft option 1 causes 20 damage -> hp becomes 0
    inputs = ["1", "1"]
    result = play_game(hero, mock_inputs=inputs)
    assert result == "game_over"
    assert hero.is_alive() is False
