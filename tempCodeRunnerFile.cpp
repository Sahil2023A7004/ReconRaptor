#include<bits/stdc++.h>
using namespace std;
int main()
{
    int n;
    cout<<"enter size of array\n";
    cin>>n;
    int arr[n];
    cout<<"enter arry elements\n";
    for(int i=0;i<n;i++)
    {
        cin>>arr[i];
    }
     int x;
    cout<<"enter element to search\n";
    cin>>x;
    bool flag = false;
    int index = -1;
    for(int i=0;i<n;i++)
    {
       if(arr[i]==x){
       flag = true;
       index = i;
       break;
       }
    }
    if(flag == true)
    {
        cout<<x<<" is the element found at index "<<index;
    }
    else 
    {
        cout<<"element not found\n";
    }
     
}