//modified from printAll.C to add the combinations to list instead of printing them
#include <vector>
#include <TString.h>

//call with storeAll(allVecs, 0, "",list);
//adds all the combinations of allVecs's elements to list
void storeAll(const vector<vector<TString> > &allVecs, size_t vecIndex, TString strSoFar, vector<TString> &list)
{
  if (vecIndex >= allVecs.size())
  {
    list.push_back(strSoFar);
    return;
  }
  
  for (size_t i=0; i<allVecs[vecIndex].size(); i++)
    storeAll(allVecs, vecIndex+1, strSoFar+allVecs[vecIndex][i]+", ", list);
}

