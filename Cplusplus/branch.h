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
  branch(TString,int,double,double);
  branch(TString,int,double,double,TString);
  branch(TString,int,double,double,TString,TString);
  TString self;//what the branch is called in the tree
  TString name;//nickname--usually what you want to appear on a plot
  TString xlabel;
  TString ylabel;
  int nBins;
  double loBin;
  double hiBin;
  bool can_extend;//do you want Draw to change the bin range?
  bool set_log_Y;//do you want a log scale?
  void binning(int,double,double);
  void binning(int,double,double,bool);
  vector<cut> c;//cuts to be applied to the branch
  void add_cut(TCut);
  void add_cut(TCut,TString);
  
protected:

private:

};
branch::branch (TString tself) {
  self = tself;
  name = tself;
  binning(0,0,0);
  set_log_Y=0;
  can_extend=0;
}
branch::branch(TString tself, TString tname) : branch(tself){
  name = tname;
}
branch::branch(TString tself, TString tname, int nb, double lb, double hb) : branch(tself,tname){
  binning(nb,lb,hb);
}
branch::branch(TString tself, TString tname, int nb, double lb, double hb, TString x, TString y) : branch(tself,tname,nb,lb,hb){
  xlabel = x;
  ylabel = y;
}
branch::branch(TString tself, int nb, double lb, double hb) : branch(tself){
  binning(nb,lb,hb);
}
branch::branch(TString tself, int nb, double lb, double hb, TString x, TString y) : branch(tself,nb,lb,hb){
  xlabel = x;
  ylabel = y;
}
void branch::binning(int nb, double lb, double hb){
  nBins = nb;
  loBin = lb;
  hiBin = hb;
  if(nBins < 0 || loBin > hiBin){
    if(nBins < 0)
      cout<<"branch "<<name<<" has nBins = "<<nBins<<". nBins must be >= 0!"<<endl;
    if(loBin > hiBin)
      cout<<"branch "<<name<<" has loBin = "<<loBin<<" and hiBin = "<<hiBin<<". loBin must be <= hiBin!"<<endl;
    exit(EXIT_FAILURE);
  }    
}
void branch::binning(int nb, double lb, double hb, bool ce){
  binning(nb,lb,hb);
  can_extend = ce;
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
