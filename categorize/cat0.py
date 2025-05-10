import yaml

# Load the key list from a file
with open("keys.txt", "r", encoding="utf-8") as f:
    keys = [line.strip() for line in f if line.strip()]

# Define categorization logic
def categorize(key):
    words = key.lower().split("_")
    categories = set()

    # Specific rules
    if key.lower().startswith("amanda"):
        categories.add("art")
    if "abstract" in key.lower():
        categories.add("symbol")
    if "aardvark" in key.lower():
        categories.add("animal")
    if "medal" in key.lower():
        categories.add("sport")
        categories.add("symbol")


    animal_keywords = {
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
    }

    category_map = {
        "symbol": ["medal", "achievement", "button", "award", "trophy", "flag", "sign", "mark"],
        "card": ["card", "deck", "joker", "ace", "spades", "hearts", "clubs", "diamonds"],
        "sport": ["football", "tennis", "basketball", "soccer", "cricket", "golf", "badminton"],
        "tool": ["tool", "saw", "hammer", "axe", "knife", "drill", "wrench", "screwdriver"],
        "food": ["food", "drink", "cake", "pizza", "fruit", "meat", "bread", "bottle", "burger", "beer", "wine"],
        "transport": ["car", "truck", "bike", "bus", "train", "plane", "ship", "boat", "tram", "rickshaw"],
        "building": ["building", "house", "castle", "tent", "tower", "temple", "church", "hospital", "airport"],
        "plant": ["tree", "flower", "plant", "leaf", "bush", "algae", "grass", "mushroom", "acorn", "agave", "almond"],
        "person": ["person", "man", "woman", "girl", "boy", "baby", "child", "worker", "soldier"],
        "emotion": ["happy", "sad", "angry", "joy", "cry", "smile", "laugh", "grimace", "emotion", "face"],
        "music": ["music", "guitar", "drum", "violin", "piano", "accordion", "flute"],
        "math": ["math", "equation", "abacus", "number", "digit"],
        "location": ["location", "city", "island", "country", "region", "airport"],
        "event": ["event", "festival", "party", "birthday", "ceremony"],
        "nature": ["sun", "moon", "sky", "cloud", "rain", "ocean", "wind", "earth"],
        "role": ["king", "queen", "leader", "advisor", "scientist"],
        "accessory": ["hat", "glasses", "watch", "jewelry", "tie", "necklace"],
        "game": ["VP","game", "board", "dice", "chess", "meeple", "domino"],
        "gesture": ["hand", "fist", "wave", "pointing", "thumb"],
        "clothing": ["shirt", "pants", "skirt", "shoes", "dress", "cape"],
        "technology": ["computer", "phone", "chip", "robot", "device", "camera", "screen"]
    }
    known_first_names = {
      "aaron", "abraham", "alfred", "amanda", "annabel", "anna", "charlene", "donald",
      "elizabeth", "gilbert", "john", "jason", "hanna", "lili", "lauren", "luis"
    }
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

    return list(categories)

# Generate dictionary
categorized = {key: categorize(key) for key in keys}

# Write to YAML file
with open("cats_final.yaml", "w", encoding="utf-8") as out:
    yaml.dump(categorized, out, allow_unicode=True)

print("Saved to cats_final.yaml")
