import copy

class Game:
    def __init__(self, players, options=None):
        self.board = [[0] * 3 for _ in range(3)]
        self.current_player = 1
        self.players = players
        self.game_over = False
        self.winner = None

    def serialize(self):
        return {
            "board": self.board,
            "current_player": self.current_player,
            "game_over": self.game_over,
            "winner": self.winner,
        }

    def deserialize(self, data):
        self.board = data["board"]
        self.current_player = data["current_player"]
        self.game_over = data["game_over"]
        self.winner = data["winner"]

    def get_state(self):
        return {
            "state": self.serialize(),
            "possible_moves": self.get_possible_moves(),
            "current_players": self.players,
        }

    def get_possible_moves(self):
        return [
            {"row": r, "col": c}
            for r in range(3)
            for c in range(3)
            if self.board[r][c] == 0
        ]

    def make_move(self, move):
        if self.game_over:
            return {"error": "Game already over"}
        r, c = move["row"], move["col"]
        if self.board[r][c] != 0:
            return {"error": "Invalid move"}
        self.board[r][c] = self.current_player
        if self.check_win(self.current_player):
            self.game_over = True
            self.winner = self.current_player
        elif not self.get_possible_moves():
            self.game_over = True
            self.winner = 0
        else:
            self.current_player = 3 - self.current_player
        return self.get_state()

    def check_win(self, player):
        b = self.board
        return (
            any([all(b[r][c] == player for c in range(3)) for r in range(3)])
            or any([all(b[r][c] == player for r in range(3)) for c in range(3)])
            or all([b[i][i] == player for i in range(3)])
            or all([b[i][2 - i] == player for i in range(3)])
        )
