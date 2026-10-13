#include <algorithm>
#include <cmath>
#include <iostream>
#include <random>
#include <vector>
using namespace std;
vector<int>a;vector<pair<int,int>>spans;
void gen(int left,int start,int s){spans.emplace_back(s-left,s+left);if(left)for(int j=start;j<(int)a.size();j++)gen(left-1,j,s+a[j]);}
int eval(const vector<int>&p,int &R){a.clear();for(int x:p){a.push_back(x);a.push_back(-x);}spans.clear();gen(4,0,0);sort(spans.begin(),spans.end());R=0;for(auto[x,y]:spans){if(y<0)continue;if(x>R)break;R=max(R,y);}int sum=0;for(int x:p)sum+=x;return R-sum;}
int main(int argc,char**argv){int t=atoi(argv[1]);long n=atol(argv[2]);mt19937 rng(20261014+t);vector<int>bestp;int best=-10000;for(long it=0;it<n;){vector<int>p={3,5,7,23};while((int)p.size()<t)p.push_back(2+(p.size()-4)*7);sort(p.begin(),p.end());int R,cur=eval(p,R);for(int k=0;k<20000 && it<n;k++,it++){auto prev=p;int j=rng()%t;p[j]+=((rng()%2)?1:-1)*(1+rng()%4);sort(p.begin(),p.end());if(p[0]<2||adjacent_find(p.begin(),p.end())!=p.end()){p=prev;continue;}int q=eval(p,R);if(q>best){best=q;bestp=p;cout<<"it="<<it<<" F="<<q<<" R="<<R<<" coefficients=";for(int x:p)cout<<x<<",";cout<<" predicted_n="<<4*q+2*t-1<<endl;}double temp=2.5*(20000-k)/20000+.05;if(q>=cur||generate_canonical<double,32>(rng)<exp((q-cur)/temp))cur=q;else p=prev;}}}
