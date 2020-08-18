//============================================================================
// Name        : QuadTree.cpp
// Author      : computation in engineering
// Version     :
// Copyright   : none
// Description : a very simple quadtree implementation with vtk output
//============================================================================

#include <iostream>
#include <fstream>
#include <string>

#include "QuadTree.h"
#include "geometry.h"

using namespace std;

bool implicitFunction(double x, double y)
{
	/*return x > 0.6;*/

	double radius = 0.5;
	return ((x-2.0) * (x-2.0) + (y-2.0) * (y-2.0)) > radius * radius;
}

unsigned int node::myNoOfNodes = 0;

node::node(double xmin, double ymin, double xmax, double ymax, node* father, int level, string stringCode) :
	myXmin(xmin), myXmax(xmax), myYmin(ymin), myYmax(ymax),
	myFather(father), myLevel(level), myStringCode(stringCode),
	myChildren(0)
{
	myNoOfNodes++;
}

void node::writeTreeToConsole()
{
	cout << "Node at level " << myLevel << ": [" << myXmin << ", " << myXmax << "] x [" <<
		myYmin << ", " << myYmax << "]" << endl;

	if (myChildren != NULL)
	{
		for (int i = 0; i < 4; ++i)
		{
			string indentation(2 * (myLevel + 1), ' ');
			cout << indentation << "Sub node " << i << ": ";
			myChildren[i]->writeTreeToConsole();
		}
	}

}

node::~node()
{
	if (myChildren != 0)
	{
		for (int i = 0; i < 4; ++i)
		{
			delete myChildren[i];
		}

		delete[] myChildren;
	}
	myNoOfNodes--;
}

void node::generateQuadtree(int maxLevel)
{
	int numberOfPoints = 5;

	if (myLevel < maxLevel && amIcut(numberOfPoints))
	{
		divideMe();

		for (int i = 0; i < 4; ++i)
		{
			myChildren[i]->generateQuadtree(maxLevel);
		}
	}
}

void node::divideMe()
{
	myChildren = new node*[4];
	myStringCode = "1";
	double middleX = 0.5 * (myXmax + myXmin);
	double middleY = 0.5 * (myYmax + myYmin);

	// North west or top left
	myChildren[0] = new node(myXmin, middleY, middleX, myYmax, this, myLevel + 1, "0");

	// North east or top right
	myChildren[1] = new node(middleX, middleY, myXmax, myYmax, this, myLevel + 1, "0");

	// South west or bottom left
	myChildren[2] = new node(myXmin, myYmin, middleX, middleY, this, myLevel + 1, "0");

	// South east or bottom right
	myChildren[3] = new node(middleX, myYmin, myXmax, middleY, this, myLevel + 1, "0");
}

bool node::amIcut(int noPoints)
{
	bool isInside = implicitFunction(myXmin, myYmin);
	double n = (noPoints - 1);

	for (int i = 0; i < noPoints; ++i)
	{
		for (int j = 0; j < noPoints; ++j)
		{
			double x = (myXmax - myXmin) * i / n + myXmin;
			double y = (myYmax - myYmin) * j / n + myYmin;

			if (implicitFunction(x, y) != isInside)
			{
				return true;
			}
		}
	}

	return false;
}



void node::writePointsToVtk(ofstream& outfile) {
	//corner vertices of this cell in a counterclockwise order
	outfile << myXmin << "\t" << myYmin << "\t" << "0" << endl;
	outfile << myXmax << "\t" << myYmin << "\t" << "0" << endl;
	outfile << myXmax << "\t" << myYmax << "\t" << "0" << endl;
	outfile << myXmin << "\t" << myYmax << "\t" << "0" << endl;
	for (int i = 0; i<4; i++) {
		if (myChildren!=0) {
			myChildren[i]->writePointsToVtk(outfile);
		}
	}
}

void node::writeNodeCodesToVtk(ofstream& outfile) {
	
	outfile << myStringCode << endl;
	for (int i = 0; i<4; i++) {
		if (myChildren != 0) {
			myChildren[i]->writeNodeCodesToVtk(outfile);
		}
	}
}

void node::writeTreeToVtk(const char* filename) {

	ofstream outfile;

	outfile.open(filename);
	outfile << "# vtk DataFile Version 4.2" << endl;
	outfile << "Test Data" << endl;
	outfile << "ASCII" << endl;
	outfile << "DATASET UNSTRUCTURED_GRID" << endl;

	//output the points
	outfile << "POINTS " << 4 * myNoOfNodes << " " << "double " << endl;
	writePointsToVtk(outfile);
	//output the cells
	outfile << "CELLS " << myNoOfNodes << " " << 5 * myNoOfNodes << endl;
	//Quickie: I rely on the order of the points here
	for (size_t i = 0; i<myNoOfNodes * 4; i += 4)
		outfile << "4\t" << i << "\t" << i + 1 << "\t" << i + 2 << "\t" << i + 3 << endl;
	//output cell types
	outfile << "CELL_TYPES " << myNoOfNodes << endl;
	for (size_t i = 0; i<myNoOfNodes; i++)
		outfile << "9" << endl;
	//outfile << "CELL_DATA " << myNoOfNodes << endl;
	//outfile << "SCALARS Node_Number double" << endl;
	//outfile << "LOOKUP_TABLE default" << endl;
	//writeNodeCodesToVtk(outfile);
	outfile.close();

}
