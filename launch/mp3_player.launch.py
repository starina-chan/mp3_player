from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")
    namespace = LaunchConfiguration("namespace")
    topic = LaunchConfiguration("topic")

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation clock",
    )
    namespace_arg = DeclareLaunchArgument(
        "namespace",
        default_value="",
        description="Namespace for the node and its topic",
    )
    topic_arg = DeclareLaunchArgument(
        "topic",
        default_value="play_audio",
        description="Topic to subscribe to for MP3 playback requests",
    )

    mp3_player_node = Node(
        package="mp3_player",
        executable="mp3_player_node",
        name="mp3_player_node",
        namespace=namespace,
        parameters=[{"use_sim_time": use_sim_time}],
        remappings=[("play_audio", topic)],
        output="screen",
    )

    return LaunchDescription(
        [
            use_sim_time_arg,
            namespace_arg,
            topic_arg,
            mp3_player_node,
        ]
    )
