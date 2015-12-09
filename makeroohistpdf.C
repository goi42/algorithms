#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooHistPdf.h"
#include <TH1.h>
#include <TString.h>
#include "RooRealVar.h"
#include <RooDataHist.h>
using namespace RooFit;

RooHistPdf makeroohistpdf(RooDataHist *h, RooRealVar *x,\
                          TString hpdfname="jibberish", TString hpdftitle="jibberish"){
  if(hpdfname=="jibberish") hpdfname = h->GetName() + " PDF";
  if(hpdftitle=="jibberish") hpdftitle = h->GetTitle() + " PDF";
  RooHistPdf histpdf(hpdfname,hpdftitle,*x,*h);
  return histpdf;
}
