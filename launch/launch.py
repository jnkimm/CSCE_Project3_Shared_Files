from launch import LaunchDescription
from launch.actions import *
from launch.event_handlers import *
from launch.events import *
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    get_scans_node = Node(package = "project3", executable = "get_scans")
    count_people_node = Node(package = "project3", executable = "count_people")

    rviz = ExecuteProcess(cmd = ['rviz'])
    ld.add_action(rviz)

    # starting nodes
    ld.add_action(get_scans_node)
    ld.add_action(count_people_node)

    # playing bag
    ep = ExecuteProcess(cmd = ['ros2', 'bag', 'play', 'bags/example1'])
    ld.add_action(ep)

    # exiting process
    event_handler = OnProcessExit(target_action = ep, on_exit = [EmitEvent(event = Shutdown())])
    terminate_at_end = RegisterEventHandler(event_handler)

    ld.add_action(terminate_at_end)

    return ld
