# labyrinth_game/constants.py

ROOMS = {
    "entrance": {
        "description": (
            "Вы у входа в лабиринт. Сырость и мох. На полу виден старый факел."
        ),
        "items": ["torch"],
        "exits": {"north": "hall", "east": "library"},
        "puzzle": None,
    },
    "hall": {
        "description": (
            "Большой зал с колоннами. На пьедестале запечатанный сундук."
        ),
        "items": [],
        "exits": {"south": "entrance", "west": "trap_room", "north": "treasure_room"},
        "puzzle": (
            "Надпись: 'Число после девяти?' Введите цифрой или словом.",
            "10",
        ),
    },
    "library": {
        "description": (
            "Тихая библиотека с древними книгами. Пахнет пылью и деревом."
        ),
        "items": ["bronze_box"],
        "exits": {"west": "entrance"},
        "puzzle": ("Сколько пальцев на одной руке? Введите цифрой.", "5"),
    },
    "trap_room": {
        "description": (
            "Комната с чистым полом. Похоже, тут спрятан механизм ловушки."
        ),
        "items": [],
        "exits": {"east": "hall"},
        "puzzle": (
            "Скажите слово 'шаг' три раза (введите: 'шаг шаг шаг').",
            "шаг шаг шаг",
        ),
    },
    "treasure_room": {
        "description": (
            "Сокровищница. Перед вами массивный сундук, весь в камнях."
        ),
        "items": ["treasure_chest"],
        "exits": {"south": "hall"},
        "puzzle": ("Код замка. Подсказка: 2 * 5 = ?", "10"),
    },
}

# --- constants for part 3 (no magic numbers) ---
EVENT_PROBABILITY = 10
TRAP_DEATH_THRESHOLD = 3

# --- commands for help ---
COMMANDS = {
    "go <direction>": "идти: north / south / east / west",
    "north": "короткая форма для 'go north'",
    "south": "короткая форма для 'go south'",
    "east": "короткая форма для 'go east'",
    "west": "короткая форма для 'go west'",
    "look": "осмотреть комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет",
    "inventory": "показать инвентарь",
    "solve": "решить загадку или открыть сундук",
    "help": "показать эту справку",
    "quit": "выйти из игры",
}
