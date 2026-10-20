import os
import subprocess
import threading

import rclpy
from ament_index_python.packages import get_package_share_directory
from rclpy.node import Node
from std_msgs.msg import String

PACKAGE_NAME = "mp3_player"
SOUNDS_DIRECTORY = "sounds"
MP3_EXTENSION = ".mp3"
PLAYER_COMMAND = ["mpg123", "-q"]
STOP_TIMEOUT_SECONDS = 2.0
QUEUE_DEPTH = 10


class Mp3PlayerNode(Node):
    def __init__(self):
        super().__init__("mp3_player_node")

        self.declare_parameter("topic", "/play_audio")
        topic = self.get_parameter("topic").get_parameter_value().string_value

        self._process: subprocess.Popen | None = None
        self._lock = threading.Lock()

        self.create_subscription(String, topic, self._on_play, QUEUE_DEPTH)
        self.get_logger().info(f"Listening on topic: {topic}")

        self._sounds_directory = os.path.join(
            get_package_share_directory(PACKAGE_NAME), SOUNDS_DIRECTORY
        )

    def _on_play(self, msg: String) -> None:
        path = msg.data.strip()

        if not path.lower().endswith(MP3_EXTENSION):
            self.get_logger().warn(f"File is not an .mp3: {path}")
            return

        resolved_path = self._resolve_path(path)
        if not os.path.isfile(resolved_path):
            self.get_logger().warn(f"File not found: {resolved_path}")
            return

        self._play(resolved_path)

    def _resolve_path(self, path: str) -> str:
        if os.path.isabs(path):
            return path
        return os.path.join(self._sounds_directory, path)

    def _play(self, path: str) -> None:
        with self._lock:
            self._stop_current()
            self.get_logger().info(f"Playing: {path}")
            self._process = subprocess.Popen(
                [*PLAYER_COMMAND, path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    def _stop_current(self) -> None:
        is_playing = self._process is not None and self._process.poll() is None
        if not is_playing:
            self._process = None
            return

        self._process.terminate()
        try:
            self._process.wait(timeout=STOP_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            self._process.kill()
        self._process = None

    def destroy_node(self) -> None:
        with self._lock:
            self._stop_current()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = Mp3PlayerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
