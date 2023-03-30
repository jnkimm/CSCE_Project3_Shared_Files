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

        self.background_set = False

        self.background = LaserScan()  

        self.scans = []

        self.get_background = self.create_subscription(
            LaserScan,
            '/bg_scan',
            self.bg_callback,
            10)

        self.get_scans = self.create_subscription(LaserScan,'/scan',self.listener_callback,300)

        # self.ranges
    def bg_callback(self,data=LaserScan()): 
        self.background = data
        self.background_set = True
        self.get_logger().info("received background scan")

    def listener_callback(self,data=LaserScan()):
        # while(self.background_set == False):
        #     print("background not set")
        # self.get_logger().info("received background scan in listener_callback")
        self.scans.append(data)


def main(args=None):
    rclpy.init(args=args)
    node = Count()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()