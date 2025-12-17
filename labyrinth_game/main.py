
#!/usr/bin/env python3

from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state: dict, command: str) -> None:
    parts = command.strip().split()
    if not parts:
        return

    action = parts[0]

    if action in {"north", "south", "east", "west"}:
        move_player(game_state, action)
        return

    match action:
        case "go":
            if len(parts) < 2:
                print("Укажите направление.")
            else:
                move_player(game_state, parts[1])
        case "look":
            describe_current_room(game_state)
        case "take":
            if len(parts) < 2:
                print("Укажите предмет.")
            else:
                take_item(game_state, parts[1])
        case "use":
            if len(parts) < 2:
                print("Укажите предмет.")
            else:
                use_item(game_state, parts[1])
        case "inventory":
            show_inventory(game_state)
        case "solve":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "help":
            show_help()
        case "quit" | "exit":
            game_state["game_over"] = True
        case _:
            print("Неизвестная команда. Попробуйте снова.")


def main() -> None:
    print("Первая попытка запустить проект!")
    print("Добро пожаловать в Лабиринт сокровищ!")

    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0,
    }

    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = get_input("> ")
        process_command(game_state, command)


if __name__ == "__main__":
    main()


