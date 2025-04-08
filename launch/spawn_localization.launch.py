#!/usr/bin/python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import TextSubstitution, LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.actions import LogInfo, DeclareLaunchArgument, OpaqueFunction


def launch_setup(context, *arg, **args):

    ### DATA INPUT ###
    vikings_bot_name = LaunchConfiguration("vikings_bot_name").perform(context)
    x_spawn = LaunchConfiguration('x_spawn').perform(context)
    y_spawn = LaunchConfiguration('y_spawn').perform(context)
    yaw_spawn = LaunchConfiguration('yaw_spawn').perform(context)
    use_sim = LaunchConfiguration("use_sim")


    package_name = "vikings_bot_localization_server"

    #amcl_config = os.path.join(get_package_share_directory(package_name), "config", "vikings_bot_amcl_config.yaml")
    amcl_config=PathJoinSubstitution([
        FindPackageShare(package_name),
        'config',
        'vikings_bot_amcl_config.yaml'
    ])
    #c = PathJoinSubstitution([get_package_share_directory(package_name), "config", vikings_bot_name_val, "_amcl_config.yaml"])

    print(x_spawn)
    

    # AMCL node
    nav2_amcl = Node(
        namespace=vikings_bot_name,
        package="nav2_amcl",
        executable="amcl",
        name="amcl",
        output="screen",
        parameters=[amcl_config,
                    {"initial_pose": {"x": float(x_spawn)}},
                    {"initial_pose": {"y": float(y_spawn)}},
                    {"initial_pose": {"yaw": float(yaw_spawn)}},
                    {"base_frame_id": f"{vikings_bot_name}/base_footprint_link"},  # These are set from launch file
                    {"odom_frame_id": f"{vikings_bot_name}/odom"}, # Because namespace is only applied to *topic* (not frame) parameters in yaml file  
                    {'use_sim_time': use_sim}
        ]
    )

    # Lifecycle node
    lifecycle_node = Node(namespace=vikings_bot_name,
                            package='nav2_lifecycle_manager',
                            executable='lifecycle_manager',
                            name="amcl_lifecycle_manager",
                            output='screen',
                            parameters=[{'use_sim_time': use_sim},
                                        {'autostart': True},
                                        {"bond_timeout": 5.0},
                                        {'node_names': ["amcl"]}
                            ]
    )

    return [nav2_amcl, lifecycle_node]


def generate_launch_description():
    # Declare launch arguments
    vikings_bot_name_arg = DeclareLaunchArgument("vikings_bot_name",
                    default_value="vikings_bot",
                    description="Robot name to make it unique")
    x_spawn_arg = DeclareLaunchArgument('x_spawn', default_value='0.0')
    y_spawn_arg = DeclareLaunchArgument('y_spawn', default_value='0.0')
    yaw_spawn_arg = DeclareLaunchArgument('yaw_spawn', default_value='0.0')
    use_sim_arg = DeclareLaunchArgument("use_sim",
                                            default_value="True",
                                            description='Use simulation or real time')

    return LaunchDescription([
        vikings_bot_name_arg,
        x_spawn_arg,
        y_spawn_arg,
        yaw_spawn_arg,
        use_sim_arg,

        OpaqueFunction(function=launch_setup)
    ])
