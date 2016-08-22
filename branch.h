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
  branch(TString,TString,int,double,double);
  branch(TString,TString,int,double,double,TString,TString);
  TString self;//what the branch is called in the tree
  TString name;//nickname--usually what you want to appear on a plot
  TString xlabel;
  TString ylabel;
  int nBins;
  double loBin;
  double hiBin;
  void binning(int,double,double);
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
branch::branch(TString tself, TString tname, int nb, double lb, double hb){
  self = tself;
  name = tname;
  nBins = nb;
  loBin = lb;
  hiBin = hb;
}
branch::branch(TString tself, TString tname, int nb, double lb, double hb, TString x, TString y){
  self = tself;
  name = tname;
  nBins = nb;
  loBin = lb;
  hiBin = hb;
  xlabel = x;
  ylabel = y;
}
void branch::binning(int b1, double b2, double b3){
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
