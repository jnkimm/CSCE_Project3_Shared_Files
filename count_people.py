import rclpy
import math
from rclpy.node import Node

# from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy, QoSLivelinessPolicy
# from rclpy.qos import QoSProfile

from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32
from std_msgs.msg import Header
from example_interfaces.msg import Int64
# from tf2_msgs.msg import TFMessage

# def print_if_scan():
#     print("pp")

class Count(Node):
    def __init__(self):
        super().__init__("Count_subscriber")

        self.background_set = False

        self.point_array = PointCloud()

        self.background = LaserScan()

        self.scans = []

        self.get_background = self.create_subscription(
            LaserScan,
            '/bg_scan',
            self.bg_callback,
            10)

        self.get_scans = self.create_subscription(LaserScan,'/scan',self.listener_callback,300)

        self.finish = self.create_subscription(LaserScan,'bag_finish',self.algo,10)

        self.point_cloud_pub = self.create_publisher(PointCloud, 'person_locations', 10)

        self.people_count_pub = self.create_publisher(Int64, '/people_count_current', 10)

        # self.ranges
    def bg_callback(self,data=LaserScan()): 
        if (self.background_set == False):
            if (len(data.ranges) == 512):
                self.background = data
                self.background_set = True
                self.get_logger().info("received background scan")
                print(len(self.background.ranges))

    def listener_callback(self,data=LaserScan()):
        if (self.background_set == True):
            person = False
            good = 0
            bad = 0
            point_array = PointCloud()
            header = Header()
            header.frame_id = "laser"
            point_array.header = header
            for i in range(512):
                if data.ranges[i] < (self.background.ranges[i] - 0.1):
                    if not person:
                        good += 1
                        if good == 6:
                            person = True
                            angle1 = data.angle_min + i * data.angle_increment
                            range1 = data.ranges[i]
                            bad = 0
                    else:
                        bad = 0
                else:
                    if person:
                        bad += 1
                        if bad == 6: # should be same number as n in (i - n) stuff but FOR SURE should not be more
                            person = False
                            angle2 = data.angle_min + (i - 7) * data.angle_increment
                            range2 = data.ranges[i - 7]
                            angle = (angle1 + angle2) / 2
                            range_ = (range1 + range2) / 2
                            x = range_ * math.cos(angle)
                            y = (range_ * math.sin(angle))
                            #self.get_logger().info("(" + str(x) + ", " + str(y) + ")")
                            point = Point32()
                            point.x = x
                            point.y = y
                            # self.get_logger().info("(" + str(point.x) + ", " + str(point.y) + ")")
                            point_array.points.append(point)
                            good = 0
                    else:
                        good = 0
            people_count = len(point_array.points)
            message = Int64()
            message.data = people_count
            self.people_count_pub.publish(message)
            self.point_cloud_pub.publish(point_array)
            # self.get_logger().info("--------------------------")
                           

    def algo(self):
        print("in algorithm")


def main(args=None):
    rclpy.init(args=args)
    node = Count()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()