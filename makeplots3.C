/*
This is a variant on makeplots2.C that does not require the same number of branches and cuts per file and branch.
It does not do the fancy comparisons that makeplots.C and makeplots2.C do, however.
It is good for comparing cuts on a single branch.
It loops over files, then branches, then cuts, assigning branches and cuts in each 
of these loops, and plotting the cuts as they come.
Each branch gets its own canvas.
*/
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
#include <TCut.h>

// local
#include "/afs/cern.ch/user/m/mwilkins/algorithms/storeAll.C"
#include "~/algorithms/branch.h"
#include "~/algorithms/cut.h"
#include "~/algorithms/file.h"

vector<TString> Lbname {"Bs","Lambda_b0","Lambda_b0"};//make sure to have 1 per file
vector<TString> massname {"Bs_LOKI_MASS_JpsiConstr","Lambda_b0_MM","Lambda_b0_MM"};
vector<TString> Jpsi_ {"","_","_"};//make sure to have 1 per file
TCut cLbDIRA(int i,float input=0.9999){//declared here because of weirdness
  TString inputstring = Form("%f",input);
  TString place=Lbname[i]+"_DIRA_OWNPV>"+inputstring;
  TCut output=(TCut)place;
  return output;
}
TCut cgprob(TString input="0.2"){
  TString place="(H1_TRACK_GhostProb<"+input+")&&(H2_TRACK_GhostProb<"+input+")";
  TCut output=(TCut)place;
  return output;
}  
TCut cLPT(float input=1000){
  TString inputstring = Form("%f",input);
  TString place = "R_PT>"+inputstring;
  TCut output=(TCut)place;
  return output;
}

