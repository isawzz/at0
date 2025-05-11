import yaml

# Load the key list from a file
with open("keys.txt", "r", encoding="utf-8") as f:
    keys = sorted([line.strip() for line in f if line.strip()])  # Sort keys alphabetically

# Define categorization logic
def categorize(key):
    words = key.lower().split("_")
    categories = set()

    # Specific rules
    if key.lower().startswith("amanda"):
        categories.add("art")
    if "abstract" in key.lower():
        categories.add("symbol")
    if "airport" in key.lower():
        categories.add("location")
    if "aardvark" in key.lower():
        categories.add("animal")
    if "medal" in key.lower():
        categories.add("sport")
        categories.add("symbol")

    animal_keywords = [
        "aardvark", "badger", "bat", "beaver", "bison", "boar", "buffalo", "camel", "cat", "chameleon", "chicken",
        "cow", "crab", "crocodile", "deer", "dinosaur", "dog", "dolphin", "donkey", "duck", "eagle", "elephant",
        "falcon", "ferret", "flamingo", "fox", "frog", "giraffe", "goat", "goose", "gorilla", "hamster", "hare",
        "hawk", "hedgehog", "hippopotamus", "horse", "hound", "hyena", "ibis", "iguana", "jaguar", "kangaroo", "koala",
        "lemur", "leopard", "lion", "llama", "lobster", "lynx", "macaw", "mammoth", "manatee", "meerkat", "mink", "mole",
        "monkey", "moose", "mouse", "mule", "narwhal", "newt", "ocelot", "octopus", "opossum", "orangutan", "ostrich",
        "otter", "owl", "ox", "panda", "panther", "parrot", "peacock", "pelican", "penguin", "pig", "pigeon",
        "platypus", "porcupine", "possum", "puma", "rabbit", "raccoon", "ram", "rat", "raven", "reindeer", "rhinoceros",
        "rooster", "salamander", "seal", "shark", "sheep", "skunk", "sloth", "snail", "snake", "sparrow", "squid",
        "squirrel", "starfish", "stingray", "stork", "swan", "tiger", "toad", "turkey", "turtle", "vulture", "walrus",
        "warthog", "wasp", "weasel", "whale", "wildcat", "wolf", "wolverine", "wombat", "woodpecker", "yak", "zebra"
    ]

    category_map = {
        "accessory": ["glasses", "hat", "jewelry", "necklace", "tie", "watch"],
        "animal": animal_keywords,
        "building": ["airport", "building", "castle", "church", "hospital", "house", "temple", "tent", "tower"],
        "card": ["ace", "card", "clubs", "deck", "diamonds", "hearts", "joker", "spades"],
        "clothing": ["cape", "dress", "pants", "shirt", "shoes", "skirt"],
        "emotion": ["angry", "cry", "emotion", "face", "grimace", "happy", "joy", "laugh", "sad", "smile"],
        "event": ["birthday", "ceremony", "event", "festival", "party"],
        "food": ["beer", "bottle", "bread", "burger", "cake", "drink", "fruit", "meat", "pizza", "wine"],
        "game": ["VP", "board", "chess", "dice", "domino", "game", "meeple"],
        "gesture": ["fist", "hand", "pointing", "thumb", "wave"],
        "location": ["airport", "city", "country", "island", "location", "region"],
        "math": ["abacus", "digit", "equation", "math", "number"],
        "music": ["accordion", "drum", "flute", "guitar", "music", "piano", "violin"],
        "nature": ["cloud", "earth", "moon", "ocean", "rain", "sky", "sun", "wind"],
        "person": ["baby", "boy", "child", "girl", "man", "person", "soldier", "woman", "worker"],
        "plant": ["acorn", "agave", "algae", "almond", "bush", "flower", "grass", "leaf", "mushroom", "plant", "tree"],
        "role": ["advisor", "king", "leader", "queen", "scientist"],
        "sport": ["badminton", "basketball", "cricket", "football", "golf", "soccer", "tennis"],
        "symbol": ["achievement", "award", "button", "flag", "mark", "medal", "sign", "trophy"],
        "technology": ["camera", "chip", "computer", "device", "phone", "robot", "screen"],
        "tool": ["axe", "drill", "hammer", "knife", "saw", "screwdriver", "tool", "wrench"],
    }
    known_first_names = [
        "aaron", "abraham", "alfred", "amanda", "annabel", "anna", "charlene", "donald",
        "elizabeth", "gilbert", "hanna", "jason", "john", "lauren", "lili", "luis"
    ]

    # Check animal first
    if any(word in animal_keywords for word in words):
        categories.add("animal")
    if any(word in known_first_names for word in words):
        categories.add("user")

    # Add from category_map
    for cat, terms in category_map.items():
        if any(word in terms for word in words):
            categories.add(cat)

    # Fallback if empty
    if not categories:
        categories.add("object")

    return sorted(list(categories))  # Sort categories alphabetically

# Generate dictionary
categorized = {key: categorize(key) for key in keys}

# Write to YAML file
with open("cats_final.yaml", "w", encoding="utf-8") as out:
    yaml.dump(dict(sorted(categorized.items())), out, allow_unicode=True)  # Sort keys alphabetically

print("Saved to cats_final.yaml")