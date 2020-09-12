#!/usr/bin/env python
# coding: utf-8

# In[2]:


import rosbag
import rospy
import matplotlib.pyplot as plt
import pandas as pd
import time
get_ipython().magic('matplotlib notebook')
from mpl_toolkits.mplot3d import Axes3D


# In[4]:


bagfile = "../bag_files/8.bag"
ground_truth_topic = "/path_ritvik"
pose_graph_topic = "/pose_graph/pose_graph_path"


# In[6]:


get_ipython().system('rosbag info ../bag_files/8.bag')


# In[17]:


bag = rosbag.Bag(bagfile)
topics = bag.get_type_and_topic_info()[1].keys()
t_start,t_end = bag.get_start_time(),bag.get_end_time()
# print(topics)
print(t_start,t_end)


# In[21]:


pose_graphs = []
ground_paths = []
t_start,t_end = bag.get_start_time(),bag.get_end_time()
print("[INFO] Reading bagfile data. This might take a while, depending on size of path (~30 mins)")
with rosbag.Bag(bagfile,'r') as bag:
    t_old = time.time()
    for topic, msg, t in bag.read_messages(topics=[ground_truth_topic,pose_graph_topic]):
        
        if topic=="/pose_graph/pose_graph_path":#"/path_ritvik":#"/airsim_node/drone/odom_local_ned":
#             pose_graphs.append(msg.poses[-1])
            pose_graphs = msg.poses
            
        if topic=="/path_ritvik":#"/airsim_node/drone/odom_local_ned":
#             ground_paths.append(msg.poses[-1])
            ground_paths = msg.poses
        
        print(t)
        
    print("[INFO] Time taken: "+str(time.time()-t_old))
    bag.close()


# In[22]:


len(pose_graphs), len(ground_paths)


# In[23]:


pose_graphs[3]


# In[58]:


# pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.reset_option('display.float_format')
def list2dictList(path_list):
    result = []
    for path_point in path_list:
        point_data = {"timestamp":path_point.header.stamp.secs+path_point.header.stamp.nsecs/10000000,
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


# In[59]:


ground_data = list2dictList(ground_paths)
pred_data = list2dictList(pose_graphs)


# In[60]:


cols = ["timestamp","tx","ty","tz","qx","qy","qz","qw"]
ground_data = ground_data[cols]
pred_data = pred_data[cols]


# In[61]:


ground_data


# In[64]:


ground_data.to_csv("error_evaluation/ground_data.csv",index=False)
pred_data.to_csv("error_evaluation/pose_graph_data.csv",index=False)
ground_data.to_csv(r'error_evaluation/stamped_groundtruth.txt', header = None, index=None, sep=' ', mode='a')
pred_data.to_csv(r'error_evaluation/stamped_traj_estimate.txt', header = None, index=None, sep=' ', mode='a')


# In[65]:


ground_data[ground_data['timestamp']=='timestamp']


# In[63]:


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(ground_data["tx"],ground_data["ty"],ground_data["tz"],color='r')
ax.plot(pred_data["tx"],pred_data["ty"],pred_data["tz"],color='g')


# In[ ]:




