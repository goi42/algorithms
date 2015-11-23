// Include files                                                                                                      
#include <vector>
#include <TLegend.h>
#include <TTree.h>
#include "TROOT.h"
#include "TRint.h"
#include <TFile.h>
#include <THStack.h>
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include <iomanip>
#include <fstream>
#include "TVector3.h"
#include "TPaveStats.h"
#include <math.h>
#include <TString.h>

// local                                                                                                              
#include "storeAll.C"
#include "makeroohistpdf.C"

void dofits.C(){
  gROOT->SetBatch(kTRUE);
  cout<<endl<<"This program takes an input file and performs a set of fits to it."<<endl;
  
  //open file and get histogram
  TFile *f = new TFile("./histos.root","READ");
  TH1F *h = (TH1F*)f->Get("cutmassLb7");

  //make Roo objects
  double mass0 = 5619.5;
  RooRealVar *mass = new RooRealVar("mass","m(#Lambda_{b})",mass0,"MeV");
  RooDataHist *data = new RooDataHist("data",h->GetTitle(),RooArgList(*mass),h);

  //construct Pdf model
  int nObj = 4; //number of things being fit, e.g., Sigma0, Lambda0, Lambda*, and background
  int nSig = 3; //number of fit things that are signal
  int nBkg = nObj-nSig; //number of fit things that are background
  vector<TString> ObjNames(nObj);
  ObjNames[0] = "#Lambda^{0}";
  ObjNames[1] = "#Sigma^{0}";
  ObjNames[2] = "#Lambda*";
  ObjNames[3] = "bkg";
  vector<int> nObjShapes(nObj); //holds the number of pdfs to be added to make up a given signal
  vector< vector<
  for(int iobj =0; iobj<nObj; iobj++){
    
  }
}
