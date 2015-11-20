#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooHistPdf.h"
#include <TH1.h>
#include <TString.h>
#include "RooRealVar.h"
#include <RooDataHist.h>
using namespace RooFit;

RooHistPdf makeroohistpdf(RooDataHist *h, RooRealVar *x){
  TString htitle = h->GetTitle();
  TString histpdftitle = htitle + " PDF";
  RooHistPdf histpdf("histpdf",histpdftitle,*x,*h);
  return histpdf;
}
