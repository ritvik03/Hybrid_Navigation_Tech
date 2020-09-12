#!/bin/sh

for i in 1 
do

echo "[INFO] Running UnReal Environment.."
xterm -hold -e "cd ~/Airsim_Binaries/HiFi_3ftMarker/HiFi_3ftMarker/LinuxNoEditor/ && ./Blocks.sh" &
sleep 10

echo "[INFO] Running Airsim node.."
xterm -hold -e "cd catkin_vins && source devel/setup.bash && roslaunch airsim_ros_pkgs airsim_node.launch" &
sleep 5

echo "[INFO] Running VINS.."
xterm -hold -e "cd catkin_vins && source devel/setup.bash && roslaunch vins_estimator airsim.launch" &
sleep 5
xterm -hold -e "cd catkin_vins && source devel/setup.bash && roslaunch vins_estimator vins_rviz.launch" &
sleep 5

echo "[INFO] Running Navigation commands.."
xterm -hold -e "cd catkin_vins && source devel/setup.bash && cd src/AirSim/PythonClient/multirotor/ && python move_on_rangoli.py" &
xterm -hold -e "cd catkin_vins && source devel/setup.bash && cd src/AirSim/PythonClient/multirotor/ && python publish_path.py" &

done