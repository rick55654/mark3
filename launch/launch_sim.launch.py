import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from launch.actions import TimerAction



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='mark3' #<--- CHANGE ME

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )


    gazebo_params_path = os.path.join(
                get_package_share_directory(package_name),'config','gazebo_params.yaml')
    

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                     launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_path }.items()
             )
    # Rviz2 
    rviz = get_package_share_directory(package_name)

    rviz2 = Node(
    name="rviz2",
    package="rviz2",
    executable="rviz2",
    arguments=['-d', os.path.join(rviz, 'config', 'view_bot.rviz')],
    )


    joy_params = os.path.join(get_package_share_directory(package_name),'config','joystick.yaml')

    joy_node = Node(
    package='joy',
    executable='joy_node',
    parameters=[joy_params,{'use_sim_time': True}],
    )


    teleop_node = Node(
    package='teleop_twist_joy', 
    executable='teleop_node',        
    name='teleop_node',        
    parameters=[joy_params, {'use_sim_time': True}],       
    remappings=[('/cmd_vel','/cmd_vel_joy')],
    )
                

    twist_mux_params = os.path.join(get_package_share_directory(package_name),'config','twist_mux.yaml')

    twist_mux = Node(
    package="twist_mux",
    executable="twist_mux",
    parameters=[twist_mux_params, {'use_sim_time': True}],
    remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')],
    )

    diff_drive_spawner = Node(
    package="controller_manager",
    executable="spawner.py",
    arguments=["diff_cont"],
    )
    
    joint_broad_spawner = Node(
    package="controller_manager",
    executable="spawner.py",
    arguments=["joint_broad"],
    )

    joint_trajectory_controller_spawner = Node(
    package="controller_manager",
    executable="spawner.py",
    arguments=["joint_trajectory_controller"],
    )




    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'mark3'],
                        output='screen')



    # Launch them all!
    return LaunchDescription([
        rsp,
        twist_mux,
        joy_node,
        teleop_node,
        gazebo,
        spawn_entity,
        joint_broad_spawner,
        diff_drive_spawner,
        joint_trajectory_controller_spawner,
        TimerAction(period=6.0,
            actions=[rviz2])
    ])
