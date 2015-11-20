//this code taken from an answer to
//http://stackoverflow.com/questions/1700079/howto-create-combinations-of-several-vectors-without-hardcoding-loops-in-c
//posted by interjay 2009/11/09.
//It is a recursive function to print combinations of elements in a vector of vectors without hardcoding loops.
#include <vector>
#include <TString.h>
//call with printAll(allVecs, 0, "");
void printAll(const vector<vector<TString> > &allVecs, size_t vecIndex, TString strSoFar)
{ 
  if (vecIndex >= allVecs.size())
  {
    
    cout << strSoFar << endl;
    
    return;
    
  }
  
  for (size_t i=0; i<allVecs[vecIndex].size(); i++)
    printAll(allVecs, vecIndex+1, strSoFar+allVecs[vecIndex][i]);
  
}
