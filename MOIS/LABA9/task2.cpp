#include <iostream>
using namespace std;

int main(int argc, char** argv) 
{
    int n = atoi(argv[1]);
    char board[n][n];
    
    for (int row = 0; row < n; row++)
        for (int col = 0; col < n; col++)
            if ((row + col) % 2 == 0)
                board[row][col] = 'W';
            else board[row][col] = 'B';

    int i = 0;
    int move = 0;
    int num1 = 0, num2 = 0, num3 = 0, num4 = 0;
    bool check1, check2, check3, check4 = false;
    char Black_checker, White_checker;
    while(1)
    {
        if (num1 + num2 + num3 + num4 == (n - 1) * 4)
            break;
        if(num3 + num4 == (n - 1) * 2)
        {
            num3 = 0;
            num4 = 0;
            if (num1 < (n - 1))
                num1 += 1;
            else
            {
                num2 += 1;
                num1 = 0;
            }
        }
        if (num3 <= (n-1)) 
            if (num3 == 0 & num4 == 0)
            {
                i += 1;
                if (i == 2)
                {
                    num3 += 1;
                    i = 0;
                }
            }
            else if (num3 < (n-1))
                num3 += 1;
            else 
            {
                num4 += 1;
                num3 = 0;
            }

        Black_checker = board[num1][num2];
        White_checker = board[num3][num4];
        if (Black_checker != 'B' & White_checker != 'B' &  (num1 != num3 || num2 != num4))
        {
            if((num1 + 1 != num3) || (num2 + 1 != num4))
                check1 = true;
            if((num1 + 1 != num3) || (num2 - 1 != num4))
                check2 = true;
            if((num1 - 1 != num3) || (num2 + 1 != num4))
                check3 = true;
            if((num1 - 1 != num3) || (num2 - 1 != num4))
                check4 = true;
            if(check1 == true & check2 == true & check3 == true & check4 == true)
                move += 1;

            check1 = false;
            check2 = false;
            check3 = false;
            check4 = false;
        };
    }
    cout << "Moves: " << move << endl;
    return 0;
}