#ifndef LBJPSIPPI_CHAIN_H 
#define LBJPSIPPI_CHAIN_H 1

// Include files
#include <TString.h>
#include <TTree.h>
#include <TVector.h>
#include <TChain.h>
#include "branch.h"
#include "file.h"
#include "fch.h"

/** @class file chain.h LbJpsipPi/file.h
 *  
 *
 *  @author Michael Wilkinson
 *  @date   2016-08-26
 */
class chain : public fch {
public: 
  /// Standard constructor
  chain(TString);
  chain(TString,TString);
  chain(TString,TString,map<TString,TString>);
  chain(TString,vector<file>);
  chain(TString,vector<file>,TString);
  chain(TString,vector<file>,TString,map<TString,TString>);
  //  virtual ~chain( ){delete self;} ///< Destructor
  TChain* self;//the chain
  /* vector<TString> locations;//the paths to the chained files, e.g., "/afs/.../file1.root" */
  void add_tree(TString,bool);
  void add_file(TString);
  void add_files(vector<file>,bool);
  TObjArray * GetListOfBranches();
  int GetNbranches();
  double GetMaximum(TString);
  double GetMinimum(TString);
  void Draw(TString,TCut,TString);

protected:

private:

};
chain::chain(TString tr){
  tname.push_back(tr);
  self = new TChain(tr,"");
  t.push_back(self->GetTree());
}
chain::chain(TString tr ,TString nm) : chain(tr){
  fch::set_name(nm);
}
chain::chain(TString tr,TString nm,map<TString,TString> mp) : chain(tr,nm) {
  fch::set_map(mp);
}
chain::chain(TString tr, vector<file> lfiles) : chain(tr){
  for(unsigned int i=0; i<lfiles.size(); i++){
    self->Add(lfiles[i].location);
    if(self==NULL) exit(EXIT_FAILURE);
  }
}
chain::chain(TString tr, vector<file> lfiles, TString nm) : chain(tr,lfiles){
  fch::set_name(nm);
}
chain::chain(TString tr, vector<file> lfiles, TString nm,map<TString,TString> mp) : chain(tr,lfiles,nm){
  fch::set_map(mp);
}
void chain::add_tree(TString trname,bool rcr=0){
  cout<<"chain::add_tree not yet implemented because it is not clear what it should do."<<endl;
  exit(EXIT_FAILURE);
}
void chain::add_file(TString floc){
  self->Add(floc);
  if(check_tsize_1())
    t[0] = self->GetTree();
  else{
    cout<<"chain::add_file only works if there is only 1 associated tree."<<endl;
    exit(EXIT_FAILURE);
  }
  if(self==NULL) exit(EXIT_FAILURE);
}
void chain::add_files(vector<file> lfiles,bool del=0){
  if(del){
    if(!fch::check_tsize_1()){
      cout<<"chain::add_files(<files>,del=1) requires 1 tree to avoid ambiguity."<<endl;
      exit(EXIT_FAILURE);
    }
    delete self;
    self = new TChain(tname[0],"");
  }
  for(unsigned int i=0; i<lfiles.size(); i++){
    self->Add(lfiles[i].location);
    if(self==NULL) exit(EXIT_FAILURE);
  }
}
TObjArray * chain::GetListOfBranches(){
  return self->GetListOfBranches();
}
int chain::GetNbranches(){
  return self->GetNbranches();
}
double chain::GetMaximum(TString bnm){
  return self->GetMaximum(bnm);
}
double chain::GetMinimum(TString bnm){
  return self->GetMinimum(bnm);
}
void chain::Draw(TString varexp,TCut acut="",TString opt=""){
  if(can_Draw())
    self->Draw(varexp,acut,opt);
}
#endif // LBJPSIPPI_CHAIN_H
