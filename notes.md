# Aims of the project is learn between robots based on vision.

- Share the graph knowledge between robot.
- Indicate the shorted path for robot.
- Identify osticles and navigate around it.
- Adapt to moving target ?

# Tasks
 - [x] Test the drone controller and the movement.
 - [x] Test the car controller and the movement.
 - [ ] Collect data and develop the server side algorithm.
 - [ ] Write the code for the quad code for controller and movement.

# Notes
## Working of skynet

### Requirements
- Given an image  of start point and end point image of the environment. Give shortest feasible path.
- If robot is free maximize the information gain with minimal cost.

### Algorithm
- The algorithm is divided into three parts

#### 1. Graph creation
- When a robot is commanded to move to a point it will take a image of the environment.
- The image and location of the robot is sent to the server ( skynet - client).
- Based on the distance threshold, we will selecte a node or create a node.
- The image is compared against other images in the nodes. Similarity of the images are analysed.
  - If the image is similar to the top image in the node, the image is discarded. weight of the image is increased.
  - If the image is not similar to the image in the node, the image is added to the node.
  - the images are then sorted based on the weight.
- If there is not edge between the previous node then a edge is created between the previous location and the current location.
- In the edge the robot name will be added. 
- If there is the edge between the previous node then the robot name will be appended to the edge.

#### 2. Graph path search.
- When a robot is commanded to move to a point it will take a image of the environment and the destination image.
- The root image is search based on the ranging fo each node image. This is the starting point.
- The destination image is search based on the ranging fo each node image. This is the destination point.
- The path is searched using the Dijkstra algorithm.

#### 3. Graph exploration
- If the robot is free it will explore the graph.
- If the node is has less weight then explore the node.

