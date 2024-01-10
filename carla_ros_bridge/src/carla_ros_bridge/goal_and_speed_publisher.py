import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy
import csv
import os 
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float64

class GoalAndSpeedPublisher(Node):
    def __init__(self, csv_filepath):
        super().__init__('goal_and_speed_publisher')
        qos_profile = QoSProfile(
        reliability=QoSReliabilityPolicy.RELIABLE, 
        history=QoSHistoryPolicy.KEEP_LAST, 
        depth=10, 
        durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
        self.goal_pub = self.create_publisher(PoseStamped, '/carla/hero/goal_pose', qos_profile)
        self.speed_pub = self.create_publisher(Float64, '/carla/hero/target_speed', qos_profile)
        self.publish_goal_and_speed(csv_filepath)

    def publish_goal_and_speed(self, csv_filepath):
        # Read the CSV file
        with open(csv_filepath, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            next(csv_reader)  # Skip the header row

            # Read the first row only
            row = next(csv_reader)
            x, y, z, speed = map(float, row)

            # Create the PoseStamped message for the goal position
            goal_msg = PoseStamped()
            goal_msg.header.stamp = self.get_clock().now().to_msg()
            goal_msg.header.frame_id = "map"
            goal_msg.pose.position.x = x
            goal_msg.pose.position.y = y
            goal_msg.pose.position.z = z
            goal_msg.pose.orientation.w = 1.0  # Assuming no orientation

            # Create the Float64 message for the target speed
            speed_msg = Float64()
            speed_msg.data = speed

            # Publish the messages
            self.goal_pub.publish(goal_msg)
            self.speed_pub.publish(speed_msg)

def main(args=None):
    rclpy.init(args=args)
    iotav_root = os.getenv('IOTAV_ROOT')
    csv_file_path = os.path.join(iotav_root, 'carla_ros_bridge/src/carla_ros_bridge/src/carla_ros_bridge/data.csv')  
    goal_and_speed_publisher = GoalAndSpeedPublisher(csv_file_path)
    rclpy.spin(goal_and_speed_publisher)

    goal_and_speed_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

