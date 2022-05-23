#include <iostream>

void invert(int * aer, int N) {

	int* buffer = new int[N];
	for (int i = 0; i < N; i++) {
		buffer[i] = aer[i];
	}
	for (int i = 0; i < N; i++){
		aer[i] = buffer[(N - 1) - i];
	}

}
int main(){

	int const AN = 5;
    int A[AN];

	int const BN = 6;
	int B[BN];

	int const CN = 7;
	int C[CN];

	for (int i = 0; i < AN; i++){
		A[i] = i;
	}
	for (int i = 0; i < BN; i++) {
		B[i] = i;
	}
	for (int i = 0; i < CN; i++) {
		C[i] = i;
	}

	invert(A, AN);
	invert(B, BN);
	invert(C, CN);

	for (int i = 0; i < AN; i++){
		std :: cout<<A[i]<<"\t";
	}
	std :: cout << "\n";
	for (int i = 0; i < BN; i++) {
		std::cout << B[i] << "\t";
	}
	std::cout << "\n";
	for (int i = 0; i < CN; i++) {
		std::cout << C[i] << "\t";
	}
	std::cout << "\n";
	
}
