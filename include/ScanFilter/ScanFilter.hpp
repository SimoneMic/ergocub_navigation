#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "sensor_msgs/msg/imu.hpp"
#include "tf2_ros/transform_listener.h"
#include "tf2_ros/buffer.h"
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"
#include "tf2/transform_datatypes.h"
#include "tf2_sensor_msgs/tf2_sensor_msgs.hpp"
#include "laser_geometry/laser_geometry.hpp"

#include "rclcpp_lifecycle/lifecycle_node.hpp"
#include "rclcpp_lifecycle/lifecycle_publisher.hpp"

#include "pcl_conversions/pcl_conversions.h"
#include "pcl/point_types.h"
#include "pcl/filters/passthrough.h"
#include "pcl/ModelCoefficients.h"
#include "pcl/filters/project_inliers.h"

#include <mutex>

class ScanFilter : public rclcpp_lifecycle::LifecycleNode
{
private:
    //parameters
    std::string m_referece_frame = "geometric_unicycle";  //virtual_unicycle_base
    std::string m_scan_topic = "/scan_local";
    std::string m_pub_topic = "/compensated_pc2";
    std::string m_imu_topic = "/head_imu";
    laser_geometry::LaserProjection m_projector;

    float m_filter_z_low = 0.2;
    float m_filter_z_high = 2.5;
    double m_close_threshold = 0.5;
    double m_imuVel_x_threshold = 0.4;
    double m_imuVel_y_threshold = 0.4;
    double m_ms_wait = 400.0;
    std::chrono::system_clock::time_point m_last_vibration_detection;

    bool m_robot_on_crane = true;

    std::shared_ptr<tf2_ros::TransformListener> m_tf_listener_{nullptr};
    std::unique_ptr<tf2_ros::Buffer> m_tf_buffer_in;

    rclcpp_lifecycle::LifecyclePublisher<sensor_msgs::msg::PointCloud2>::SharedPtr m_pointcloud_pub;
    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr m_raw_scan_sub;
    rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr m_imu_sub;
    geometry_msgs::msg::Vector3 m_imu_angular_velocity;
    std::mutex m_imu_mutex;

    void scan_callback(const sensor_msgs::msg::LaserScan::ConstPtr& scan_in);

    void imuCallback(const sensor_msgs::msg::Imu::ConstPtr& imu_msg);

public:
    ScanFilter(const rclcpp::NodeOptions & options);

    using CallbackReturn = rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;

    CallbackReturn on_configure(const rclcpp_lifecycle::State &);
    CallbackReturn on_activate(const rclcpp_lifecycle::State &);
    CallbackReturn on_deactivate(const rclcpp_lifecycle::State &);
    CallbackReturn on_cleanup(const rclcpp_lifecycle::State &);
    CallbackReturn on_shutdown(const rclcpp_lifecycle::State & state);
    CallbackReturn on_error(const rclcpp_lifecycle::State & state);
};  // End of class ScanFilter node