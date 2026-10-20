from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    topic_arg = DeclareLaunchArgument(
        "topic",
        default_value="/play_audio",
        description="ROS2 topic to subscribe to for MP3 playback requests",
    )

    mp3_player_node = Node(
        package="mp3_player",
        executable="mp3_player_node",
        name="mp3_player_node",
        parameters=[{"topic": LaunchConfiguration("topic")}],
        output="screen",
    )

    return LaunchDescription(
        [
            topic_arg,
            mp3_player_node,
        ]
    )
