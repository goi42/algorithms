#ifndef BRANCH_H 
#define BRANCH_H 1

// Include files
#include <TFile.h>
#include <TString.h>
#include <vector>
#include "cut.h"

/** @class branch branch.h LbJpsipPi/branch.h
 *  
 *
 *  @author Michael Wilkinson
 *  @date   2016-01-14
 */
class branch {
public: 
  /// Standard constructor
  branch(TString);
  branch(TString,TString);
  branch(TString,TString,int,int,int);
  branch(TString,TString,int,int,int,TString,TString);
  TString self;//what the branch is called in the tree
  TString name;//nickname--usually what you want to appear on a plot
  TString xlabel;
  TString ylabel;
  int nBins;
  int loBin;
  int hiBin;
  void binning(int,int,int);
  vector<cut> c;//cuts to be applied to the branch
  void add_cut(TCut);
  void add_cut(TCut,TString);
  
protected:

private:

};
branch::branch (TString temp) {
  self = temp;
}
branch::branch(TString temp1, TString temp2){
  self = temp1;
  name = temp2;
}
branch::branch(TString tself, TString tname, int nb, int lb, int hb){
  self = tself;
  name = tname;
  nBins = nb;
  loBin = lb;
  hiBin = hb;
}
branch::branch(TString tself, TString tname, int nb, int lb, int hb, TString x, TString y){
  self = tself;
  name = tname;
  nBins = nb;
  loBin = lb;
  hiBin = hb;
  xlabel = x;
  ylabel = y;
}
void branch::binning(int b1, int b2, int b3){
  nBins = b1;
  loBin = b2;
  hiBin = b3;
}
void branch::add_cut(TCut temp){
  cut tempcut(temp);
  c.push_back(tempcut);
}
void branch::add_cut(TCut temp,TString tname){
  cut tempcut(temp,tname);
  c.push_back(tempcut);
}
#endif // BRANCH_H
