#include "testlib.h"
#include <iostream>

using namespace std;

int main(int argc, char* argv[])
{
    registerGen(argc, argv);
    int n = atoi(argv[1]);
    int m = atoi(argv[2]);
    for (int i = 0; i < n; ++i) {
        if (i) cout << " ";
        cout << rnd.next(1, m);
    }
    cout << endl;

    return 0;
}
