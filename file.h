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
  vector<TString> tname;
  void add_tree(TString);
  vector<branch> b;
  void add_branch(TString);
  void add_branch(TString,TString);
  
protected:

private:

};
file::file(TString temp){
  self = TFile::Open(temp);
  if(self==NULL) exit(EXIT_FAILURE);
  location = temp;
}
file::file(TString temp1,TString temp2){
  self = TFile::Open(temp1);
  if(self==NULL) exit(EXIT_FAILURE);
  location = temp1;
  name = temp2;
}
file::file(TString temp1,TString temp2,map<TString,TString> temp3){
  self = TFile::Open(temp1);
  if(self==NULL) exit(EXIT_FAILURE);
  location = temp1;
  name = temp2;
  quality = temp3;
}
void file::add_tree(TString temp){
  TTree * temptree;
  self->GetObject(temp,temptree);
  t.push_back(temptree);
  tname.push_back(temp);
}
void file::add_branch(TString temp){
  branch tempbranch(temp);
  b.push_back(tempbranch);
}
void file::add_branch(TString temp1,TString temp2){
  branch tempbranch(temp1,temp2);//self and name
  b.push_back(tempbranch);
}


#endif // LBJPSIPPI_FILE_H
