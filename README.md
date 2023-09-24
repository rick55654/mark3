cd mark3_ws

colcon build --symlink-install

source install/setup.bash

ros2 launch mark3 launch_sim.launch.py world:=src/mark3/worlds/rick.world

# launch without map
ros2 launch mark3 launch_sim.launch.py

#SLAM
ros2 launch mark3 online_async_launch.py

#nav2
ros2 launch mark3 navigation_launch.py
