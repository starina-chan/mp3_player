# mp3_player

A ROS 2 node that plays a sound clip when you send it the clip's file name.

`mp3_player` is an `ament_python` package for ROS 2 Humble. The node listens on a `std_msgs/String` topic and plays each received `.mp3` with `mpg123` in a subprocess, so playback never blocks the ROS executor.

## Installation

Install `mpg123`, then build the package in your workspace:

```bash
sudo apt install mpg123
cd <your_ws>
colcon build --packages-select mp3_player
source install/setup.bash
```

## Features

- Plays an `.mp3` file when its path is published to a topic
- Resolves relative paths against the bundled `sounds/` directory
- Interrupts the current clip when a new one arrives
- Skips non-`.mp3` and missing files with a warning
- Stops playback cleanly on shutdown

## Usage

Start the node:

```bash
ros2 launch mp3_player mp3_player.launch.py
```

Play a bundled clip:

```bash
ros2 topic pub --once /play_audio std_msgs/msg/String "data: 'ijou_hassei.mp3'"
```

## Docs

### Launch arguments

| Argument | Default | Description |
| --- | --- | --- |
| `topic` | `/play_audio` | Topic to subscribe to for playback requests |

### Parameters

| Parameter | Default | Description |
| --- | --- | --- |
| `topic` | `/play_audio` | Topic to subscribe to for playback requests |

### Subscribed topics

| Topic | Type | Description |
| --- | --- | --- |
| `/play_audio` | `std_msgs/msg/String` | Absolute path, or path relative to `sounds/`, of the `.mp3` to play |

### Tests

```bash
colcon test --packages-select mp3_player
colcon test-result --verbose
```

Linting uses `ruff` instead of `ament_flake8`: `uvx ruff check . && uvx ruff format --check .`

### Bundled sounds

- `ijou.mp3`
- `ijou_hassei.mp3`
- `keikoku.mp3`
- `seijou.mp3`
