/*
* main.cpp
*
*  Created on: Nov 25, 2013
*      Author: stefan
*/

#include <iostream>
#include <stdio.h>
#include "QuadTree.h"

using namespace std;

int main() {
	cout << "This is the simplest quadtree I know, add functionality if you like" << endl;
	cout << "start generating the tree" << endl;
	node* tree = new node(0.0, 0.0, 4.0, 4.0, NULL, 0, "0");

	tree->generateQuadtree(5);
	tree->writeTreeToConsole();
	cout << "generating the tree finished" << endl;
	cout << "start writing" << endl;
	tree->writeTreeToVtk("quadTree.vtk"); // paraview
	cout << "writing finished" << endl;
	
	delete tree;

	system("pause");

	return 0;
}
