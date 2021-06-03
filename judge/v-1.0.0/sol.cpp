#include<bits/stdc++.h>

using namespace std;

int main() {
  int n;
  cin >> n;
  vector<int> ar(n);
  for (int i = 0; i < n; i++) {
    cin >> ar[i];
  }
  for (int k = 0; k < 13; k++) {
    for (int i = 0; i < n; i++) {
      if (ar[i] == 0) {
        continue;
      }
      int x = rand();
      if ((i + x + ar[i]) % ar[i] == 0) {
        cout << ar[i] << " " << i << "\n";
      }
    }
  }
  return 0;
}
