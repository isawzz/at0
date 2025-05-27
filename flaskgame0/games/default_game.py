import os

class Game:
    def __init__(self, players, options):
        self.players = players
        self.options = options
        self.state = {}

    def serialize(self):
        return self.state

    def deserialize(self, state):
        self.state = state

    def make_move(self, move):
        return {"message": f"Move received: {move}"}

    def get_state(self):
        return {
            "possible_moves": self.get_possible_moves(),
            "players": self.players,
            "options": self.options,
            "state": self.state,
        }

    def get_possible_moves(self):
        routes = [
            "/",
            "/help",
            "/start_game",
            "/game_state/<game_id>",
            "/make_move/<game_id>",
            "/save_game/<game_id>",
            "/load_game/<game_id>",
            "/delete_game/<game_id>",
            "/get_tables",
            "/get_table_names",
        ]

        saved_ids = [
            fname.rsplit(".", 1)[0]
            for fname in os.listdir("saved_games")
            if fname.endswith(".json")
        ]

        moves = []

        for route in routes:
            if "<game_id>" in route:
                for gid in saved_ids:
                    moves.append(route.replace("<game_id>", gid))
            elif route == "/start_game":
                # Suggest starting each game
                game_files = [
                    fname.rsplit(".", 1)[0]
                    for fname in os.listdir("games")
                    if fname.endswith(".py") and not fname.startswith("__")
                ]
                for game in game_files:
                    moves.append(f"/start_game?gamename={game}")
            else:
                moves.append(route)

        return moves
