#include <iostream>
#include <iomanip>  
#include <time.h>
#include <cstdlib>
#include <vector>
#include <unordered_set>
#include <fstream>

using namespace std;

bool isMagicSquare(vector<vector<int>> square, int n) 
{
    unordered_set<int> uniqueNums;
    for (int i = 0; i < n; i++) 
	{
        for (int j = 0; j < n; j++) 
		{
            uniqueNums.insert(square[i][j]);
        }
    }
    if (uniqueNums.size() != n * n)
	{
        return false;
    }
    
    int targetSum = n * (n * n + 1) / 2;
    for (int i = 0; i < n; i++) 
	{
        int rowSum = 0;
        int colSum = 0;
        for (int j = 0; j < n; j++) 
		{
            rowSum += square[i][j];
            colSum += square[j][i];
        }
        if (rowSum != targetSum || colSum != targetSum) 
		{
            return false;
        }
    }
    int diagSum1 = 0;
    int diagSum2 = 0;
    for (int i = 0; i < n; i++) 
	{
        diagSum1 += square[i][i];
        diagSum2 += square[i][n-i-1];
    }
    if (diagSum1 != targetSum || diagSum2 != targetSum) 
	{
        return false;
    }
    
    return true;
}

void tcmagic(int n, const char* filename)
{
	vector<vector<int>> matris(n, vector<int>(n, 0));

	int m = 0;
	for(int i = 0; i < n; i++)
	{
		for(int k = 0; k < n; k++)
		{
			matris[i][k] = k + 1 + n * m;
		}
		m++;
	}
	int k, mi, mj;
	k = (n - 2) / 4;
	for (mi = 0; mi < k; mi++)
	{
		for (mj = k + 1; mj < 2 * k + 1; mj++)
		{
            swap(matris[mi][mj], matris[mi][4 * k + 2 - mj - 1]);
		}
	}

	for (mi = 3 * k + 2; mi < 4 * k + 2; mi++)
	{
		for (mj = k + 1; mj < 2 * k + 1; mj++)
		{
            swap(matris[mi][mj], matris[mi][4 * k + 2 - mj - 1]);
		}
	}

	for (mj = 0; mj < k; mj++)
	{
		for (mi = k + 1; mi < 2 * k + 1; mi++)
		{
            swap(matris[mi][mj], matris[4 * k + 2 - mi - 1][mj]);
		}
	}

	for (mj = 3 * k + 2; mj < 4 * k + 2; mj++)
	{
		for (mi = k + 1; mi < 2 * k + 1; mi++)
		{
            swap(matris[mi][mj], matris[4 * k + 2 - mi - 1][mj]);
		}
	}

	for (mi = 0; mi < k; mi++)
	{
	    for (mj = k + 1; mj < 3 * k + 1; mj++)
		{
            swap(matris[mi][mj], matris[4 * k + 2 - mi - 1][mj]);
		}
	}

	for (mj = 0; mj < k; mj++)
	{
		for (mi = k + 1; mi < 3 * k + 1; mi++)
		{
            swap(matris[mi][mj], matris[mi][4 * k + 2 - mj - 1]);
		}
	}

	for (int a = 0; a < n / 2; a++)
	{
		if (a != k)
		{
            swap(matris[a][3 * k + 1], matris[4 * k + 2 - a - 1][3 * k + 1]);
	    }
    }
	for (int a = k + 1; a <= 3 * k; a++)
	{
        swap(matris[a][k], matris[a][3 * k + 1]);
	}

    swap(matris[n / 2][k], matris[n / 2][3 * k + 1]);

	for (int a = 0; a < n / 2; a++)
	{
		if (a != k)
		{
            swap(matris[3 * k + 1][a], matris[3 * k + 1][4 * k + 2 - a - 1]);
		}
	}

	for (int a = 0; a < n / 2; a++)
	{
		if (a != k)
		{
            swap(matris[k][a], matris[k][4 * k + 2 - a - 1]);
		}
	}

	for (int a = k + 1; a <= 3 * k; a++)
	{
        swap(matris[k][a], matris[3 * k + 1][a]);
	}

    swap(matris[k][0], matris[3 * k + 1][0]);

	for (int a = k + 1; a < n / 2; a++)
	{
        swap(matris[0][a], matris[0][4 * k + 2 - a - 1]);
	}

	for (int a = 0; a < k; a++)
	{
        swap(matris[n / 2][a], matris[n / 2][4 * k + 2 - a - 1]);
	}
			
	ofstream file(filename);
	for(int i = 0; i < n; i++)
	{
		for(int k = 0; k < n; k++)
		{
			file << setw(5) << matris[i][k];
		}
		file << endl;
	}
	file << endl;	
		
	int toplam=0;
	for(int i = 0; i < n; i++)
	{
		toplam = toplam + matris[1][i];
	}
	file << "Sum of Rows : " << toplam << endl << endl << endl;
	file.close();
}

