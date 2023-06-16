#include <iostream>
#include <vector>
using namespace std;
string str;
int n;
void permut_lex(int pos, vector<int>& p, vector<bool>& used) {
    if (pos == n) {
        for (int i = 0; i < n; i++) {
            cout << str[p[i]];
        }
        cout << endl;
    }
    for (int i = 0; i < n; i++) {
        if (!used[i]) {
            used[i] = true;
            p[pos] = i;

            permut_lex(pos + 1, p, used);

            p[pos] = 0;
            used[i] = false;
        }
    }
}

void permut_antylex(int pos, vector<int>& p, vector<bool>& used) {
    if (pos == -1) {
        for (int i = n - 1; i >= 0; i--) {
            cout << str[p[i]];
        }
        cout << endl;
    }
    for (int i = n - 1; i >= 0; i--) {
        if (!used[i]) {
            used[i] = true;
            p[pos] = i;

            permut_antylex(pos - 1, p, used);

            p[pos] = 0;
            used[i] = false;
        }
    }
}

int main() {
    vector<int> p;
    vector<bool> used;
    cin >> str;
    n = str.size();
    p.resize(n);
    used.resize(n);
    permut_lex(0, p, used);
    cout << endl;
    permut_antylex(n - 1, p, used);
    return 0;
}