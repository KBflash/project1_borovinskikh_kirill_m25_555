import math

from labyrinth_game.constants import COMMANDS, ROOMS

# ---------- Описание комнаты ----------

def describe_current_room(game_state: dict) -> None:
    current_room_id = game_state["current_room"]
    room = ROOMS[current_room_id]

    print(f"\n== {current_room_id.upper()} ==")
    print(room["description"])

    items = room.get("items", [])
    if items:
        print("Заметные предметы:", ", ".join(items))

    exits = ", ".join(room.get("exits", {}).keys())
    print("Выходы:", exits)

    if room.get("puzzle"):
        print("Кажется, здесь есть загадка (команда: solve).")


# ---------- Вспомогательные ----------

def _normalize_answer(text: str) -> str:
    return text.strip().lower()


# ---------- Загадки ----------

def solve_puzzle(game_state: dict) -> None:
    """Попытка решить загадку в текущей комнате."""
    current_room = game_state["current_room"]
    room = ROOMS[current_room]

    if not room.get("puzzle"):
        print("Загадок здесь нет.")
        return

    question, correct_answer = room["puzzle"]
    print(f"🧩 {question}")

    answer = input("Ваш ответ: ")
    norm = _normalize_answer(answer)
    correct = _normalize_answer(correct_answer)

    alternatives = {
        "10": ["десять", "ten"],
        "5": ["пять", "five"],
        "шаг шаг шаг": ["шаг  шаг  шаг"],
    }

    valid_answers = {correct}
    valid_answers.update(alternatives.get(correct, []))

    if norm in valid_answers:
        print("✅ Верно! Загадка решена.")
        room["puzzle"] = None

        if current_room == "trap_room":
            print("Механизм плит отключен — путь безопасен.")
    else:
        print("❌ Неверно. Попробуйте снова.")
        if current_room == "trap_room":
            trigger_trap(game_state)


# ---------- Победа ----------

def attempt_open_treasure(game_state: dict) -> None:
    """Открытие сундука в сокровищнице."""
    current_room = game_state["current_room"]
    room = ROOMS[current_room]

    if current_room != "treasure_room":
        print("Здесь нет сокровищ для открытия.")
        return

    inventory = game_state["player_inventory"]

    if "rusty_key" in inventory:
        print("🔑 Вы используете ключ — замок щёлкает. Сундук открыт!")
        if "treasure_chest" in room["items"]:
            room["items"].remove("treasure_chest")
        print("💰 В сундуке сокровища! Вы победили!")
        game_state["game_over"] = True
        return

    print("Сундук заперт. Можно попробовать ввести код.")
    choice = _normalize_answer(input("Ввести код? (да/нет): "))
    if choice != "да":
        print("Вы отступаете от сундука.")
        return

    puzzle = room.get("puzzle")
    if not puzzle:
        print("Кодовый механизм не найден.")
        return

    _, correct_answer = puzzle
    attempt = _normalize_answer(input("Введите код: "))

    if attempt == _normalize_answer(correct_answer):
        print("✅ Код принят! Сундук открыт!")
        if "treasure_chest" in room["items"]:
            room["items"].remove("treasure_chest")
        print("💰 В сундуке сокровища! Вы победили!")
        game_state["game_over"] = True
    else:
        print("❌ Неверный код. Сундук остаётся заперт.")


# ---------- Справка ----------

def show_help(commands: dict = COMMANDS) -> None:
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"{cmd:<16} - {desc}")


# ---------- Псевдослучайность ----------

def pseudo_random(seed: int, modulo: int) -> int:
    """Псевдослучайное число в диапазоне [0, modulo)."""
    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(frac * modulo)


# ---------- Ловушки ----------

def trigger_trap(game_state: dict) -> None:
    """Срабатывание ловушки."""
    print("⚠️ Ловушка активирована! Пол начал дрожать...")

    inventory = game_state["player_inventory"]

    if inventory:
        idx = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory.pop(idx)
        print(f"💥 Вы потеряли предмет: {lost_item}")
        return

    damage = pseudo_random(game_state["steps_taken"], 10)
    if damage < 3:
        print("💀 Пол провалился под вами... Вы погибли!")
        game_state["game_over"] = True
    else:
        print("😰 Повезло! Вы отделались испугом.")


# ---------- Случайные события ----------

def random_event(game_state: dict) -> None:
    """Редкие случайные события после перемещения."""
    seed = game_state["steps_taken"]

    if pseudo_random(seed, 10) != 0:
        return

    event_type = pseudo_random(seed + 1, 3)
    current_room = game_state["current_room"]
    room = ROOMS[current_room]
    inventory = game_state["player_inventory"]

    if event_type == 0:
        print("💰 На полу блеснула монетка.")
        room.setdefault("items", []).append("coin")

    elif event_type == 1:
        print("👀 В темноте послышался шорох...")
        if "sword" in inventory:
            print("⚔️ Вы показали меч, и существо убежало.")

    else:
        if current_room == "trap_room" and "torch" not in inventory:
            print("🚨 В темноте вы наступили на подозрительную плиту!")
            trigger_trap(game_state)

