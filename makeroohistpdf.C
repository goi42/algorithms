#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooHistPdf.h"
#include <TH1.h>
#include <TString.h>
#include "RooRealVar.h"
#include <RooDataHist.h>
using namespace RooFit;

RooHistPdf makeroohistpdf(TH1F *h, RooRealVar *x){
  RooDataHist* hist = new RooDataHist("hist","hist",RooArgList(*x),h);
  TString htitle = h->GetTitle();
  TString histpdftitle = htitle + " PDF";
  RooHistPdf histpdf("histpdf",histpdftitle,*x,*hist);
  return histpdf;
}
