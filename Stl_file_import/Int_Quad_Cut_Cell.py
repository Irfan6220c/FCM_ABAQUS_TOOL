# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 00:59:39 2018

@author: Boulbrachene
"""
import numpy as np
import numpy.linalg as la

class Cut_Element_Integration:

    def __init__(self, nodal_coordinates, E, t, prxy,Integration_points):
        self._nodal_coordinates = nodal_coordinates
        self._E = E
        self._t = t
        self._prxy = prxy
        self.Xi_points = []
        self.Eta_points = []
        self.Weights = []
        self.Alpha_value_GP = []
        
        for i in range (0,len(Integration_points)):
            self.Xi_points.append(Integration_points[i][0])
            self.Eta_points.append(Integration_points[i][1])
            self.Weights.append(Integration_points[i][2])
            self.Alpha_value_GP.append(Integration_points[i][3])


    @property
    def E(self):
        return self._E
    @E.setter
    def E(self, value):
        self._E = value

    @property
    def t(self):
        return self._t
    @t.setter
    def t(self, value):
        self._t = value
    
    @property
    def prxy(self):
        return self._prxy
    @prxy.setter
    def prxy(self, value):
        self._prxy = value


    def calculate_elastic_stiffness_matrix(self):
        """Calculate Stiffness Matrix for one quadrilateral element
        
        Returns
        -------
        Ke : array_like
            element stiffness matrix
        """

        K_e = np.zeros((8,8))

#        GP = np.array([-0.577350269189626, 0.577350269189626])
#        WtFac = np.array([1., 1.])

        D = self._comp_mat_matrix_plane_stress()

        for i in range(len(self.Eta_points)):
            gp_eta = self.Eta_points[i]         #current gauss point coordinate eta
            gp_w = self.Weights[i]          #current gauss point weight in eta
            gp_xi = self.Xi_points[i]      #current gauss point coordinate xi
            alpha_GP = self.Alpha_value_GP[i]
            J = self._calculate_Jacobian(gp_xi, gp_eta)
            J_inv = la.inv(J)
            det_J = la.det(J)

            B = self._calculate_B_matrix(gp_xi, gp_eta, J_inv)

            K_e += (np.dot(np.dot(B.T, D) ,B)) * det_J *gp_w*alpha_GP
            
        ##multiply with thickness
        K_e *= self._t
        
        return K_e
    

    def _comp_mat_matrix_plane_stress(self):
        """Calculates the constant material matrix
        
        Returns
        -------
        D : array_like
            the material matrix
        """
        E = self._E
        prxy = self._prxy
        D = np.matrix([ [1,    prxy, 0         ],
                        [prxy, 1,    0         ],
                        [0,    0,    (1-prxy)/2] ])
        D *= E / (1 - prxy**2)
        return D

    
    def _calculate_B_matrix(self, xi, eta, J_inv):
        """Calculates the bending B matrix

        Parameters
        ----------
        xi : float
            xi coordinate of the gauss point
        eta : float
            eta coordinate of the gauss point
        J_inv : array_like
            the inverse of the jacobian matrix

        Returns
        -------
        B : array_like
            B (stress-strain) operator
        """
        ##calculate B matrix
        B = np.zeros((3,8))      #initialize B
        dN_dxi_deta = self.calculate_shapefunctions_derivatives(xi, eta)
        dN_dx_dy = np.dot(J_inv, dN_dxi_deta)
       # n_nodes = 4
        for j in range(4):
            B[0,j*2+0] = dN_dx_dy[0,j]
            B[0,j*2+1] = 0
            B[1,j*2+0] = 0
            B[1,j*2+1] = dN_dx_dy[1,j]
            B[2,j*2+0] = dN_dx_dy[1,j]
            B[2,j*2+1] = dN_dx_dy[0,j]
#        j=2
#        B[0,4] = dN_dx_dy[0,3]
#        B[0,5] = 0
#        B[1,4] = 0
#        B[1,5] = dN_dx_dy[1,3]
#        B[2,4] = dN_dx_dy[1,3]
#        B[2,5] = dN_dx_dy[0,3]
##        j=3
#        B[0,6] = dN_dx_dy[0,2]
#        B[0,7] = 0
#        B[1,6] = 0
#        B[1,7] = dN_dx_dy[1,2]
#        B[2,6] = dN_dx_dy[1,2]
#        B[2,7] = dN_dx_dy[0,2]
        return B


    def calculate_shape_functions(self, xi, eta):
        """Calculates the bilinear shape functions

        Parameters
        ----------
        xi : float
            xi coordinate of the gauss point
        eta : float
            eta coordinate of the gauss point

        Returns
        -------
        N : array_like
            [N1, N2, N3, N4]
        
        Raises
        ------
        NotImplementedError
            If the number of the nodes does not equal 4
        """
        N1 = ((1.0-xi)*(1.0-eta))/4.0  #shapefunction node 1
        N2 = ((1.0+xi)*(1.0-eta))/4.0  #shapefunction node 2
        N3 = ((1.0+xi)*(1.0+eta))/4.0  #shapefunction node 3
        N4 = ((1.0-xi)*(1.0+eta))/4.0  #shapefunction node 4
        N = np.array([N1,N2,N3,N4])
        return N
    

    def calculate_shapefunctions_derivatives(self, xi ,eta):
        """Calculates the bilinear shape function derivatives wrt. the paremtric coordinates

        Parameters
        ----------
        xi : float
            xi coordinate of the gauss point
        eta : float
            eta coordinate of the gauss point

        Returns
        -------
        dN : array_like
            [[dN1dx, dN2dx, dN3dx, dN4dx]
             [dN1dy, dN2dy, dN3dy, dN4dy]]
        
        Raises
        ------
        NotImplementedError
            If the number of the nodes does not equal 4
        """
        #w.r.t xi
        dN1_dxi = ((-1)*(1-eta))/4  #shapefunction node 1
        dN2_dxi = (( 1)*(1-eta))/4  #shapefunction node 2
        dN3_dxi = (( 1)*(1+eta))/4  #shapefunction node 3
        dN4_dxi = ((-1)*(1+eta))/4  #shapefunction node 4
        #w.r.t eta
        dN1_deta = ((1-xi)*(-1))/4  #shapefunction node 1
        dN2_deta = ((1+xi)*(-1))/4  #shapefunction node 2
        dN3_deta = ((1+xi)*( 1))/4  #shapefunction node 3
        dN4_deta = ((1-xi)*( 1))/4  #shapefunction node 4

        dN = np.matrix([[dN1_dxi,  dN2_dxi,  dN3_dxi,  dN4_dxi],
                        [dN1_deta, dN2_deta, dN3_deta, dN4_deta]])
        return dN
    

    def _calculate_Jacobian(self, xi, eta):
        """Calculates the Jacobian of the element
        
        Parameters
        ----------
        xi : float
            xi coordinate of the gauss point
        eta : float
            eta coordinate of the gauss point
        
        Returns
        -------
        J : array_like
            The jacobian matrix
        """
        nodal_coordinates = self._nodal_coordinates
        dN_dxi_deta = self.calculate_shapefunctions_derivatives(xi, eta)
        J = np.dot(dN_dxi_deta, nodal_coordinates)
        return J




#element = QuadPlateMembrane(
#    nodal_coordinates = [[0, 0], [1, 0], [1, 1], [0, 1]],
#    E = 200,
#    t = 1,
#    prxy = 0.3)
#
#k = element.calculate_elastic_stiffness_matrix()
#print(k)
    