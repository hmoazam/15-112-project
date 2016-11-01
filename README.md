# 15-112-project
Summary
I plan to make an interactive map of the ground floor of CMUQ. It will allow users to select their starting location and destinations (or enter the destination), on screen, and then provide them with the shortest route to their destination.

Libraries and features that I will be using/implementing include:
•	Tkinter 
•	Graph libraries (which one to be decided)
•	Djikstra’s shortest path algorithm
              *this list may be added to if I require any additional functionality

User interface of the project 
The interface will be the map itself, with the various nodes (possible locations) visible. Clicking on a node will activate it, and then allow you to select a second node (your destination). These both change colour. Then, once both nodes are selected, the shortest path between the two locations will be drawn on the map. There will also be the option of entering the destination/choosing it from a list and then constructing a path from the starting node selected and then drawing the path.

List of features that I will implement and demo by the first milestone:
•	Initialising the nodes and paths for half of the ground floor - focus on the offices side/CS corridor
•	Colour change of nodes and drawing the shortest path

List of features that will be included if time permits:
•	Time of travel 
•	Hover over node to show room number/location name
