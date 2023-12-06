import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    rviz_config_dir = os.path.join(
        get_package_share_directory('ergocub_navigation'),
        'rviz',
        'nav2.rviz')

    return LaunchDescription([
        Node(package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            output={'both': 'log'},
            parameters=[{'use_sim_time': use_sim_time}]
            )
    ])