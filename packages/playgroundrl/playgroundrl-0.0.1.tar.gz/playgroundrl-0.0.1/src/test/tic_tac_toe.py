from client import PlaygroundClient
import random, math
import json


# The following line are an example of how to use the API
class TestTicTacToe(PlaygroundClient):
    def __init__(self, endpoint="http://44.205.255.44:8083"):
        super().__init__(
            "tic_tac_toe",
            model_name="tic_tac_toe_robot" + str(random.randrange(100, 1000)),
            endpoint=endpoint,
            max_exchange=5000,
            game_type=2,
        )

    def callback(self, state, reward):
        # Todo: After talking with Rayan
        # move this to JSON and user to checking to super class
        state = json.loads(state)
        user = state["player_moving"]
        board = state["board"]

        if user != self.user_id:
            return None

        for i in range(0, 3):
            for j in range(0, 3):
                if board[i][j] == 0:
                    # Choose first open state
                    return str(i * 3 + j)

    def gameover_callback(self):
        pass


endpoint = "http://127.0.0.1:8083/"
t = TestTicTacToe(endpoint=endpoint)
t.run()
