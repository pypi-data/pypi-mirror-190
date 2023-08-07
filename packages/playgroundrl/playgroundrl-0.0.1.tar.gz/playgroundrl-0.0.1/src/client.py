import socketio
from abc import ABC, abstractmethod
import random


# TODO: Handle retrying and what happens if we never receive a message back ()
# TODO: Turn print statements into logging statements
# TODO: Turn Dict messages into classes
# TODO: Kill the client better, sometimes it hangs
class PlaygroundClient(ABC):
    def __init__(
        self,
        game,
        model_name,
        training=False,
        game_type=1,  # must be 1 or 2
        endpoint="http://44.205.255.44:8083",
        max_exchange=20,
    ):
        """
        An API to handle one game.
        """

        print("Connecting....")
        self.sio = socketio.Client()
        self.user_id = "sample_id" + str(random.randrange(100, 1000))
        auth = {"token": "brrrlin", "user_id": self.user_id, "api_key": "400"}

        self.sio.connect(endpoint, auth=auth, namespaces=["/"])
        self.register_handlers()
        print("Connected!")

        self.game = game
        self.model_name = model_name
        self.training = training
        self.game_type = game_type

        # Temporary variable to limit number of messages received
        # Todo: Find a more elegant solution to prevent infinite loops
        self.max_exchange = max_exchange
        self.exchanged = 0

    def register_handlers(self):
        self.sio.on("state_msg", lambda msg: self._on_state_msg(msg))
        # this now happens by default, when the state updatd correctly
        self.sio.on("ack", lambda msg: self._on_action_ack_msg(msg))
        self.sio.on("game_over", lambda msg: self._on_game_over_msg(msg))
        self.sio.on("send_game_id", lambda msg: self._on_send_game_id_msg(msg))
        self.sio.on("exception", lambda msg: self._on_error_msg(msg))
        self.sio.on("*", lambda type, msg: self._default_callback(self, type, msg))

    @abstractmethod
    def callback(self, state: str, reward: str) -> str:
        """
        Instances implement this with their RL strategies.
        Returns the action for the client to take,
        or none for no action.
        """
        # TODO: Make self, state, and reward proper objects
        pass

    @abstractmethod
    def gameover_callback(self):
        """Run some action when the game ends"""
        pass

    def _on_state_msg(self, msg):
        print(" --state_msg received: ", msg)
        state = msg["state"]
        reward = msg["reward"]
        is_game_over = msg["is_game_over"]
        if is_game_over or self.exchanged > self.max_exchange:
            print(
                "Game is over or max number of messages has been reached, disconnecting..."
            )
            self.gameover_callback()
            self.sio.disconnect()
            return

        # Use user defined function to determine callback
        action = self.callback(state, reward)
        if action is not None:
            payload = {"action": action, "game_id": self.game_id}
            print(" -- sending action: ", action)
            self.sio.emit("submit_agent_action", payload)

        self.exchanged += 1

    def _on_action_ack_msg(self, msg):
        print(" --ack message received", msg)
        # self.sio.emit('get_state', {'game_id': self.game_id})

    # TODO: handle this gracefully
    def _on_game_over_msg(self, msg):
        print("outcome: ", msg["outcome"])
        print(" game over! ")
        exit()

    def _on_send_game_id_msg(self, msg):
        print("  --send_game_id message received", msg)

        self.game_id = msg["game_id"]
        assert self.game_id is not None
        self.sio.emit("get_state", {"game_id": self.game_id})

    def _default_callback(self, msg_type, msg):
        raise Exception("Received unexpected data from server: " + msg_type + msg)

    def _on_error_msg(self, msg):
        raise Exception(msg)

    def run(self):
        """
        Server and client will repeatedly
        """
        print("  --running")
        self.sio.emit(
            "start_game",
            {
                "game": self.game,
                "game_type": self.game_type,
                "training": self.training,
                "model_name": self.model_name,
            },
        )
        self.sio.wait()
