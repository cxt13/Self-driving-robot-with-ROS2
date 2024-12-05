import os
from pathlib import Path

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription  # Corrected import

from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration  # Corrected import

def generate_launch_description():
    bumperbot_description_dir = get_package_share_directory("bumperbot_description")

    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(bumperbot_description_dir, "urdf", "bumperbot.urdf.xacro"),  # Simplified path handling
        description="Absolute path to robot URDF file"
    )

    robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration("model")]),
        value_type=str
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )

    gazebo_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=[str(Path(bumperbot_description_dir).parent.resolve())]  # Fixed path handling
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")  # Corrected path and arguments
        ]),
        launch_arguments=[
            ("gz_args", [" --render-engine ogre -v 4 -r empty.sdf "])  # Fixed argument formatting
        ]
    )

    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-topic", "robot_description", "-name", "bumperbot"]
    )

    return LaunchDescription([
        model_arg,
        robot_state_publisher_node,
        gazebo_resource_path,
        gazebo,
        gz_spawn_entity
    ])
