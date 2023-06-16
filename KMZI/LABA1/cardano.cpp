#include "libs.hh"

void rotate_matrix(std::vector<std::vector<int>>& matrix, std::vector<std::vector<int>>& rotatedMatrix, int angle) 
{
    int n = matrix.size();

    if (angle == 0 || angle % 360 == 0) 
    {
        rotatedMatrix = matrix;
        return;
    }

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            rotatedMatrix[i][j] = 0;
    
    if (angle == 90)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                rotatedMatrix[j][n-i-1] = matrix[i][j];
    else if (angle == 180)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                rotatedMatrix[n-i-1][n-j-1] = matrix[i][j];
    else if (angle == 270)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                rotatedMatrix[n-j-1][i] = matrix[i][j];
}

std::vector<std::vector<int>> make_grid(int n)
{
    std::vector<int> indecis(n * n);
    for (int inx = 0; inx < n * n; inx++) indecis[inx] = inx;
    int index, i, j;

    std::vector<int> grid_indecis;
    while(!indecis.empty())
    {
        index = (indecis.size() - indecis.size() % n) / n;
        i = indecis[index] / n, j = indecis[index] % n;
        int els[] = {
            i * n + j, j * n + (n - i - 1), 
            (n - i - 1) * n + (n - j - 1), (n - j - 1) * n + i
        };
        grid_indecis.push_back(indecis[index]);
        for (auto el : els) indecis.erase(std::remove(indecis.begin(), indecis.end(), el), indecis.end());
    }
    std::vector<std::vector<int>> grid_matrix(n, std::vector<int>(n, 0));
    for(int g : grid_indecis) grid_matrix[g / n][g % n] = 1;

    return grid_matrix;
}

std::string encode_cardano(std::vector<std::vector<int>> &grid, std::string str)
{
    std::vector<std::vector<int>> buf_grid = grid;
    int n = grid.size();
    std::vector<std::vector<std::string>> encode_matrix(n, std::vector<std::string>(n));

    while (str.length() < n * n) str.append(" ");

    int k = 0;
    for (int side = 0; side <= 270; side += 90)
    {
        rotate_matrix(grid, buf_grid, side);
        for(int i = 0; i < n; i++)
            for(int j = 0; j < n; j++)
                if(buf_grid[i][j] == 1)
                    encode_matrix[i][j] = str[k++];
    }

    std::string result;
    for(int i = 0; i < n; i++)
        for(int j = 0; j < n; j++)
            result += encode_matrix[i][j];

    return result;
}

std::string decode_cardano(std::vector<std::vector<int>> &grid, std::string str)
{
    std::vector<std::vector<int>> buf_grid = grid;
    int n = grid.size();
    std::vector<std::vector<std::string>> encode_matrix(n, std::vector<std::string>(n));
    int k = 0;
    for(int i = 0; i < n; i++)
        for(int j = 0; j < n; j++)
            encode_matrix[i][j] = str[k++];

    std::string result;
    for (int side = 0; side <= 270; side += 90)
    {
        rotate_matrix(grid, buf_grid, side);
        for(int i = 0; i < n; i++)
            for(int j = 0; j < n; j++)
                if(buf_grid[i][j] == 1)
                    result += encode_matrix[i][j];
    }

    return result;
}

// int main()
// {
//     std::string to_encode = "hello, world!";
//     int n = ceil(sqrt(to_encode.length()));
//     std::vector<std::vector<int>> grid = make_grid(n);
//     std::string to_decode = encode_cardano(grid, to_encode);
//     std::cout << to_decode << std::endl;

//     std::string from_decode = decode_cardano(grid, to_decode);
//     std::cout << from_decode << std::endl;
// }