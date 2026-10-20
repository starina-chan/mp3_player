"""ROS2 node that plays an MP3 file when a message is received on /play_audio."""

import os
import subprocess
import threading

import rclpy
from ament_index_python.packages import get_package_share_directory
from rclpy.node import Node
from std_msgs.msg import String


class Mp3PlayerNode(Node):
    def __init__(self):
        super().__init__("mp3_player_node")

        self.declare_parameter("topic", "/play_audio")
        topic = self.get_parameter("topic").get_parameter_value().string_value

        self._process: subprocess.Popen | None = None
        self._lock = threading.Lock()

        self.create_subscription(String, topic, self._on_play, 10)
        self.get_logger().info(f"Listening on topic: {topic}")

        self._sounds_dir = os.path.join(
            get_package_share_directory("mp3_player"), "sounds"
        )

    def _on_play(self, msg: String) -> None:
        path = msg.data.strip()

        if not path.lower().endswith(".mp3"):
            self.get_logger().warn(f"File is not an .mp3: {path}")
            return

        if not os.path.isabs(path):
            path = os.path.join(self._sounds_dir, path)

        if not os.path.isfile(path):
            self.get_logger().warn(f"File not found: {path}")
            return

        with self._lock:
            self._stop_current()
            self.get_logger().info(f"Playing: {path}")
            self._process = subprocess.Popen(
                ["mpg123", "-q", path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    def _stop_current(self) -> None:
        if self._process is not None and self._process.poll() is None:
            self._process.terminate()
            try:
                self._process.wait(timeout=2.0)
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
