#!/bin/sh

for i in 1 
do

xterm -hold -e "roscore" &
xterm -hold -e "cd ~/Airsim_Binaries/HiFi_3ftMarker/HiFi_3ftMarker/LinuxNoEditor/ && ./Blocks.sh" &
sleep 10
# xterm -hold -e "cd ~/vins_ws/catkin_airsim/src/AirSim/PythonClient/multirotor/ && python goto_location.py" &
xterm -hold -e "cd ~/vins_ws/catkin_airsim && source devel/setup.bash && source install/setup.bash && cd ~/vins_ws/catkin_airsim/src/AirSim/PythonClient/multirotor/ && python publish_image.py" &
# xterm -hold -e "cd ~/catkin_workspace && source devel/setup.bash && source install/setup.bash && cd ~/catkin_workspace/src/AirSim/PythonClient/multirotor/ && python publish_image.py" &
xterm -hold -e "cd ~/vins_ws/catkin_airsim && source devel/setup.bash && source install/setup.bash && cd ~/vins_ws/catkin_airsim/src/AirSim/PythonClient/multirotor/ && python publish_imu.py" &
xterm -hold -e "cd ~/vins_ws/catkin_airsim && source devel/setup.bash && source install/setup.bash && cd ~/vins_ws/catkin_airsim/src/AirSim/PythonClient/multirotor/ && python publish_path.py" &
done