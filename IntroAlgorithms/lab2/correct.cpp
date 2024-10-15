#include<bits/stdc++.h>

using namespace std;
long long A[1000000];
long long B[1000000];
long long tp[1000000];
long long temp[1000000];
long long M=998244353;
map<long long,long long>bigger;
map<long long,long long>smaller;
map<long long,long long>turn;

long long merge(long long l,long long m,long long r){
long long i,j,k,ans=0,altt=0;
for(i=l,j=m+1,k=l;k<=r;k++){
if(i>m){
temp[k]=A[j];
j++;
}else if(j>r){
temp[k]=A[i];
i++;
}else if(A[i]<=A[j]){
temp[k]=A[i];
i++;
}else{
temp[k]=A[j];
ans+=(m+1)-i;
j++;
}
}
for(k=l;k<=r;k++){
A[k]=temp[k];
}
return ans%M;
}
long long invcnt(long long l,long long r){
long long ans=0;
if(l<r){
int m=(l+r)/2;
ans+=invcnt(l,m);
ans+=invcnt(m+1,r);
ans+=merge(l,m,r);
}
return ans%M;
}
int main(){
    long long a,b,b1,b2;
    long long ans=0,ansr=0,altt=0,s=0,last=0;
    cin>>a>>b;
b1=b;
b2=b;
    b1=(b1/a)%M;
    for(int i=0;i<a;i++){
    cin>>A[i];
    tp[i]=A[i];
    B[i]=A[i];
}
sort(tp,tp+a);
for(int i=0;i<a;i++){
bigger[tp[i]]=a-1-i;
}
for(int i=a-1;i>=0;i--){
smaller[tp[i]]=i;
}
for(int i=0;i<a;i++){
turn[A[i]]=bigger[A[i]]-smaller[A[i]];
s=(s+bigger[A[i]])%M;
}
ans=invcnt(0,a-1)%M;
long long c=(b2)%a,ans1=ans,ans2=ans;
for(int i=0;i<c-1;i++){
ansr=(ansr+ans1+turn[B[i]])%M;
ans1=(ans1+turn[B[i]]);
}
for(int i=0;i<a;i++){
altt=(ans2+altt+turn[B[i]])%M;
ans2=(ans2+turn[B[i]]);
if(i==a-1){
last=ans2;
}
}
long long bp;
b2=(b2-1)%M;
bp=(b2*(b2+1))/2;
bp%=M;
ans=(ans%M+ansr%M)%M;
ans=(ans%M+(((altt%M)*(b1%M))%M))%M;
ans=(ans%M+(((s%M)*bp%M)%M))%M;
if(b%a==0){
ans=(ans-last+M)%M;
}
cout<<ans%M<<endl;
    return 0;
}