void ccmagic(int n, const char* filename)
{
	vector<vector<int>> matris(n + 1, vector<int>(n + 1, 0));
    vector<int> yenimatris((n * n) / 8, 0);
    vector<int> yenimatris1((n * n) / 8, 0);
    vector<int> yenimatris2((n * n) / 8, 0);
    vector<int> yenimatris3((n * n) / 8, 0);
	for(int a = 1; a <= n; a++)
	{
		for(int b = 1; b <= n; b++)
		{
			matris[a][b] = 0;
		}
	}
	
	int m = 0;
	for(int i = 1; i <= n; i++)
	{
		for(int k = 1; k <= n; k++)
		{
			matris[i][k] = k + n * m;
		}
		m++;
	}
	
	int sayici = 0;
	for(int i = 1; i <= n / 4; i++)
	{
		for(int k = n / 4 + 1; k <= 3 * n / 4; k++)
		{
			yenimatris[sayici] = matris[i][k];
			sayici++;
		}
	}
	int sayici1 = 0;
	for(int i = 3 * n / 4 + 1; i <= n; i++)
	{
		for(int k = n / 4 + 1; k <= 3 * n / 4; k++)
		{
			yenimatris1[sayici1] = matris[i][k];
			sayici1++;
		}
	}

	for(int i = 3 * n / 4 + 1; i <= n; i++)
	{
		for(int k = n / 4 + 1; k <= 3 * n / 4; k++)
		{
			matris[i][k] = yenimatris[sayici - 1];
			sayici--;
		}
	}
	
	for(int i = 1; i <= n / 4; i++)
	{
		for(int k = n / 4 + 1; k <= 3 * n/4; k++)
		{
			matris[i][k] = yenimatris1[sayici1 - 1];
			sayici1--;
		}
	}

	int sayici2 = 0;
	for(int i = n / 4 + 1; i <= 3 * n / 4; i++)
	{
		for(int k = 1; k <= n / 4; k++)
		{
			yenimatris2[sayici2] = matris[i][k];
			sayici2++;
		}
	}

	int sayici3 = 0;
	for(int i = n / 4 + 1; i <= 3 * n / 4; i++)
	{
		for(int k = 3 * n / 4 + 1;k <= n; k++)
		{
			yenimatris3[sayici3] = matris[i][k];
			sayici3++;
		}
	}

	for(int i = n / 4 + 1; i <= 3 * n / 4; i++)
	{
		for(int k = 1; k <= n / 4; k++)
		{
			matris[i][k] = yenimatris3[sayici3 - 1];
			sayici3--;
		}
	}
	
	for(int i = n / 4 + 1; i <= 3 * n / 4; i++)
	{
		for(int k = 3 * n / 4 + 1; k <= n; k++)
		{
			matris[i][k] = yenimatris2[sayici2 - 1];
			sayici2--;
		}
	}
	
	ofstream file(filename);
	for(int i = 1; i <= n; i++)
	{
		for(int k = 1; k <= n; k++)
		{
			file << setw(5)<<matris[i][k];
		}
		file << endl;
	}
	file << endl;	

	int toplam=0;
	for(int i = 1; i <= n; i++)
	{
		toplam = toplam + matris[1][i];
	}
	file << "Sum of Rows: " << toplam << endl << endl;
	file.close();
}

void tmagic(int n, const char* filename)
{
    vector<vector<int>> matrix(n, vector<int>(n, 0));
	int bas = n / 2;
	int bas1 = n - 1;
	int a = 1;
	while(a != (n * n) + 1)
	{
		if(matrix[bas % n][bas1 % n] == 0)
		{
			matrix[bas % n][bas1 % n] = a;
		}
		else
		{
			if((bas - 1) % n < 0)
			{
				bas = bas + 3;
			}
			if((bas1 - 2) % n < 0)
			{
				bas1 = bas1 + 3;
			}
			matrix[(bas - 1) % n][(bas1 - 2) % n] == a;
		}
		
		if(matrix[(bas + 1) % n][(bas1 + 1) %n] == 0)
		{
			bas1++;
			bas++;
		}
		else
		{
			bas1--;
		}
		a++;
	}
	
	ofstream file(filename);
	for(int i = 0; i < n; i++)
	{
		for(int k = 0; k < n; k++)
		{
			file << setw(5) << matrix[i][k];
		}
		file << endl;
	}
	file << endl;

	int toplam = 0;	
	for(int i = 0; i < n; i++)
	{
		toplam = toplam + matrix[1][i];
	}
	file << "Sum of Rows: " << toplam << endl << endl;
	file.close();
}

int main()
{
    while(1)
	{
        cout<<"Give me a number for magic squares : ";
        int n;
        cin >> n;  
        if(n % 2 == 0)
		{
            if(n % 4 == 0)
                ccmagic(n, "res.txt");
            else
                tcmagic(n, "res.txt");
        }
        else
            tmagic(n, "res.txt");
    }	
}