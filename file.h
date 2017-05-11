#ifndef LBJPSIPPI_FILE_H 
#define LBJPSIPPI_FILE_H 1

// Include files
#include <TString.h>
#include <TTree.h>
#include <TVector.h>
#include <TFile.h>
#include "branch.h"
#include "cut.h"


/** @class file file.h LbJpsipPi/file.h
 *  
 *
 *  @author Michael Wilkinson
 *  @date   2016-01-14
 */
class file {
public: 
  /// Standard constructor
  file(TString);
  file(TString,TString);
  file(TString,TString,map<TString,TString>);
  //  virtual ~file( ){delete self;} ///< Destructor
  TFile* self;//the file
  TString location;//the path to it, e.g., "/afs/.../file.root"
  TString name;//nickname for the file
  map<TString,TString> quality;//handy for comparing files, e.g., quality["year"]="2015"
  vector<TTree*> t;
  vector<TString> tname;
  void add_tree(TString);
  vector<branch> b;
  void add_branch(TString);
  void add_branch(TString,TString);
  void add_branch(TString,int,double,double);
  void add_branch(TString,TString,int,double,double);
  vector<cut> c;//cuts to be applied to the file
  void add_cut(TCut);
  void add_cut(TCut,TString);

protected:

private:

};
file::file(TString loc){
  self = TFile::Open(loc);
  if(self==NULL) exit(EXIT_FAILURE);
  location = loc;
}
file::file(TString loc,TString nm) : file(loc){
  name = nm;
}
file::file(TString loc,TString nm,map<TString,TString> mp) : file(loc,nm){
  quality = mp;
}
void file::add_tree(TString trname){
  TTree * temptree;
  self->GetObject(trname,temptree);
  t.push_back(temptree);
  tname.push_back(trname);
}
void file::add_branch(TString br){
  b.push_back(branch(br));
}
void file::add_branch(TString br,TString brname){
  b.push_back(branch(br,brname));//self and name
}
void file::add_branch(TString br,int nbins,double lobin,double hibin){
  b.push_back(branch(br,nbins,lobin,hibin));
}
void file::add_branch(TString br,TString brname,int nbins,double lobin,double hibin){
  b.push_back(branch(br,brname,nbins,lobin,hibin));//self and name
}
void file::add_cut(TCut temp){
  c.push_back(cut(temp));
}
void file::add_cut(TCut temp,TString tname){
  c.push_back(cut(temp,tname));
}
#endif // LBJPSIPPI_FILE_H
