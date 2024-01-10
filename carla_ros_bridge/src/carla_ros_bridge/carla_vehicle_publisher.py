import rclpy
from rclpy.node import Node
import carla
from carla_msgs.msg import CarlaActorList, CarlaActorInfo

class CarlaVehiclePublisher(Node):
    def __init__(self):
        super().__init__('carla_vehicle_publisher')
        self.publisher = self.create_publisher(CarlaActorList, '/carla/vehicles', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(10.0)

    def timer_callback(self):
        world = self.client.get_world()
        vehicles = world.get_actors().filter('vehicle.*')

        actor_list_msg = CarlaActorList()
        for vehicle in vehicles:
            actor_info = CarlaActorInfo()
            actor_info.id = vehicle.id
            actor_info.type = vehicle.type_id
            actor_info.rolename = vehicle.attributes.get('role_name', 'unknown')
            actor_list_msg.actors.append(actor_info)

        self.publisher.publish(actor_list_msg)

def main(args=None):
    rclpy.init(args=args)
    node = CarlaVehiclePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