void makeplots3(TString runmode="d", TString drawopt=""){
  gROOT->SetBatch(kTRUE);
  TString placeholder;//this is to avoid adding strings in functions; assign right before use
  TString placeholder2;
  TString placeholder3;
  TString outputlocation="./";
  TString filename="plots.pdf";
  // ofstream myfile;
  // TString trueratiostring="";//holds information to be put at end of myfile
  // myfile.open(outputlocation+"sigbkg.csv");
  // myfile<<"dataset,cuts,number signal,number background"<<endl;
  // float bkgcutofflo = 5100;
  // float bkgcutoffhi = 0;
  // cout<<"using "<<bkgcutofflo<<" and "<<bkgcutoffhi<<" as the boundaries between bkg and sig for ratio calculation"<<endl;
  //create necessary counters, canvases, legends, etc.
  cout<<endl;
  vector<TCanvas*> c;//each canvas holds one stack of histograms
  int ci = 0;//how many canvases have been plotted?
  vector<TLegend*> leg;//one legend per canvas
  vector<THStack*> hs;//one stack per canvas
  vector< vector<TH1F*> > h;
  TCanvas *cf = new TCanvas("cf","combined");//canvas to hold everything

  //assign things to actually be plotted
  map<TString,TString> f1quality {{"filetype","data"},{"decaymode","both"}};
  map<TString,TString> f2quality {{"filetype","MC"},{"decaymode","#Lambda^{0}"}};
  map<TString,TString> f3quality {{"filetype","MC"},{"decaymode","#Sigma^{0}"}};
  file f[]={{"/afs/cern.ch/work/m/mwilkins/Lb2JpsiLtr/data/subLimDVNtuples.root","data",f1quality}, \
            {"/afs/cern.ch/work/m/mwilkins/Lb2JpsiLtr/MC/withKScut/Lb2JpsiLMC.root","#Lambda^{0} MC",f2quality}, \
            {"/afs/cern.ch/work/m/mwilkins/Lb2JpsiLtr/MC/withKScut/Lb2JpsiSMC.root","#Sigma^{0} MC",f3quality}};
  int nFiles = (sizeof(f)/sizeof(f[0]));
  if((unsigned int)nFiles != Lbname.size()){
    cout<<"number of Lbnames must = nFiles"<<endl;
    cout<<"nFiles = "<<nFiles<<" while Lbname.size() = "<<Lbname.size()<<endl;
    exit(EXIT_FAILURE);
  }else if((unsigned int)nFiles != Jpsi_.size()){
    cout<<"number of Jpsi_ must = nFiles"<<endl;
    cout<<"nFiles = "<<nFiles<<" while Jpsi_.size() = "<<Jpsi_.size()<<endl;
    exit(EXIT_FAILURE);
  }else if(massname.size()!=(unsigned int)nFiles){
    cout<<"number of mass names must equal the number of files"<<endl;
    exit(EXIT_FAILURE);
  }

  int idatafile;//to store the index of the data file
  int iLMCfile;//to store the index of the L0 file
  int iSMCfile;//to store the index of the sig0 file
  cout<<"Starting file loop..."<<endl;
  for(int ifile=0;ifile<nFiles;ifile++){
    //store file indices
    if(f[ifile].name=="data") idatafile = ifile;
    if(f[ifile].name=="#Lambda^{0} MC") iLMCfile = ifile;
    if(f[ifile].name=="#Sigma^{0} MC") iSMCfile = ifile;
    cout<<"Using "<<f[ifile].name<<"..."<<endl;
    // myfile<<f[ifile].name;
    // //use appropriate mass parameter
    // placeholder = Lbname[ifile]+"_MM";
    // if(f[ifile].quality["filetype"]=="data") {
    //   placeholder = "Bs_LOKI_MASS_JpsiConstr";
    //   cout<<"using Bs_LOKI_MASS_JpsiConstr"<<endl;
    // }
    // placeholder2 = Lbname[ifile]+"_BKGCAT";
    placeholder3 = Lbname[ifile]+"_PT";
    f[ifile].b={{placeholder3,"#Lambda_{b} p_{T}",4000,0,20000},    \
                {placeholder3,"#Lambda_{b} p_{T} LL",4000,0,20000}, \
                {placeholder3,"#Lambda_{b} p_{T} DD",4000,0,20000},     \
                {placeholder3,"#Lambda_{b} p_{T}",400,0,20000},        \
                {placeholder3,"#Lambda_{b} p_{T} LL",400,0,20000},     \
                {placeholder3,"#Lambda_{b} p_{T} DD",400,0,20000}};
                // {placeholder,massname[ifile],400,4100,6100},\
                // {placeholder,massname[ifile]+" LL",400,4100,6100},\
                // {placeholder,massname[ifile]+" DD",400,4100,6100}};
                // {placeholder2,"#Lambda_{b} BKGCAT",131,0,131}                    \
                // {"J_psi_1S_MM","J/#psi(1S) MM",48,2980,3220},                    \
                // {"J_psi_1S_ENDVERTEX_CHI2/J_psi_1S_ENDVERTEX_NDOF","#chi^{2}/ndof(J/#psi(1S))",210,0,21}, \
                // {"R_WM","#Lambda^{0} M with p #rightarrow #pi",80,300,700}, \
                // {"H2_TRACK_GhostProb","#pi track GhostProb",100,0,1},   \
                // {"H1_TRACK_GhostProb","p track GhostProb",100,0,1},      \
                // {"muplus_TRACK_GhostProb","#mu^{+} track GhostProb",100,0,1}, \
                // {"muminus_TRACK_GhostProb","#mu^{-} track GhostProb",100,0,1}};
    cout<<"branches declared"<<endl;
    f[ifile].add_tree("Lb2JpsiLTree/mytree");//all 3 files have the same tree
    cout<<"tree added"<<endl;
    
    int nBranches = f[ifile].b.size();
    
    TCut cH1LL = "H1_TRACK_Type==3";
    TCut cH2LL = "H2_TRACK_Type==3";
    TCut cLL = cH1LL&&cH2LL;
    TCut cH1DD = "H1_TRACK_Type==5";
    TCut cH2DD = "H2_TRACK_Type==5";
    TCut cDD = cH1DD&&cH2DD;
    TCut cmupLL = "muplus_TRACK_Type==3";
    TCut cmumLL = "muminus_TRACK_Type==3";
    TCut cmupDD = "muplus_TRACK_Type==5";
    TCut cmumDD = "muminus_TRACK_Type==5";
    
    TCut cLbBKGCAT = "Lambda_b0_BKGCAT<20";
    TCut cLBKGCAT = "R_BKGCAT==0";
    TCut cpTRUEID = "H1_TRUEID==2212||H1_TRUEID==-2212";
    TCut cpiTRUEID = "H2_TRUEID==211||H2_TRUEID==-211";
    TCut cJpsiBKGCAT = "J_psi_1S_BKGCAT==0";
    
    TCut cLFD = "R_FDCHI2_ORIVX>50";
    TCut cLMM1 = "(R_MM>1112)&&(R_MM<1120)";
    TCut cLMM2 = "(R_MM>1110)&&(R_MM<1122)";
    TCut cLZ = "R_ENDVERTEX_Z>500";
    TCut cJpsiMM = "((J_psi_1S_MM-3096.92)>-48)&&((J_psi_1S_MM-3096.92)<43)";
    
    TCut cLWM = "(R_WM-497.614<-40)||(R_WM-497.614>40)";
    placeholder = "(J_psi_1S"+Jpsi_[ifile]+\
      "Hlt1DiMuonHighMassDecision_TOS==1)||(J_psi_1S"+Jpsi_[ifile]+"Hlt1TrackMuonDecision_TOS==1)";
    TCut ctriggerHlt1part1=(TCut)placeholder;
    placeholder="J_psi_1S"+Jpsi_[ifile]+"Hlt1TrackAllL0Decision_TOS==1";
    TCut ctriggerHlt1part2=(TCut)placeholder;
    TCut ctriggerHlt1=ctriggerHlt1part1||ctriggerHlt1part2;
    placeholder="J_psi_1S"+Jpsi_[ifile]+"Hlt2DiMuonDetachedJPsiDecision_TOS==1";
    TCut ctriggerHlt2=(TCut)placeholder;
    TCut ctrigger = ctriggerHlt1&&ctriggerHlt2;
    //cuts whose name varies by file:
    placeholder=Lbname[ifile]+"_ENDVERTEX_CHI2/"+Lbname[ifile]+"_ENDVERTEX_NDOF<10";
    TCut cLbendv=(TCut)placeholder;
    TCut cLiming = cLPT()&&cLbDIRA(ifile)&&cLFD&&((cLL&&cgprob()&&cLMM1)||(cDD&&cLZ&&cLMM2&&cLbendv&&cJpsiMM));
    TCut cWMtot = cLiming&&cLWM;
    TCut ctriggertot = cWMtot&&ctrigger;

    placeholder2=Form("%f",bkgcutofflo);
    placeholder=massname[ifile]+"<"+placeholder2;
    TCut cbkglo=(TCut)placeholder;
    placeholder2=Form("%f",bkgcutoffhi);
    placeholder=massname[ifile]+">"+placeholder2;
    TCut cbkghi=(TCut)placeholder;
    TCut cbkg;
    if(bkgcutofflo<bkgcutoffhi) cbkg = cbkglo||cbkghi;
    if(bkgcutofflo>=bkgcutoffhi) cbkg = cbkglo;
    cout<<"cbkg = "<<cbkg<<endl;

    placeholder=massname[ifile]+">5500&&"+massname[ifile]+"<5775";
    TCut cLreg = (TCut)placeholder;
    placeholder=massname[ifile]+">5300&&"+massname[ifile]+"<5650";
    TCut cSreg = (TCut)placeholder;
    placeholder=massname[ifile]+">=5775&&"+massname[ifile]+"<5975";
    TCut cbkgreg = (TCut)placeholder;
    //the following cuts are variations on the above:
    // TCut cmid = cLPT()&&cLbDIRA(ifile)&&cLFD&&cJpsiMM&&((cLL&&cgprob()&&cLMM1)||(cDD&&cLZ&&cLMM2&&cLbendv))&&cLWM&&ctrigger;
 // TCut clo=cLPT()&&cLbDIRA(ifile,0.999)&&cLFD&&cJpsiMM&&((cLL&&cgprob()&&cLMM1)||(cDD&&cLZ&&cLMM2&&cLbendv))&&cLWM&&ctrigger;
    // TCut chiLL=cLPT()&&cLbDIRA(ifile,0.99999993)&&cLFD&&cJpsiMM&&((cLL&&cgprob()&&cLMM1)||(cDD&&cLZ&&cLMM2&&cLbendv))\
    //   &&cLWM&&ctrigger;
    // TCut chiDD=cLPT()&&cLbDIRA(ifile,0.999999995)&&cLFD&&cJpsiMM&&((cLL&&cgprob()&&cLMM1)||(cDD&&cLZ&&cLMM2&&cLbendv))\
    //   &&cLWM&&ctrigger;
    // TCut chi=(chiLL&&cLL)||(chiDD&&cDD);


    cout<<"cuts (mostly) declared"<<endl;
    
    cout<<endl<<"Starting branch loop..."<<endl;
    for(int ibranch=0; ibranch<nBranches; ibranch++){
      cout<<"On branch "<<f[ifile].b[ibranch].name<<" for file "<<f[ifile].name<<"..."<<endl;
      
      //assign cuts
      TCut coptimized=((cLL&&cLPT(1300))||(cDD&&cLPT(2100)))&&cLbDIRA(ifile,0.999993) \
        &&cLFD&&cJpsiMM&&((cLL&&cgprob()&&cLMM1)||(cDD&&cLZ&&cLMM2&&cLbendv)) \
        &&cLWM&&ctrigger;
      TCut ctight=((cLL&&cLPT(6000))||(cDD&&cLPT(7000)))&&cLbDIRA(ifile,0.999999) \
        &&cLFD&&cJpsiMM&&((cLL&&cgprob()&&cLMM1)||(cDD&&cLZ&&cLMM2&&cLbendv)) \
        &&cLWM&&ctrigger;
      f[ifile].b[ibranch].c ={{coptimized,"Optimized: cos()>0.999993 with #Lambda_{p_{T}}>1300 LL or >2100 DD"},\
                              {ctight,"Tight: cos()>0.999999 with #Lambda_{p_{T}}>6000 LL or >7000 DD"}}; 
        // }else if(f[ifile].b[ibranch].name.Contains("mid")){
        //   for(int i=0;i<12000;i+=100){
        //     TCut cmidLPT=cLPT(i)&&cLbDIRA(ifile)&&cLFD&&cJpsiMM&&((cLL&&cgprob()&&cLMM1)||(cDD&&cLZ&&cLMM2&&cLbendv)) \
        //       &&cLWM&&ctrigger;
        //     TString istring = Form("%i",i);
        //     placeholder = "cos()>0.9999 and #Lambda_{p_{T}}>"+istring;
        //     f[ifile].b[ibranch].add_cut(cmidLPT,placeholder);
        //   }        
        // }else if(f[ifile].b[ibranch].name.Contains("hi")){
        //   for(int i=0;i<12000;i+=100){
        //     TCut chiLLLPT=cLPT(i)&&cLbDIRA(ifile,0.99999993)&&cLFD&&\
        //       cJpsiMM&&((cLL&&cgprob()&&cLMM1)||(cDD&&cLZ&&cLMM2&&cLbendv))&&cLWM&&ctrigger;
        //     TCut chiDDLPT=cLPT(i)&&cLbDIRA(ifile,0.999999995)&&cLFD&&\
        //       cJpsiMM&&((cLL&&cgprob()&&cLMM1)||(cDD&&cLZ&&cLMM2&&cLbendv))&&cLWM&&ctrigger;
        //     TCut chiLPT=(chiLLLPT&&cLL)||(chiDDLPT&&cDD);
        //     TString istring = Form("%i",i);
        //     placeholder = "cos()>0.99999993 for LL and >0.999999995 for DD and #Lambda_{p_{T}}>"+istring;
        //     f[ifile].b[ibranch].add_cut(chiLPT,placeholder);
        //   }        
        // }
        // if(f[ifile].quality["filetype"]=="MC") 
        //   for(unsigned int i=0; i<f[ifile].b[ibranch].c.size(); i++)
        //     f[ifile].b[ibranch].c[i]=f[ifile].b[ibranch].c[i].self&&cpTRUEID&&cpiTRUEID;
        // //for SMC, we want to see only the real stuff
      
      // else if(f[ifile].b[ibranch].self=="H2_TRACK_GhostProb") f[ifile].b[ibranch].c={cH2LL,cH2DD};
      // else if(f[ifile].b[ibranch].self=="H1_TRACK_GhostProb") f[ifile].b[ibranch].c={cH1LL,cH1DD};
      // else if(f[ifile].b[ibranch].self=="muplus_TRACK_GhostProb") f[ifile].b[ibranch].c={cmupLL,cmupDD};
      // else if(f[ifile].b[ibranch].self=="muminus_TRACK_GhostProb") f[ifile].b[ibranch].c={cmumLL,cmumDD};
      
      int nCuts = f[ifile].b[ibranch].c.size();
      if(nCuts==0){
        //for branches with no cuts assigned, 
        //we must give them an empty cut with an empty name
        //so they can be plotted in the cuts loop
        f[ifile].b[ibranch].c = {{"",""}};
        nCuts = f[ifile].b[ibranch].c.size();
      }
      //create necessary canvasy things
      TString cistring = Form("%d",ci);
      placeholder = "c"+cistring;
      c.push_back( new TCanvas(placeholder,placeholder,1200,800) ); //create the canvases
      c[ci]->cd();
      gStyle->SetOptStat("");
      leg.push_back( new TLegend(0.125, 0.6, 0.625, 0.93) );//create legend
      placeholder = "hs"+cistring;
      hs.push_back( new THStack(placeholder,placeholder) ); //create the stack to hold the histograms
      TString leglabel="";
      TString stacktitle="";
      h.resize(ci+1);
      
      int icolor = 0;//color counter
      
      for(int icut =0; icut<nCuts; icut++){
        //adjust LL and DD branches to have LL and DD cuts
        if(f[ifile].b[ibranch].name.Contains("LL")){
          f[ifile].b[ibranch].c[icut].self=f[ifile].b[ibranch].c[icut].self&&cLL;
          f[ifile].b[ibranch].c[icut].name+=" LL";
        }
        if(f[ifile].b[ibranch].name.Contains("DD")){
          f[ifile].b[ibranch].c[icut].self=f[ifile].b[ibranch].c[icut].self&&cDD;
          f[ifile].b[ibranch].c[icut].name+=" DD";
        }
        
        cout<<"On cut "<<f[ifile].b[ibranch].c[icut].name<<"..."<<endl;
        //create convenient strings
        TString icutstring = Form("%d",icut);
        TString hname = "h"+cistring+icutstring;
        TString htitle = f[ifile].b[ibranch].name;
        //create histogram
        int nBins = f[ifile].b[ibranch].nBins;
        int loBin = f[ifile].b[ibranch].loBin;
        int hiBin = f[ifile].b[ibranch].hiBin;
        h[ci].push_back( new TH1F(hname,htitle,nBins,loBin,hiBin) );
        //draw histogram
        cout<<"\rdrawing histogram "<<icut+1<<"/"<<nCuts<<"...";
        while(icolor==0||icolor==5||icolor==10||(icolor>=17&&icolor<=19)) 
          icolor++;//skip bad colors 
        h[ci][icut]->SetLineColor(icolor);
        placeholder = f[ifile].b[ibranch].self+">>"+hname;
        TCut * thiscut = &f[ifile].b[ibranch].c[icut].self;
        cut * mycut = &f[ifile].b[ibranch].c[icut];
        f[ifile].t[0]->Draw(placeholder,*thiscut,drawopt);//there's only one tree per file
        // //calculate sig/bkg
        // cout<<"\rcalculating sig/bkg "<<icut+1<<"/"<<nCuts<<"...";
        // int nbkg = (int)f[ifile].t[0]->GetEntries(*thiscut&&cbkg);//number passing cbkg
        // int nent = (int)f[ifile].t[0]->GetEntries(*thiscut);//total number
        // int nsig = nent - nbkg;
        // mycut->nbkg = nbkg;
        // mycut->nsig = nsig;
        // mycut->nL = (int)f[ifile].t[0]->GetEntries(*thiscut&&cLreg);//number in /\ region
        // mycut->nS = (int)f[ifile].t[0]->GetEntries(*thiscut&&cSreg);//number in S region
        // mycut->nb = (int)f[ifile].t[0]->GetEntries(*thiscut&&cbkgreg);//number in bkg region
        
        // float ratio = sqrt((float)nsig/(float)nbkg); 
        //stack histogram
        cout<<"\rstacking histogram "<<icut+1<<"/"<<nCuts<<"...";
        leglabel=f[ifile].b[ibranch].c[icut].name;
        // placeholder2=Form("%.3f",ratio);
        leg[ci]->AddEntry(h[ci][icut],leglabel,"l");//fill legend
        hs[ci]->Add(h[ci][icut]);//stack histogram
        //store calculations
        // myfile<<","<<leglabel<<","                                      \
        //       <<Form("%i",nsig)<<","                                    \
        //       <<Form("%i",nbkg)<<endl;
        //calculate SMC sig/data bkg
        // if(ifile==(nFiles-1)){//ensure everything's been calculated
        //   if(ibranch==0&&icut==0){
        //     trueratiostring +="summary,cuts,L0 sig,L0 bkg,S0 sig,S0 bkg,data sig,data bkg";
        //     trueratiostring +=",L/sqrt(L+B),S/sqrt(S+B)";
        //     trueratiostring +=",nL,nS,nb\n";
        //   }
        //   if(f[iSMCfile].b[ibranch].c[icut].name==f[idatafile].b[ibranch].c[icut].name \
        //      &&f[iSMCfile].b[ibranch].c[icut].name==f[iLMCfile].b[ibranch].c[icut].name){
        //     //only for cuts in common; should probably check branches too,
        //     //but the name varies by file and I don't want to code all that in right now
        //     int nLs = f[iLMCfile].b[ibranch].c[icut].nsig;
        //     int nLb = f[iLMCfile].b[ibranch].c[icut].nbkg;
        //     int nSs = f[iSMCfile].b[ibranch].c[icut].nsig;
        //     int nSb = f[iSMCfile].b[ibranch].c[icut].nbkg;
        //     int nds = f[idatafile].b[ibranch].c[icut].nsig;
        //     int ndb = f[idatafile].b[ibranch].c[icut].nbkg;
        //     float ratioL = ((float)nLs+(float)nLb)/sqrt((float)nLs+(float)nLb+(float)ndb);
        //     float ratioS = ((float)nSs+(float)nSb)/sqrt((float)nSs+(float)nSb+(float)ndb);
        //     int nL = f[iLMCfile].b[ibranch].c[icut].nL;
        //     int nS = f[iLMCfile].b[ibranch].c[icut].nS;
        //     int nb = f[iLMCfile].b[ibranch].c[icut].nb;
            
        //     trueratiostring+=","+f[ifile].b[ibranch].c[icut].name+","+Form("%i",nLs)+"," \
        //       +Form("%i",nLb)+","+Form("%i",nSs)+","+Form("%i",nSb)+","+Form("%i",nds)+","+Form("%i",ndb)+"," \
        //       +Form("%.6f",ratioL)+","+Form("%.6f",ratioS)+","          \
        //       +Form("%i",nL)+","+Form("%i",nS)+","+Form("%i",nb)+"\n";
        //   }
        // }

        icolor++;
      }
      stacktitle+=f[ifile].name+", "+f[ifile].b[ibranch].name;
      //draw stacked histograms
      cout<<"\rdrawing stack "<<ci+1<<": "<<stacktitle<<"...";
      hs[ci]->SetTitle(stacktitle);
      hs[ci]->Draw("nostack");
      leg[ci]->Draw();
      //save stuff:
      cout<<"\rsaving files for stack "<<ci+1<<"...";
      placeholder = outputlocation+filename+"(";//the closing page is added after the loop
      c[ci]->Print(placeholder);
      if(runmode.Contains("C")){
        placeholder = outputlocation+"c"+cistring+"_"+stacktitle+".C";
        c[ci]->SaveAs(placeholder);
      }
      cout<<endl;
      ci++;//iterates every time we finish a branch
    }
  }
  int nCanvases=ci;
  float sqnc = sqrt(nCanvases), sqncu = ceil(sqnc), sqncd = floor(sqnc);
  while(sqncu*sqncd<nCanvases) sqncu++;//makes rows and columns close to square
  cf->Divide(sqncu,sqncd);//canvas divided to be able to hold all other canvases
  for(int i=0;i<nCanvases;i++){//fill cf
    cf->cd(i+1);//because cd() counts from 1
    c[i]->DrawClonePad();
  }
  placeholder = outputlocation+filename+")";
  cf->Print(placeholder);
  // myfile<<trueratiostring;//include at end of CSV file
  // myfile.close();
  gROOT->SetBatch(kFALSE);
  cout<<"done"<<endl;
}
