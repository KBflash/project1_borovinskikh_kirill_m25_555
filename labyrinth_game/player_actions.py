
from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def get_input(prompt: str = "> ") -> str:
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state: dict, direction: str) -> None:
    current = game_state["current_room"]
    room = ROOMS[current]

    if direction not in room["exits"]:
        print("Нельзя пойти в этом направлении.")
        return

    next_room = room["exits"][direction]

    if (
        next_room == "treasure_room"
        and "rusty_key" not in game_state["player_inventory"]
        ):
        print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        return

    game_state["current_room"] = next_room
    game_state["steps_taken"] += 1

    describe_current_room(game_state)
    random_event(game_state)


def take_item(game_state: dict, item_name: str) -> None:
    room = ROOMS[game_state["current_room"]]

    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in room["items"]:
        room["items"].remove(item_name)
        game_state["player_inventory"].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def show_inventory(game_state: dict) -> None:
    inv = game_state["player_inventory"]

    if inv:
        print("Инвентарь:")
        for item in inv:
            print(f"- {item}")
    else:
        print("Инвентарь пуст.")


def use_item(game_state: dict, item_name: str) -> None:
    inv = game_state["player_inventory"]

    if item_name not in inv:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Вы зажгли факел. Стало светлее.")
    elif item_name == "sword":
        print("С мечом вы чувствуете себя увереннее.")
    elif item_name == "bronze_box":
        print("Вы открыли бронзовую шкатулку.")
        if "rusty_key" not in inv:
            inv.append("rusty_key")
            print("Внутри оказался ржавый ключ.")
        else:
            print("Шкатулка пуста.")
    else:
        print("Вы не знаете, как использовать этот предмет.")



