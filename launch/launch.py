from launch import *
from launch.actions import *
from launch.event_handlers import *
from launch.events import *
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    arg = DeclareLaunchArgument('bag_in')
    arg = DeclareLaunchArgument('bag_out')

    ld = LaunchDescription([arg])

    get_scans_node = Node(package = "project_3", executable = "get_scans")
    count_people_node = Node(package = "project_3", executable = "count_people")

    # rviz = ExecuteProcess(cmd = ['rviz2'])
    # ld.add_action(rviz)

    # starting nodes
    ld.add_action(get_scans_node)
    ld.add_action(count_people_node)

    # playing bag
    bag = LaunchConfiguration('bag_in')
    ep = ExecuteProcess(cmd = ['ros2', 'bag', 'play', bag])
    ld.add_action(ep)

    bag_o = LaunchConfiguration('bag_out')
    bag_exec = ExecuteProcess(cmd = ['ros2', 'bag', 'record', '/person_locations', '/people_count_current', 'people_count_total', '/test', bag_o])
    ld.add_action(bag_exec)

    # exiting process
    event_handler = OnProcessExit(target_action = bag_exec, on_exit = [EmitEvent(event = Shutdown())])
    terminate_at_end = RegisterEventHandler(event_handler)

    ld.add_action(terminate_at_end)

    return ld
