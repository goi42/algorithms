#ifndef LBJPSIPPI_CHAIN_H 
#define LBJPSIPPI_CHAIN_H 1

// Include files
#include <TString.h>
#include <TTree.h>
#include <TVector.h>
#include <TChain.h>
#include "branch.h"
#include "file.h"

/** @class file chain.h LbJpsipPi/file.h
 *  
 *
 *  @author Michael Wilkinson
 *  @date   2016-08-26
 */
class chain {
public: 
  /// Standard constructor
  /* chain(file); */
  chain(TString,vector<file>);
  chain(TString,vector<file>,TString);
  chain(TString,vector<file>,TString,map<TString,TString>);
  /* chain(TString); */
  /* chain(TString,TString); */
  /* chain(TString,TString,map<TString,TString>); */
  /* chain(vector<TString>); */
  /* chain(vector<TString>,vector<TString>); */
  /* chain(vector<TString>,vector<TString>,map<TString,TString>); */
  //  virtual ~chain( ){delete self;} ///< Destructor
  TChain* self;//the chain
  /* vector<TString> locations;//the paths to the chained files, e.g., "/afs/.../file1.root" */
  TString name;//nickname for the chain
  map<TString,TString> quality;//handy for comparing chains, e.g., quality["year"]="2015"
  TString tname;//name of tree--should include any intervening folders and be common to all files in the chain
  vector<branch> b;
  void add_branch(TString);
  void add_branch(TString,TString);
  void add_files(vector<file>,bool);
  void Draw(TString);
  void Draw(TString,TCut,TString);
  void Draw(TString,TString,TString);
  
protected:

private:

};
chain::chain(TString tr, vector<file> lfiles){
  tname = tr;
  self = new TChain(tr,"");
  for(unsigned int i=0; i<lfiles.size(); i++){
    self->Add(lfiles[i].location);
    if(self==NULL) exit(EXIT_FAILURE);
  }
}
chain::chain(TString tr, vector<file> lfiles, TString nm){
  chain tempchain(tr, lfiles);
  (*this)=tempchain;
  name = nm;
}
chain::chain(TString tr, vector<file> lfiles, TString nm,map<TString,TString> mp){
  chain tempchain(tr, lfiles, nm);
  (*this)=tempchain;
  quality = mp;
}void chain::add_branch(TString br){
  branch tempbranch(br);
  b.push_back(tempbranch);
}
void chain::add_branch(TString br,TString brname){
  branch tempbranch(br,brname);//self and name
  b.push_back(tempbranch);
}
void chain::add_files(vector<file> lfiles,bool del=0){
  if(del){
    delete self;
    self = new TChain(tname,"");
  }
  for(unsigned int i=0; i<lfiles.size(); i++){
    self->Add(lfiles[i].location);
    if(self==NULL) exit(EXIT_FAILURE);
  }
}  
void chain::Draw(TString opt=""){
  self->Draw(opt);
}
void chain::Draw(TString varexp,TCut acut,TString opt=""){
  self->Draw(varexp,acut,opt);
}
void chain::Draw(TString varexp,TString acut,TString opt=""){
  TCut tempcut = (TCut)acut;
  self->Draw(varexp,tempcut,opt);
}

#endif // LBJPSIPPI_CHAIN_H
