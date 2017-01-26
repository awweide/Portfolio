#include <iostream>
#include <math.h>
#include <time.h>
#include <sstream>
#include <fstream>

#define N 32					// Defines the maximum possible grid size
//#define T 2.1556				// Defines the starting temperature
#define t 0.02					// Defines the relative temperature
#define WARMRUNS 10000000	// Defines the amount of flip-attempts to burn-in
#define TRUERUNS 10000000	// Defines the number of samplings after burn-in
#define TEMPINCR 0.00		// Defines the stepsize when increasing temperature
#define TEMPRUNS 1			// Defines the number of temperature steps
#define OUTPUT "c0p02.txt"

using namespace std;

//Initializes NX&NY, which represent the -effective- size of the grid, while N merely allocates sufficient memory
int NX, NY;

//Initializes pointers to next element in the lattice in a periodic fashion; l=left, etc
//These limit the -effective- size of the grid, by point for instance a leftwards step for x=8 to x=0
int pointl[N], pointr[N], pointu[N], pointd[N];

//Initializes the lattice as a N*N 2D grid. Actual geometry is represented by pointx and formulae
int grid[N][N];

//Initializes the two coordinates, energychange for the torus geometry
//and current energydifference between torus and klein hamiltonians
int X, Y, dEt, delta;

//Initializes beta, the inverse of T, to avoid repeatedly inverting later on; and summation, for calculating the < >_t
//as well as tau, the line tension free energy
double beta, summation, tau;


//Prints the grid's state; troubleshooting tool
void print(){
	for(int x=0;x<NX;++x){
		for(int y=0;y<NY;++y){
			if (grid[x][y] == 1) cout << '+';
			else cout << '-';
			cout << ' ';
		}
		cout << endl;
	}
}


//Calculates the torus-Hamiltonian of the grid; this will always be an integer, even after divided by 2
//Skips all points which do not cross the seam, seeing as these cancel against the klein-Hamiltonian anyway
//And we are never really interested in the actual energy of the torus
//Also calculates only one way across the seam, multiplying by 2 by symmetry, which in turn cancels against the 1/2
//The - is represented by -=
//In total; only calculates energies for interactions across the seam

int torusH(){
	int sum = 0;
	for(int y=0;y<NY;++y){
		sum -= grid[0][y]*grid[NX-1][y];
	}
	return sum;
}

//Calculates the klein-Hamiltonian in a similar fashion
//The - sign from the Hamiltonian cancels against the - from crossing the klein seam
//The mobius property is preserved by making y and NY-1-y as neighbours
int kleinH(){
	int sum = 0;
	for(int y=0;y<NY;++y){
		sum += grid[0][y]*grid[NX-1][NY-1-y];
	}
	return sum;
}



void main(){
	double Tc = 2.0/(log(1+sqrt(2.0)));
	double T = Tc*(t-1);

	//Opens output file for writing
	ofstream target;
	target.open(OUTPUT);
	
	for(NY=2;NY<20;++NY){
	
	//Sets current effective grid size
	NX = NY;




	//Seeds random function
	srand(time(NULL));

	//Sets correct values for pointers
	for(int i=0;i<NX;++i){
		pointl[i] = i - 1;
		pointr[i] = i + 1;
	}
	for(int i=0;i<NY;++i){
		pointu[i] = i + 1;
		pointd[i] = i - 1;
	}
	pointl[0] = NX-1; pointr[NX-1] = 0; pointd[0] = NY-1; pointu[NY-1] = 0;

	//OUTER LOOP FOR INCREMENTING THROUGH MULTIPLE TEMPERATURES
	for(int tempruns=0;tempruns<TEMPRUNS;++tempruns){
	
		//Sets beta to inverse of current temperature, resets summation variable
		beta = 1.0/(T+TEMPINCR*tempruns);
		summation = 0;
		
		//Initializes grid with random values for spin
		for(int x=0;x<NX;++x) for(int y=0;y<NY;++y) grid[x][y] = ((int(rand()%2) * 2 - 1));

		//WARMING UP TO ERASE THE INITAL CONFIGURATION AND ACHIEVE A QUASI-STEADY STATE
		//This is a stripped down version of the next loop
		for(int runs=0;runs<WARMRUNS;++runs){
			//Gets random, valid values for coordinates
			X = int(rand()%NX); Y = int(rand()%NY);
		
			//Calculates new energy minus old energy for the torus for flipping the spin at (X,Y)
			//Note that new spin = -old spin, such that new spin - old spin = -2 old spin
			//And furthermore, -2 old spin * -1/2 totals to old spin * unity
			//Finally, every pair should be counted twice; each acting as centre once and neighbour once
			dEt = 2*grid[X][Y] * (grid[pointr[X]][Y] + grid[pointl[X]][Y] + grid[X][pointu[Y]] + grid[X][pointd[Y]]);
		
			//Flips if energydecrease or with a certain probability if energyincrease
			
			if ( (exp(-1.0 * dEt * beta)) > ( ((double)rand() + 1) / (double)RAND_MAX ) ) grid[X][Y] *= -1;
		}
	
	
		//Initializes starting energydifference, such that only its change needs to be tracked
		delta = kleinH() - torusH();

		//AVERAGING OVER QUASI-STABLE STATES
		for(int runs=0;runs<TRUERUNS;++runs){
			//Gets random, valid values for coordinates
			X = int(rand()%NX); Y = int(rand()%NY);
				

			//Calculates new energy minus old energy for the torus for flipping of spin at (X,Y)
			//Note that new spin = -old spin, such that new spin - old spin = -2 old spin
			//And furthermore, -2 old spin * -1/2 totals to old spin * unity
			//Finally, every pair should be counted twice; each acting as centre once and neighbour once
			dEt = 2*grid[X][Y] * (grid[pointr[X]][Y] + grid[pointl[X]][Y] + grid[X][pointu[Y]] + grid[X][pointd[Y]]);
			

			//Flips if energydecrease or with a certain probability if energyincrease
			//Updates current energies if flipping occurs
			
			
			if ( (exp(-1.0 * dEt * beta)) > ( ((double)rand() + 1) / (double)RAND_MAX ) ) {
		
		
				//Checks for the special seam; else, no change in delta
				if (X==0) delta -= 2*grid[0][Y] * (grid[NX-1][NY-Y-1] + grid[NX-1][Y]);
				else if (X==NX-1) delta -= 2*grid[X][Y] * (grid[0][NY-Y-1] + grid[0][Y]);
				grid[X][Y] *= -1;
			}
			//Summation is used to count the total energies; normalization for averaging occurs later
			summation += exp(-1.0 * delta * beta);
			if ((-1.0 * delta * beta) < -300) cout << "Overflow error!" << endl;
			
			
		}
	
		//Tests so see if the final energy of continously updating is the same as the actual energy
		//Troubleshooting - errorchecking
		if ((kleinH()-torusH()) != delta) cout << "Error in delta energy!" << endl;
	
		//Calculates tau
		tau = -1 * (T+TEMPINCR*tempruns) * log(summation / (TRUERUNS + 0.0)) / NY;
		
		//Notifies of printing, prints to output file
		cout << "Outputting for " << NX << endl;
		target << (1.0/((NX+0.0)*t)) << ' ' << (tau/t) << endl;
	}
	}
	//Closes output file
	target.close();
}
