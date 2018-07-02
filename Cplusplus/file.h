#ifndef LBJPSIPPI_FILE_H 
#define LBJPSIPPI_FILE_H 1

// Include files
#include <TString.h>
#include <TTree.h>
#include <TVector.h>
#include <TFile.h>
#include "branch.h"
#include "cut.h"
#include "fch.h"


/** @class file file.h LbJpsipPi/file.h
 *  
 *
 *  @author Michael Wilkinson
 *  @date   2016-01-14
 */
class file : public fch {
public:
  /// Standard constructor
  file(TString);
  file(TString,TString);
  file(TString,TString,TString);
  file(TString,TString,map<TString,TString>);
  file(TString,TString,map<TString,TString>,TString);
  file(TString,TString,TString,map<TString,TString>);
  //  virtual ~file( ){delete self;} ///< Destructor
  TFile* self;//the file
  TString location;//the path to it, e.g., "/afs/.../file.root"
  void add_tree(TString);
  TObjArray * GetListOfBranches();
  int GetNbranches();
  double GetMaximum(TString);
  double GetMinimum(TString);
  void Draw(TString,TCut,TString);

protected:

private:

};
file::file(TString loc){
  self = TFile::Open(loc);
  if(self==NULL) exit(EXIT_FAILURE);
  location = loc;
}
file::file(TString loc,TString nm) : file(loc){
  fch::set_name(nm);
}
file::file(TString loc,TString nm,TString tr) : file(loc,nm) {
  add_tree(tr);
}
file::file(TString loc,TString nm,map<TString,TString> mp) : file(loc,nm){
  fch::set_map(mp);
}
file::file(TString loc,TString nm,map<TString,TString> mp,TString tr) : file(loc,nm,mp){
  add_tree(tr);
}
file::file(TString loc,TString nm,TString tr,map<TString,TString> mp) : file(loc,nm,mp,tr){
}
void file::add_tree(TString trname){
  TTree * temptree;
  self->GetObject(trname,temptree);
  t.push_back(temptree);
  tname.push_back(trname);
}
TObjArray * file::GetListOfBranches(){
  if(!check_tsize_1()){
    cout<<"file::GetListOfBranches() is only available for objects with only one tree."<<endl;
    exit(EXIT_FAILURE);
  }
  return t[0]->GetListOfBranches();
}
int file::GetNbranches(){
  if(!check_tsize_1()){
    cout<<"file::GetNbranches() is only available for objects with only one tree."<<endl;
    exit(EXIT_FAILURE);
  }
  return t[0]->GetNbranches();
}
double file::GetMaximum(TString bnm){
  if(!check_tsize_1()){
    cout<<"file::GetMaximum(<branch>) is only available for objects with only one tree."<<endl;
    exit(EXIT_FAILURE);
  }
  return t[0]->GetMaximum(bnm);
}
double file::GetMinimum(TString bnm){
  if(!check_tsize_1()){
    cout<<"file::GetMinimum(<branch>) is only available for objects with only one tree."<<endl;
    exit(EXIT_FAILURE);
  }
  return t[0]->GetMinimum(bnm);
}
void file::Draw(TString varexp,TCut acut="",TString opt=""){
  
  if(can_Draw())
    t[0]->Draw(varexp,acut,opt);
}
#endif // LBJPSIPPI_FILE_H
