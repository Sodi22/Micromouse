import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion

import time

class FollowLeftWall(Node):
    def __init__(self):
        super().__init__("follow_left_wall")
        
        # Publisher for robot velocity commands
        self.cmd_vel_publisher = self.create_publisher(Twist, "/cmd_vel", 10)

        # Subscriber for laser scan data
        self.laser_scan_subscriber = self.create_subscription(LaserScan, "/scan", self.laser_scan_callback, 1)

        # Subscriber to the /odom topic
        self.odom_subscriber = self.create_subscription(Odometry, "/odometry/filtered", self.odom_callback, 1)

        self.target_distance_to_wall = 0.7 # in meters
        self.forward_speed = 0.1 # in m/s
        self.turning_speed = 0.05 # in rad/s

        self.current_position_x = 0.0
        self.current_position_y = 0.0
        self.current_yaw = 0.0
        self.direction = 0 # north: 0, west: 1, south: 2, east: 3

        self.positional_error = 0.01
        self.angular_error = 0.0175 #0.0017

        self.left_distance = 0.5
        self.front_distance = 5
        self.right_distance = 0.5

        self.target_position_x = 0.9
        self.target_position_y = 0.0
        self.target_yaw = 0.0

        self.lidar = 0
        self.odom = 0

        self.get_logger().info("FollowLeftWall node has been started.")

    def laser_scan_callback(self, msg: LaserScan):
        ranges = msg.ranges
        num_ranges = len(ranges)

        left_index = int((1.5708 - msg.angle_min) / msg.angle_increment)
        front_index = int((0.0 - msg.angle_min) / msg.angle_increment)
        right_index = int((-1.5708 - msg.angle_min) / msg.angle_increment)

        left_index = max(0, min(left_index, num_ranges-1))
        front_index = max(0, min(front_index, num_ranges-1))
        right_index = max(0, min(right_index, num_ranges-1))

        left_distance = ranges[left_index]
        front_distance = ranges[front_index]
        right_distance = ranges[right_index]

        self.left_distance = left_distance
        self.front_distance = front_distance
        self.right_distance = right_distance

        self.lidar = 1

        #self.get_logger().info(f"Distance: left={left_distance}, front={front_distance}, right={right_distance}")

    def odom_callback(self, msg: Odometry):
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation

        quaternion = (orientation.x, orientation.y, orientation.z, orientation.w)
        roll, pitch, yaw = euler_from_quaternion(quaternion)

        self.current_position_x = position.x
        self.current_position_y = position.y
        self.current_yaw = yaw

        self.odom = 1

        #self.get_logger().info(f"Position: x={position.x}, y={position.y}")
        #self.get_logger().info(f"Orientation: yaw={yaw}")

    def turn(self):
        twist = Twist()

        if self.left_distance > self.target_distance_to_wall:
            if self.direction == 0:
                self.target_yaw = 1.5708
                self.direction = 1
            elif self.direction == 1:
                self.target_yaw = 3.1416
                self.direction = 2
            elif self.direction == 2:
                self.target_yaw = -1.5708
                self.direction = 3
            elif self.direction == 3:
                self.target_yaw = 0.0
                self.direction = 0
            twist.angular.z = self.turning_speed
            twist.linear.x = 0.0
            self.cmd_vel_publisher.publish(twist)
        elif self.front_distance > self.target_distance_to_wall:
            if self.direction == 0:
                self.target_yaw = 0.0
            elif self.direction == 1:
                self.target_yaw = 1.5708
            elif self.direction == 2:
                self.target_yaw = 3.1416
            elif self.direction == 3:
                self.target_yaw = -1.5708
            twist.angular.z = 0.0
            twist.linear.x = 0.0
            self.cmd_vel_publisher.publish(twist)
        elif self.right_distance > self.target_distance_to_wall:
            if self.direction == 0:
                self.target_yaw = -1.5708
                self.direction = 3
            elif self.direction == 1:
                self.target_yaw = 0.0
                self.direction = 0
            elif self.direction == 2:
                self.target_yaw = 1.5708
                self.direction = 1
            elif self.direction == 3:
                self.target_yaw = 3.1416
                self.direction = 2
            twist.angular.z = -self.turning_speed
            twist.linear.x = 0.0
            self.cmd_vel_publisher.publish(twist)
        else:
            if self.direction == 0:
                self.target_yaw = 3.1416
                self.direction = 2
            elif self.direction == 1:
                self.target_yaw = -1.5708
                self.direction = 3
            elif self.direction == 2:
                self.target_yaw = 0.0
                self.direction = 0
            elif self.direction == 3:
                self.target_yaw = 1.5708
                self.direction = 1
            twist.angular.z = self.turning_speed
            twist.linear.x = 0.0
            self.cmd_vel_publisher.publish(twist)

    def move(self):
        twist = Twist()
        if self.direction == 0:
            self.target_position_x = self.current_position_x
            self.target_position_y = self.current_position_y
            self.target_position_x += 0.9
            self.target_position_x = round(self.target_position_x / 0.9) * 0.9
            self.get_logger().info(f"Target x={self.target_position_x}")
        elif self.direction == 1:
            self.target_position_x = self.current_position_x
            self.target_position_y = self.current_position_y
            self.target_position_y += 0.9
            self.target_position_y = round(self.target_position_y / 0.9) * 0.9
            self.get_logger().info(f"Target y={self.target_position_y}")
        elif self.direction == 2:
            self.target_position_x = self.current_position_x
            self.target_position_y = self.current_position_y
            self.target_position_x -= 0.9
            self.target_position_x = round(self.target_position_x / 0.9) * 0.9
            self.get_logger().info(f"Target x={self.target_position_x}")
        elif self.direction == 3:
            self.target_position_x = self.current_position_x
            self.target_position_y = self.current_position_y
            self.target_position_y -= 0.9
            self.target_position_y = round(self.target_position_y / 0.9) * 0.9
            self.get_logger().info(f"Target y={self.target_position_y}")
        twist.angular.z = 0.0
        twist.linear.x = self.forward_speed
        self.cmd_vel_publisher.publish(twist)

    def stop(self):
        twist = Twist()
        twist.angular.z = 0.0
        twist.linear.x = 0.0
        self.cmd_vel_publisher.publish(twist)

    def reset(self):
        self.lidar = 0
        self.odom = 0

