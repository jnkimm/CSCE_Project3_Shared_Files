import rclpy
from rclpy.node import Node

from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy, QoSLivelinessPolicy
from rclpy.qos import QoSProfile

from sensor_msgs.msg import LaserScan
from tf2_msgs.msg import TFMessage

def print_if_scan():
    print("pp")

class Listener(Node):
    def __init(self):
        super().__init__("Laser_scan_subscriber")

        self.laser_scan = LaserScan()

        qos_profile = QoSProfile(depth=100)
        qos_profile.reliability = QoSReliabilityPolicy.RELIABLE
        qos_profile.durability = QoSDurabilityPolicy.VOLATILE
        qos_profile.history = QoSHistoryPolicy.UKNOWN
        qos_profile.deadline = -1
        qos_profile.lifespan = -1
        qos_profile.Liveliness = QoSLivelinessPolicy.AUTOMATIC
        qos_profile.Liveliness_lease_duration = -1
        qos_profile.avoid_rosbag_mismatch = True

        self.get_scans = self.create_subscription(
            LaserScan,
            '/rosbag2_player/scan',
            self.listener_callback,
            qos_profile)
        # self.ranges
    def listener_callback(self,data=LaserScan()): 
        self.laser_scan = data
        print("pp")
        self.get_logger().info(f"received LaserScan message: {self.laser_scan.ranges}")
        print_if_scan()

def main(args=None):
    rclpy.init(args=args)
    node = Listener("pp")
    print("about to spin")
    rclpy.spin(node)
    print("done spinning")
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()