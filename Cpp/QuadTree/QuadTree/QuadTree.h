/*
* QuadTree.hpp
*
*      Author: computation in engineering
*/
#ifndef QUADTREE_HPP_
#define QUADTREE_HPP_
#include <fstream>
using namespace std;

bool implicitFunction(double x, double y);

class node {
private:
	node** myChildren = NULL;
	// the convention is
	// myChildren[0] = NW  myChildren[1] = NE
	// myChildren[2] = SW  myChildren[3] = SE

	double myXmin, myYmin, myXmax, myYmax; //bounding box
										   //"convinience" members
	node*  myFather;
	int myLevel; // remember the depth I am located at
	string myStringCode; //which code do I have?

	//just for counting how many nodes exist in the tree
	static unsigned int myNoOfNodes;

	//helper functions
	void divideMe();
	bool amIcut(int noPoints);

	//output functions
	void writePointsToVtk(ofstream&);
	//void writeCellsToVtk(ofstream&);
	void writeNodeCodesToVtk(ofstream& outfile);

	//prohibit implicit casts and copy constructors
	explicit node(const node&);
	//prohibit copy construction
	node& operator=(const node&);

public:
	node(double xmin, double ymin, double xmax, double ymax, node* father, int level, string stringCode);
	~node();

	void generateQuadtree(int maxLevel);

	//output
	void writeTreeToConsole();

	void writeTreeToVtk(const char* filename);
};

#endif /* QUADTREE_HPP_ */
