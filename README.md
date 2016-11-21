# trajpub

A collection of ROS nodes that publish messages of the type `geometry_msgs/Point`.

## Installation

Type this in a terminal.
This should work if you have ROS and `catkin_tools` installed on your computer.

```
cd <your_catkin_workspace>/src
git clone https://github.com/adaldo/trajpub
cd <your_catkin_workspace>
catkin build
source devel/setup.bash
```

## Usage

Type this in a terminal.

```
roslaunch trajpub example.launch type:=<some_type>
```

Replace `<some_type>` with the trajectory that you want to publish, such as `circle` or `constant`.

## Adding your own trajectories using `rospy`

1. Inherit from `abstract.Abstract`.
2. Redefine `compute_point` and, if needed, `__init__`.
3. Start a ROS node with `rospy.init_node`.
4. Spawn an instance of your child class.
5. Call the `start` method on your object.

You can use `zero.py` as a stub.
