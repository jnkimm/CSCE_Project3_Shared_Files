import rclpy
from rclpy.node import Node

# from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy, QoSLivelinessPolicy
# from rclpy.qos import QoSProfile

from sensor_msgs.msg import LaserScan
# from tf2_msgs.msg import TFMessage

# def print_if_scan():
#     print("pp")

class Count(Node):
    def __init__(self):
        super().__init__("Count_subscriber")

        self.laser_scan = LaserScan()  


        self.get_scans = self.create_subscription(
            LaserScan,
            '/bg_scan',
            self.listener_callback,
            10)

        self.send_data = self.create_publisher(LaserScan,'transfer',10)
        # self.ranges
    def listener_callback(self,data=LaserScan()): 
        self.laser_scan = data
        self.get_logger().info(f"received LaserScan message: {self.laser_scan.ranges}")

def main(args=None):
    rclpy.init(args=args)
    node = Count()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()