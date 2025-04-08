# vikings_bot_localization_server

<hr>

### Description
This package contains `vikings_bot` project localization related files. It uses AMCL localization method from `ROS2 NAV2` stack.

<hr>

## Installation

Download source and install dependencies:
```
rosdep update
rosdep install --ignore-src --default-yes --from-path src
```

Build package:
```
colcon build
source install/setup.bash
```

<hr>

### Usage

To spawn localization:
```
ros2 launch vikings_bot_localization_server spawn_localization.launch.py
```
#### Parameters:
- `vikings_bot_name`: namespace of robot - [vikings_bot_1 or vikings_bot_2] -> *string*, default *vikings_bot_1*
- `x_spawn`: Initial x pose -> *float*, default *0.0*
- `y_spawn`: Initial y pose -> *float*, default *0.0*
- `yaw_spawn`: Initial yaw pose -> *float*, default *0.0*
- `use_sim`: whether to use simulated or real robot -> *bool*, default *true*



