#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>
using namespace std;
struct Solver {
 int l,r; array<int,8>a; vector<pair<int,int>> spans;
 void gen(int left,int start,int s){spans.emplace_back(s-left*l,s+left*r); if(left)for(int j=start;j<8;j++) gen(left-1,j,s+a[j]);}
 int score(){spans.clear();gen(4,0,0);sort(spans.begin(),spans.end());int lo=-l*(l+1)/2,hi=r*(r+1)/2;for(int v:a) if(v<0)lo+=v;else hi+=v;int end=lo-1,miss=0;for(auto [x,y]:spans){x=max(x,lo);y=min(y,hi);if(y<x||y<=end)continue;if(x>end+1)miss+=x-end-1;end=y;}return miss+max(0,hi-end);}
};
int main(int argc,char**argv){int l=argc>1?atoi(argv[1]):31,r=argc>2?atoi(argv[2]):32;long iterations=argc>3?atol(argv[3]):2000000;mt19937 gen(20261014);Solver s{l,r};array<int,8> seed={-23*l,-7*l,-5*l,-3*l,3*r,5*r,7*r,23*r};int best=1000000;array<int,8> champion;
for(long it=0;it<iterations;){s.a=seed;int old=s.score();for(int k=0;k<20000&&it<iterations;k++,it++){auto prev=s.a;int j=gen()%8;int step=1+gen()%(k<10000?30:5);s.a[j]+=(gen()%2?step:-step);bool ok=true;for(int h=1;h<8;h++)ok &=s.a[h]>s.a[h-1];ok &=s.a[3]<-l && s.a[4]>r;if(!ok){s.a=prev;continue;}int q=s.score();if(q<best){best=q;champion=s.a;cout<<it<<" missing="<<q<<" core="<<-l<<","<<r<<" tails=";for(int v:s.a)cout<<v<<",";cout<<endl;if(!q)return 0;}double temp=3.0*(20000-k)/20000+.03;if(q<=old || generate_canonical<double,32>(gen)<exp((old-q)/temp))old=q;else s.a=prev;}seed=champion; if(gen()%3==0)for(int j=0;j<8;j++)seed[j]+=(int)(gen()%41)-20;sort(seed.begin(),seed.end());}
}
