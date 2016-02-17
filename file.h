#ifndef LBJPSIPPI_FILE_H 
#define LBJPSIPPI_FILE_H 1

// Include files
#include <TString.h>
#include <TTree.h>
#include <TVector.h>
#include <TFile.h>
#include "branch.h"


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
  void add_tree(TString);
  vector<branch> b;
  void add_branch(TString);
  void add_branch(TString,TString);
  void operator = (TFile*);
  
protected:

private:

};
file::file(TString temp){
  self = TFile::Open(temp);
  location = temp;
}
file::file(TString temp1,TString temp2){
  self = TFile::Open(temp1);
  location = temp1;
  name = temp2;
}
file::file(TString temp1,TString temp2,map<TString,TString> temp3){
  self = TFile::Open(temp1);
  location = temp1;
  name = temp2;
  quality = temp3;
}
void file::add_tree(TString temp){
  TTree * temptree;
  self->GetObject(temp,temptree);
  t.push_back(temptree);
}
void file::add_branch(TString temp){
  branch tempbranch(temp);
  b.push_back(tempbranch);
}
void file::add_branch(TString temp1,TString temp2){
  branch tempbranch(temp1,temp2);//self and name
  b.push_back(tempbranch);
}
void file::operator= (TFile* param){
  self = param;
}


#endif // LBJPSIPPI_FILE_H
