#include<bits/stdc++.h>

using namespace std;

const int SUCCESS = 0;
const int FAILURE = 1;
const int ARGV_ERROR = 2; /* Nedd exactly two arguments to compare. */
const int READ_ERROR = 3; /* Can't open required files. */
const int TOKEN_COUNT_ERROR = 4; /* Token count are different */

int main(int args, const char *argv[]) {
  if (args <= 3) {
    return ARGV_ERROR;
  }
  
  ifstream file_lhs = ifstream(argv[1]);
  ifstream file_rhs = ifstream(argv[2]);
  int p = stoi(argv[3]);
  double err = 1;
  for (int i = 0; i < p; i++) {
    err /= 10;
  }
  
  if (!file_lhs.is_open() || !file_rhs.is_open()) {
    file_lhs.close();
    file_rhs.close();
    return READ_ERROR;
  }
  
  double x;
  vector<double> lhs, rhs;
  while (file_lhs >> x) {
    lhs.push_back(x);
  }
  while (file_rhs >> x) {
    rhs.push_back(x);
  }
  file_lhs.close();
  file_rhs.close();
  
  if ((int) lhs.size() != (int) rhs.size()) {
    return TOKEN_COUNT_ERROR;
  }
  
  auto ok = [&] (double a, double b) {
    return fabs(a - b) <= err;
  };
  
  int n = (int) lhs.size();
  for (int i = 0; i < n; i++) {
    if (ok(lhs[i], rhs[i]) == false) {
      return FAILURE;
    }
  }
  return SUCCESS;
}
