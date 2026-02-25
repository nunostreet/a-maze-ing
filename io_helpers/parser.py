import sys
from typing import Any


def parser() -> dict[str, Any] | None:
    """Parse the configuration file and return a dictionary.

    Returns:
        dict: Configuration dictionary with validated values.
        None: If an error occurs.
    """
    mand_keys = {'HEIGHT',
                 'WIDTH',
                 'ENTRY',
                 'EXIT',
                 'OUTPUT_FILE',
                 'PERFECT',
                 'SEED',
                 }
    algorithms = {
                'DFS',
                'PRIM'
            }
    exist_keys: set[str] = set()

    try:
        if len(sys.argv) == 1:
            raise ValueError("Not enough arguments")
        if len(sys.argv) > 2:
            raise ValueError("Too many arguments")
        if not (sys.argv[1].endswith('.txt')):
            raise ValueError("Argument has to be a file")
        else:
            with open(sys.argv[1]) as file:

                lines = file.readlines()
                dictionary: dict[str, Any] = {}

                for line in lines:
                    words = line.strip()
                    if len(words) == 0:
                        continue
                    else:
                        if words[0] == '#':
                            continue
                        if '=' in words:
                            parts = words.split("=", 1)
                            key = parts[0]
                            value = parts[1]
                            dictionary[key] = value
                            exist_keys.add(key)
                        else:
                            raise TypeError("Invalid Syntax")

                if all(keys in dictionary for keys in mand_keys):

                    # height
                    value = dictionary['HEIGHT']
                    try:
                        height = int(value)
                    except ValueError:
                        raise ValueError("HEIGHT must be an integer")
                    if height <= 0:
                        raise ValueError("HEIGHT must be a positive integer")
                    dictionary['HEIGHT'] = height

                    # width
                    value = dictionary['WIDTH']
                    try:
                        width = int(value)
                    except ValueError:
                        raise ValueError("WIDTH must be an integer")
                    if width <= 0:
                        raise ValueError("WIDTH must be a positive integer")
                    dictionary['WIDTH'] = width

                    # entry
                    value = dictionary['ENTRY']
                    entries = value.split(",")
                    if len(entries) != 2:
                        raise ValueError("ENTRY must only have an x, y")
                    else:
                        try:
                            x = int(entries[0])
                            y = int(entries[1])
                        except ValueError:
                            raise ValueError("ENTRY must only be an integer")
                        if x < 0 or y < 0:
                            raise ValueError(
                                "ENTRY must be a positive integer")
                    dictionary['ENTRY'] = (x, y)

                    if x >= dictionary['WIDTH'] or y >= dictionary['HEIGHT']:
                        raise ValueError("ENTRY is outside the maze bounds")

                    # exit
                    value = dictionary['EXIT']
                    exits = value.split(",")
                    if len(exits) != 2:
                        raise ValueError("EXIT must only have an x, y")
                    else:
                        try:
                            x = int(exits[0])
                            y = int(exits[1])
                        except ValueError:
                            raise ValueError("EXIT must only be an integer")
                        if x < 0 or y < 0:
                            raise ValueError("EXIT must be a positive integer")
                    dictionary['EXIT'] = (x, y)

                    # verificar que não sai para fora do maze
                    if x >= dictionary['WIDTH'] or y >= dictionary['HEIGHT']:
                        raise ValueError("EXIT is outside the maze bounds")

                    # verificar que entry e exit são diferentes
                    if dictionary['ENTRY'] == dictionary['EXIT']:
                        raise ValueError(
                            "ENTRY and EXIT must have different values")

                    # output_file
                    value = dictionary['OUTPUT_FILE']
                    if len(value) == 0:
                        raise ValueError("OUTPUT_FILE cannot be empty")
                    if not value.endswith('.txt'):
                        raise ValueError("OUTPUT_FILE must be a '.txt' file")
                    dictionary['OUTPUT_FILE'] = value

                    # perfect
                    value = dictionary['PERFECT']
                    if value != 'True' and value != 'False':
                        raise ValueError(
                            'PERFECT can only have True or False values')
                    dictionary['PERFECT'] = value == 'True'

                    # seed
                    value = dictionary['SEED']
                    try:
                        seed = int(value)
                    except ValueError:
                        raise ValueError("SEED must be an integer")
                    dictionary['SEED'] = seed

                    # cycle_density
                    if 'CYCLE_DENSITY' in dictionary:
                        try:
                            cyc_density = float(dictionary['CYCLE_DENSITY'])
                            if not (0.0 <= cyc_density <= 0.3):
                                raise ValueError(
                                    "CYCLE_DENSITY must be between 0.0 and 0.3"
                                    )
                            dictionary['CYCLE_DENSITY'] = cyc_density
                        except ValueError as e:
                            if "between" in str(e):
                                raise e
                            raise ValueError("CYCLE_DENSITY must be a float")

                    # algorithms
                    if 'ALGORITHM' in dictionary:
                        try:
                            algo = dictionary['ALGORITHM'].strip().upper()
                            if algo not in algorithms:
                                raise ValueError(
                                    f"Unknown algorithm: {algo}")
                        except Exception as e:
                            raise ValueError(e)

                    return dictionary
                else:
                    missing = mand_keys - exist_keys
                    print(f"Missing Keys: {missing}")
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(e)
    return None
