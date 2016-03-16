#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#ifndef __makeroohistpdf_C_INCLUDED__
#define __makeroohistpdf_C_INCLUDED__
#include "RooHistPdf.h"
#include <TH1.h>
#include <TString.h>
#include "RooRealVar.h"
#include <RooDataHist.h>
using namespace RooFit;

RooHistPdf makeroohistpdf(RooDataHist *h, RooRealVar *x, TString hpdfname="jibberish", TString hpdftitle="jibberish"){
  if(hpdfname=="jibberish") {
    TString temp = h->GetName();
    hpdfname = temp + " PDF";
  }
  if(hpdftitle=="jibberish"){
    TString temp = h->GetTitle();
    hpdftitle = temp + " PDF";
  }
  RooHistPdf histpdf(hpdfname,hpdftitle,*x,*h);
  return histpdf;
}
#endif
