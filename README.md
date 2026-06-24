# mp3_player — ROS2 MP3 Player Node

A ROS2 Python node that plays an `.mp3` file whenever a message is published to a topic. A new message interrupts any currently playing audio.

## Requirements

- ROS2 (Humble or later)
- `mpg123` audio player

```bash
sudo apt install mpg123
```

## Build

```bash
cd <your_ws>
colcon build --packages-select mp3_player
source install/setup.bash
```

## Usage

### Launch (recommended)

```bash
ros2 launch mp3_player mp3_player.launch.py
```

With a custom topic:

```bash
ros2 launch mp3_player mp3_player.launch.py topic:=/my_audio_topic
```

### Run the node directly

```bash
ros2 run mp3_player mp3_player_node
ros2 run mp3_player mp3_player_node --ros-args -p topic:=/my_audio_topic
```

### Publish a message to trigger playback

```bash
ros2 topic pub --once /play_audio std_msgs/String "data: '/relate/path/from/sounds/dir.mp3'"
ros2 topic pub --once /play_audio std_msgs/msg/String "data: 'ijou_hassei.mp3'"
```

## Behavior

| Situation | Result |
|---|---|
| Valid `.mp3` path received | Stops current audio (if any), plays new file |
| Path does not exist | Warning logged, playback skipped |
| File is not `.mp3` | Warning logged, playback skipped |
| Node shuts down | Current playback is stopped cleanly |

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `topic` | `/play_audio` | ROS2 topic to subscribe to |