def main(args=None):
    rclpy.init(args=args)
    follow_left_wall = FollowLeftWall()
    while 1:
        while follow_left_wall.lidar == 0 or follow_left_wall.odom == 0:
            rclpy.spin_once(follow_left_wall)
        follow_left_wall.reset()
        follow_left_wall.turn()
        while follow_left_wall.current_yaw < follow_left_wall.target_yaw - follow_left_wall.angular_error or follow_left_wall.current_yaw > follow_left_wall.target_yaw + follow_left_wall.angular_error:
            rclpy.spin_once(follow_left_wall)
        follow_left_wall.stop()
        while follow_left_wall.lidar == 0 or follow_left_wall.odom == 0:
            rclpy.spin_once(follow_left_wall)
        follow_left_wall.reset()
        follow_left_wall.move()
        if follow_left_wall.direction == 0 or follow_left_wall.direction == 2:
            while abs(follow_left_wall.current_position_x - follow_left_wall.target_position_x) > follow_left_wall.positional_error:
                rclpy.spin_once(follow_left_wall)
        else:
            while abs(follow_left_wall.current_position_y - follow_left_wall.target_position_y) > follow_left_wall.positional_error:
                rclpy.spin_once(follow_left_wall)
        follow_left_wall.stop()
        follow_left_wall.get_logger().info("WAITING")
        time.sleep(1)
    follow_left_wall.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()