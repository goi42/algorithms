#ifndef LBJPSIPPI_FCH_H 
#define LBJPSIPPI_FCH_H 1

// Include files
#include <TString.h>
#include <TTree.h>
#include <TVector.h>
#include <TFile.h>
#include "branch.h"
#include "cut.h"


/** @class fch fch.h LbJpsipPi/fch.h
 *  
 *
 *  @author Michael Wilkinson
 *  @date   2016-01-14
 */
class fch {//abstract base class for file and chain classes
public: 
  /// Standard constructor
  fch(){};
  //  virtual ~fch( ){delete self;} ///< Destructor
  TString name;//nickname for the file or chain
  void set_name(TString);
  map<TString,TString> quality;//handy for comparing files, e.g., quality["year"]="2015"
  void set_map(map<TString,TString>);
  vector<TTree*> t;
  vector<TString> tname;
  vector<branch> b;
  void add_branch(TString);
  void add_branch(TString,TString);
  void add_branch(TString,int,double,double);
  void add_branch(TString,TString,int,double,double);
  vector<cut> c;//cuts to be applied to the file
  void add_cut(TCut);
  void add_cut(TCut,TString);
  int GetNtrees();
  bool check_tsize_1();
  virtual TObjArray * GetListOfBranches()=0;
  virtual int GetNbranches()=0;
  virtual double GetMaximum(TString)=0;
  virtual double GetMinimum(TString)=0;
  virtual void Draw(TString,TCut,TString)=0;

protected:
  bool can_Draw();

private:

};
void fch::set_name(TString nm) {
  name=nm;
}
void fch::set_map(map<TString,TString> mp){
  quality = mp;
}
void fch::add_branch(TString br){
  b.push_back(branch(br));
}
void fch::add_branch(TString br,TString brname){
  b.push_back(branch(br,brname));//self and name
}
void fch::add_branch(TString br,int nbins,double lobin,double hibin){
  b.push_back(branch(br,nbins,lobin,hibin));
}
void fch::add_branch(TString br,TString brname,int nbins,double lobin,double hibin){
  b.push_back(branch(br,brname,nbins,lobin,hibin));//self and name
}
void fch::add_cut(TCut temp){
  c.push_back(cut(temp));
}
void fch::add_cut(TCut temp,TString tname){
  c.push_back(cut(temp,tname));
}
int fch::GetNtrees(){
  if(t.size()!=tname.size()){
    cout<<"there are "<<t.size()<<" trees but "<<tname.size()<<" tree names. How did this happen?"<<endl;
    exit(EXIT_FAILURE);
  }
  return t.size();
}
bool fch::check_tsize_1(){
  if(GetNtrees()==1)
    return 1;
  else{
    cout<<"Tree vector contains "<<GetNtrees()<<" trees."<<endl;
    return 0;
  }
}
bool fch::can_Draw(){
  if(check_tsize_1())
    return 1;
  else{
    cout<<"fch::Draw is only available for objects with just one associated tree."<<endl;
    exit(EXIT_FAILURE);
  }
}
#endif // LBJPSIPPI_FCH_H
