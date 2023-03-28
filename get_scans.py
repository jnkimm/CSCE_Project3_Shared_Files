import rclpy
from rclpy.node import Node

# from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy, QoSLivelinessPolicy
# from rclpy.qos import QoSProfile

from sensor_msgs.msg import LaserScan
# from tf2_msgs.msg import TFMessage

# def print_if_scan():
#     print("pp")

class Listener(Node):
    def __init__(self):
        super().__init__("Laser_scan_subscriber")

        # self.current_scan = LaserScan()
        self.background_set = False
        self.background_scan = LaserScan()
        self.last_five = []
        self.get_scans = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            10)

        # self.send_data = self.create_publisher(LaserScan,'transfer_scans',10)
        self.send_bg = self.create_publisher(LaserScan,'bg_scan',10)
        # self.ranges
    def listener_callback(self,data=LaserScan()): 
        # self.get_logger().info(f"received LaserScan message: {self.laser_scan.ranges}")
        # self.send_data.publish(data)
        if (not(self.background_set)):
            self.last_five.append(data)
        # if(len(self.background_scan.ranges) == 0):
        #     self.background_scan = data
        # else:
        #     for i in range(len(self.background_scan.ranges)):
        #         if (data.ranges[i] == float('inf')):
        #             if (background_scan.ranges[i] == float('inf')):
        #                 continue;
        #             elif (abs(background_scan.ranges[i] - data.range_max) ):
        print(self.background_set)
        if (len(self.last_five) == 5 and not(self.background_set)) :
            self.is_background()
            self.last_five.pop(0)
        else:
            self.send_bg.publish(self.background_scan)


    def is_background(self):
            for i in range(len(self.last_five[0].ranges)):
                average = (self.last_five[0].ranges[i] + self.last_five[1].ranges[i] + self.last_five[2].ranges[i] + self.last_five[3].ranges[i] + self.last_five[4].ranges[i])/5
                if (average == float('nan')):
                    average = float('inf')
                for j in range(5):
                    if ((average == float('inf')) and (self.last_five[j].ranges[i] == float('inf'))):
                        continue
                    elif ((average == float('inf')) and (abs(self.last_five[j].ranges[i] - self.last_five[j].range_max) > 0.1)) :
                        continue
                    elif (abs(average - self.last_five[j].ranges[i]) > 0.1):
                        return
            self.background_scan = self.last_five[2]
            self.get_logger().info(f"received LaserScan message: {self.background_scan.ranges}")
            self.send_bg.publish(self.last_five[2])
            self.background_set = True


def main(args=None):
    rclpy.init(args=args)
    node = Listener()
    print("about to spin")
    rclpy.spin(node)
    print("done spinning")
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()