#! /usr/bin/env python
# -*- coding: utf-8 -*-

#A bunch of includes I used in a Statistical Physics-excercies, which generally provides what I need

from __future__ import division             # To assure that division between two integers gives a sensible result
import sys                                  # Here we use the 'sys' library to handle command line arguments 
import numpy                                # A (big) library for doing array oriented numerics
import matplotlib as mpl                    # A plotting framework 
from matplotlib import rc                   # Configuration files
mpl.use('PDF')                              # Uncomment to generate figures in PDF format
import matplotlib.pyplot as pyplot
from scipy.integrate import odeint          # To solve systems of 1st order ordinary differential equations
from scipy.optimize  import newton          # Rootfinder using Newton's method
from scipy.integrate import quad            # To do one-dimensional integrals (quadratures)

#V0 is the boundary function used
#Tweaking the fTerms-values it probably a good idea; difficult functions will require a large number
#of Fourier terms, calling for larger steps to plot fewer functions

def V0(u):
	if u<0: return -V0(-u)								#Creates an antisymmetric extension for Fourier purposes
	
	#if (u>1/4 and u<3/4): return 1						#1 This is a heaviside function
	#return 0
	
	return numpy.sin(4*numpy.pi*u)						#3 This is a sine function
	
	#return (1 - (u - 1/2)**4)							#4 This is a sort of quadratic function with non-zero edges
	
	#return (1/16 - (u - 1/2)**4)						#5 This is the same sort of function with zero edges
	
	#return numpy.sin(u*(u-1)*numpy.cosh(u))**3			#6 This is a fairly random function
	
def V0square(u):
	return V0(u)**2
	
#Vterm describes the m'th term in the Fourier series for V
def Vterm(u,v,m):
	return numpy.sin(m*numpy.pi*u)*numpy.sinh(m*numpy.pi*v)
	
#Euterm and Evterm describe the m'th term in the Fourier series for E's u and v-coordinates
def Euterm(u,v,m):
	return numpy.cos(m*numpy.pi*u)*numpy.sinh(m*numpy.pi*v)*m*numpy.pi
	
def Evterm(u,v,m):
	return numpy.sin(m*numpy.pi*u)*numpy.cosh(m*numpy.pi*v)*m*numpy.pi

#The m'th Fourier term, used in integration to determine the Fourier coefficients
def quadFunc(u,m):
	return numpy.sin(m*u*numpy.pi)*V0(u)
	
#Error function for estimating convergence
def errFunc(u,add):
	f = 0
	for n in xrange(1,add[0]):
		f += Vterm(u,1,n)*add[1][n]
	return (f-V0(u))**2


def main(argv):

	fTermsMax = 50										# Max number of Fourier terms to use
	fTermsStep = 1										# Number of new Fourier terms before reevaluating precision
	fTermsCurrent = 0									# Number of Fourier terms currently in use; dynamic, for storage purposes
	gridSize = 50										# Number of subdivisions in the u- and v-direction of the area
	fCoeff = range(0,fTermsMax+1)						# Array for storing the coefficients
	error = 100											# Initializing error as larger than maxError
	maxError = 0.0001 * quad(V0square,-1,1)[0]			# Target for approximation error, relative to the norm of the target function
	
	
	xValues = numpy.linspace(0,1,gridSize+1)
	yValues = numpy.linspace(0,0,gridSize+1)
	
	#Complicated loop; it calculates the Fourier coefficients, while every ?-steps considering if convergence is already satisfactory.
	#It also plots the approximations as it goes along. It's most important function in going forwards is deciding the number of
	#Fourier coefficients to use and setting their value.
	while((error > maxError) and (fTermsCurrent < fTermsMax)):
		if (error != 100): pyplot.plot(xValues, yValues, '-', label="V(u,1) m=%d" %(fTermsCurrent))
		for m in xrange(fTermsCurrent+1,fTermsCurrent+1+fTermsStep):
			fCoeff[m] = quad(quadFunc, -1, 1, m)[0] / numpy.sinh(m*numpy.pi)
			for x in range(gridSize):
				yValues[x] += Vterm(xValues[x],1,m)*fCoeff[m]
		fTermsCurrent += fTermsStep
		error = quad(errFunc, -1, 1, [fTermsCurrent, fCoeff])[0]
						
	#Plots the final approximation
	pyplot.plot(xValues, yValues, '+-r', label="V(u,1) m=%d" %(fTermsCurrent))
	
	#Calculates and pltos the actual boundary function
	for x in range(gridSize):
		yValues[x] = V0(xValues[x])
	pyplot.plot(xValues, yValues, 'xb', label="V_0(u)")

	#More plotting related stuff
	#pyplot.title("Comparison of given and approximated functions at the non-zero boundary")
	pyplot.legend()
	pyplot.xlabel('u')
	pyplot.ylabel('V')
	pyplot.savefig("boundary.pdf")
	pyplot.clf()
	
	#Initializes xValues and yValues as a grid, and also variables to store the valeus of the potential the electrical field components on the grid
	xValues = numpy.linspace(0,1,gridSize+1)
	yValues = numpy.linspace(0,1,gridSize+1)
	zValues = [[0]*(gridSize+1) for x in xrange(gridSize+1)]
	EuValues = [[0]*(gridSize+1) for x in xrange(gridSize+1)]
	EvValues = [[0]*(gridSize+1) for x in xrange(gridSize+1)]
	
	#Caluclates the potential and electrical field components for each point on the grid, with m incrementing over Fourier terms
	for m in range(1,fTermsCurrent+1):
		for x in range(gridSize+1):
			for y in range(gridSize+1):
				zValues[y][x] += Vterm(xValues[x], yValues[y], m)*fCoeff[m]
				EuValues[y][x] += Euterm(xValues[x], yValues[y], m)*fCoeff[m]
				EvValues[y][x] += Evterm(xValues[x], yValues[y], m)*fCoeff[m]
	
	#Plotting for the potential
	CP = pyplot.contourf(xValues, yValues, zValues)
	pyplot.colorbar(CP)
	#pyplot.title('V(u,v)')
	pyplot.xlabel('u')
	pyplot.ylabel('v')
	pyplot.savefig("contourV")
	pyplot.clf()
	
	#Plotting for the electrical field
	pyplot.quiver(xValues,yValues,EuValues,EvValues)
	#pyplot.title('E(u,v)')
	pyplot.xlabel('u')
	pyplot.ylabel('v')
	pyplot.savefig("quiverE")
	pyplot.clf()
	
if __name__ == "__main__":
    main(sys.argv[1:])
