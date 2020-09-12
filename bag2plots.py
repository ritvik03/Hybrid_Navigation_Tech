import argparse
import rosbag
import rospy
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
from mpl_toolkits.mplot3d import Axes3D

def list2dictList(path_list):
    result = []
    for index,path_point in enumerate(path_list):
        point_data = {"timestamp":index*1.0/10000,#path_point.header.stamp.secs+path_point.header.stamp.nsecs/10000000,
                      "tx":path_point.pose.position.x,
                     "ty":path_point.pose.position.y,
                     "tz":path_point.pose.position.z,
                     "qx":path_point.pose.orientation.x,
                     "qy":path_point.pose.orientation.y,
                     "qz":path_point.pose.orientation.z,
                     "qw":path_point.pose.orientation.w}
        result.append(point_data)
    
    df = pd.DataFrame(result)
    return df

def read_bag_file(bagfile,ground_truth_topic,pose_graph_topic):
    
    pose_graphs = []
    ground_paths = []
    print("[INFO] Reading bagfile data. This might take a while, depending on size of path (~30 mins)")
    with rosbag.Bag(bagfile,'r') as bag:
        t_old = time.time()
        for topic, msg, t in bag.read_messages(topics=[ground_truth_topic,pose_graph_topic]):
        
            if topic==pose_graph_topic: #"/pose_graph/pose_graph_path":#"/path_ritvik":#"/airsim_node/drone/odom_local_ned":
                pose_graphs = msg.poses
            
            if topic==ground_truth_topic: #"/path_ritvik":#"/airsim_node/drone/odom_local_ned":
                ground_paths = msg.poses
        
            print(t)
        
        print("[INFO] Time taken: "+str(time.time()-t_old))
        bag.close()

    return pose_graphs,ground_paths

def parse_arguments():
    parser = argparse.ArgumentParser(description='Plot errors from trajectory and ground truth bag file')
    parser.add_argument('b', help='path to bag file')
    parser.add_argument('-d', default="error_evaluation/", help='path to directory to store error files')
    parser.add_argument('-g', default="/path_ritvik", help='topic where ground truth is published')
    parser.add_argument('-p', default="/pose_graph/pose_graph_path", help='topic where ground truth is published')
    # parser.print_help()
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_arguments()
    
    ground_truth_topic = args.g
    pose_graph_topic = args.p
    bagfile = args.b
    error_dir = args.d
    print(bagfile,error_dir,ground_truth_topic,pose_graph_topic)

    pose_graphs,ground_paths = read_bag_file(bagfile,ground_truth_topic,pose_graph_topic)
    print("[INFO] Length of pose_graphs, ground_paths: "+str(len(pose_graphs))+", " +str(len(ground_paths)))
    
    ground_data = list2dictList(ground_paths)
    pred_data = list2dictList(pose_graphs)
    cols = ["timestamp","tx","ty","tz","qx","qy","qz","qw"]
    ground_data = ground_data[cols]
    pred_data = pred_data[cols]

#     ground_data  = ground_data.sort_values(by="timestamp")
#     pred_data = pred_data.sort_values(by="timestamp")

    ground_data.to_csv(os.path.join(error_dir,"stamped_groundtruth.txt"),index=False,sep=' ', header=None)
    pred_data.to_csv(os.path.join(error_dir,"stamped_traj_estimate.txt"),index=False,sep=' ',header=None)
    
    ground_data.to_csv(os.path.join(error_dir,"stamped_groundtruth.csv"),index=False, header=None)
    pred_data.to_csv(os.path.join(error_dir,"stamped_traj_estimate.csv"),index=False,header=None)

    # ground_data.to_csv(r'error_evaluation/stamped_groundtruth2.txt', header = None, index=None, sep=' ', mode='a')
    # pred_data.to_csv(r'error_evaluation/stamped_traj_estimate2.txt', header = None, index=None, sep=' ', mode='a')

    print("[INFO] Running RPG error evaluation")
#     cmd = "python2 rpg_trajectory_evaluation/scripts/analyze_trajectory_single.py "+error_dir +" --png"
    cmd = "python preprocess_data.py"
    print("[INFO] Executing Command: $"+cmd)
    os.system(cmd)
    
    cmd = "python2 rpg_trajectory_evaluation/scripts/analyze_trajectory_single.py "+error_dir +" --png"
    print("[INFO] Executing Command: $"+cmd)
    os.system(cmd)
    
    cmd = "evo_traj tum -as error_evaluation/traj_est.csv --ref error_evaluation/grundtruth.csv -p --t_max_diff 0.1"
    print("[INFO] Executing Command: $"+cmd)
    os.system(cmd)