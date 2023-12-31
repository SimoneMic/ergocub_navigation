from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    return LaunchDescription([
        #DeclareLaunchArgument(
        #    'use_sim_time',
        #    default_value='false',
        #    description='Use simulation (Gazebo) clock if true'
        #),
        DeclareLaunchArgument(
            name='scanner', 
            default_value='scanner',
            description='Namespace for sample topics'
        ),
        Node(
            package='ergocub_navigation',
            executable='scan_filter',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}]
        ),
        Node(
            package='pointcloud_to_laserscan', executable='pointcloud_to_laserscan_node',
            remappings=[('cloud_in', '/compensated_pc2'),
                        ('scan', '/filtered_scan_compensated')],
            parameters=[{
                'target_frame': 'geometric_unicycle',    #virtual_unicycle_base
                'transform_tolerance': 0.03,        #0.01
                'min_height': -0.2,  #-300
                'max_height': 3.0,  #300
                'angle_min': -2.7,   #-2.61799,  # -M_PI
                'angle_max': 2.7,    #2.61799,  # M_PI
                'angle_increment': 0.003926991,  # 2M_PI/360.0
                'scan_time': 0.05,
                'range_min': 0.2,
                'range_max': 30.0,
                'use_inf': True,
                'inf_epsilon': 1.0
                #'concurrency_level': 2
            }],
            name='pointcloud_to_laserscan'
        ),
        Node(
            package='pointcloud_to_laserscan', executable='pointcloud_to_laserscan_node',
            remappings=[('cloud_in', '/compensated_pc2_2'),
                        ('scan', '/rear_scan_compensated_right')],
            parameters=[{
                'target_frame': 'geometric_unicycle',    #virtual_unicycle_base
                'transform_tolerance': 0.03,        #0.01
                'min_height': -0.2,  #-300
                'max_height': 3.0,  #300
                'angle_min': -2.61799,   #-3.141592653,  # -M_PI
                'angle_max': -1.0,    #3.141592653,  # M_PI
                'angle_increment': 0.003926991,  # 2M_PI/360.0
                'scan_time': 0.05,
                'range_min': 0.2,
                'range_max': 30.0,
                'use_inf': True,
                'inf_epsilon': 1.0
                #'concurrency_level': 2
            }],
            name='rear_pointcloud_to_laserscan_right'
        ),
        Node(
            package='pointcloud_to_laserscan', executable='pointcloud_to_laserscan_node',
            remappings=[('cloud_in', '/compensated_pc2_3'),
                        ('scan', '/rear_scan_compensated_left')],
            parameters=[{
                'target_frame': 'geometric_unicycle',    #virtual_unicycle_base
                'transform_tolerance': 0.03,        #0.01
                'min_height': -0.2,  #-300
                'max_height': 3.0,  #300
                'angle_min': 1.0,   #-3.141592653,  # -M_PI
                'angle_max': 2.61799,    #3.141592653,  # M_PI
                'angle_increment': 0.003926991,  # 2M_PI/360.0
                'scan_time': 0.05,
                'range_min': 0.2,
                'range_max': 30.0,
                'use_inf': True,
                'inf_epsilon': 1.0
                #'concurrency_level': 2
            }],
            name='rear_pointcloud_to_laserscan_left'
        )
    ])
    