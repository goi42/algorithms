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

//-----------------------------------------------------------------------------
// Implementation file for class : makeplots
//
// 2015-10-22 : Michael Wilkinson
//-----------------------------------------------------------------------------

//=============================================================================
// Standard constructor, initializes variables
//=============================================================================
void makeplots(TString runmode = "d", TString drawopt = "norm"){
  gROOT->SetBatch(kTRUE);
  cout<<endl<<"If you want to use custom parameters, option 'b' for branch, 'c' for cuts,"\
      <<", 'o' to specify the output, or 'f' to select the files and trees to include."<<endl;
  cout<<"Option 'C' saves canvases as .C files."<<endl;
  cout<<"The second parameter is the draw option. 'norm' by default."<<endl<<endl;
  cout<<"This program handles a specified number of variations and generates plots from the files corresponding to these.";
  cout<<" E.g., year, decay, and filetype would plot stuff from nYears*nDecays*nFileTypes files, labeled accordingly.";
  cout<<" This is in addition to however many branches and cuts you would like to perform."<<endl<<endl;
  TString placeholder;//this is to avoid adding strings in functions; assign right before use
  TString placeholder2;
  TString response;//this is for user input; assign right before use
  //default parameters
  TString outputlocation="./";
  TString filename="plots.pdf";
  int nFiles=8;
  vector<TFile*> f(nFiles);
  TString tuplelocation = "/afs/cern.ch/work/m/mwilkins/b_b-bar_cross-section/";
  placeholder = tuplelocation+"Strp20r1_SL_D0andDp_MD.root";
  f[0] = TFile::Open(placeholder);//2011 data B-D0
  placeholder = tuplelocation+"Strp20r1_SL_D0andDp_MD.root";
  f[1] = TFile::Open(placeholder);//2011 data B0D-
  placeholder = tuplelocation+"Bu_D0Xmunu_cocktail_12873441_MC2011_S20r1_noPID_Tuples.root";
  f[2] = TFile::Open(placeholder);//2011 MC B-D0
  placeholder = tuplelocation+"Bd_DpXmunu_cocktail_11874401_MC2011_S20r1_noPID_Tuples.root";
  f[3] = TFile::Open(placeholder);//2011 MC B0D-
  placeholder = tuplelocation+"B2DMuNuX_tuples_05082015.root";
  f[4] = TFile::Open(placeholder);//2015 data B-D0
  placeholder = tuplelocation+"B2DMuNuX_tuples_05082015.root";
  f[5] = TFile::Open(placeholder);//2015 data B0D-
  placeholder = tuplelocation+"Bu_D0Xmunu_cocktail_12873441_MC2015_S22_noPID_Tuples.root";
  f[6] = TFile::Open(placeholder);//2015 MC B-D0
  placeholder = tuplelocation+"Bd_DpXmunu_cocktail_11874401_MC2015_S22_noPID_Tuples.root";
  f[7] = TFile::Open(placeholder);//2015 MC B0D-
  vector<TString> tree(nFiles);
  tree[0] = "tupleb2D0Mu/tupleb2D0Mu";
  tree[1] = "tupleb2DpMu/tupleb2DpMu";
  tree[2] = "Tuple_b2D0MuX/DecayTree";
  tree[3] = "Tuple_b2DpMuX/DecayTree";
  tree[4] = "Tuple_b2D0MuX/DecayTree";
  tree[5] = "Tuple_b2DpMuX/DecayTree";
  tree[6] = "Tuple_b2D0MuX/DecayTree";
  tree[7] = "Tuple_b2DpMuX/DecayTree";
  int nLayers=5;//year, filetype, decay, branch, cuts
  vector<TString> Lresponse(nLayers);
  Lresponse[0]="year";
  Lresponse[1]="filetype";
  Lresponse[2]="decay";
  Lresponse[3]="branch";
  Lresponse[4]="cut";
  vector<int> nL(nLayers);
  nL[0]=2;
  nL[1]=2;
  nL[2]=2;
  nL[3]=1;
  nL[4]=1;
  vector< vector<TString> > L;//L[layer][layerelement]
  L.resize(nLayers);
  for(int i=0; i<nLayers; i++){
    L[i].resize(nL[i]);
  }
  L[0][0]="2011";
  L[0][1]="2015";
  L[1][0]="data";
  L[1][1]="MC";
  L[2][0]="B^{-}->(D^{0}->K^{-} #pi^{+})#mu^{-}";
  L[2][1]="B^{0}->(D^{-}->K^{+} #pi^{-} #pi^{-})#mu^{+}";
  L[3][0]="";
  L[4][0]="";
  int bL=3;//index corresponding to branch layer
  int nBranches=1;
  int cL=4;//index corresponding to cut layer
  int nCuts=1;
  vector< vector<TString> > branch;//branch[file][branches]
  branch.resize(nFiles);//finished resizing below in loop with cut vector
  vector<int> nBins(nBranches);
  nBins[0]=131;//these are for nLongTracks
  vector<int> loBin(nBranches);
  loBin[0]=0;
  vector<int> hiBin(nBranches);
  hiBin[0]=262;
  vector< vector< vector<TString> > > cut;//cut[file][branch][cuts]
  cut.resize(nFiles);
  for(int i=0;i<nFiles;i++){//resize and fill branch and cut vectors
    cut[i].resize(nBranches);
    branch[i].resize(nBranches);
    for(int j=0; j<nBranches; j++){
      cut[i][j].resize(nCuts);
      branch[i][j]="nLongTracks";//only one branch; same for all these files
      for(int k=0; k<nCuts; k++){
        if(i%2==0){//since I've listed the files alternating by decay
          cut[i][j][k]="(B_M>3500)&&(B_M<5000)&&(D_M>1849.84)&&(D_M<1879.84)";
        } else{
          cut[i][j][k]="(B_M>3500)&&(B_M<5000)&&(D_M>1854.61)&&(D_M<1884.61)";
        }
      }
    }
  }
  int nComparisons=1;
  vector<TString> comparison(nComparisons);
  comparison[0]="decay";
  int nhpc=2;
  int nCanvases=4;
  vector<TString> list(0);//this holds the combinations of things used to describe the files; 
  //                        keep empty as the combinations are appended in get custom parameters
  //-----------------------------get custom parameters-----------------------//
  if(runmode.Contains("o")){
    cout<<"Where should the output be stored? (make sure the directory exists; include / at end)"<<endl;
    cin>>outputlocation;
    cout<<"What should the output file be called? (include extension, e.g., 'plots.pdf')"<<endl;
    cin>>filename;
  }
  if(runmode.Contains("f")){
    //ask levels of variation
    cout<<"How many levels of variation, including branch and cuts? ";
    cout<<"E.g., if you wanted to compare years, decays, and cuts, you would say 3."<<endl;
    cin>>nLayers;
    while(nLayers<=0){
      cout<<"You must specify at least one layer."<<endl;
      cin>>nLayers;
    }
    cout<<"How many of these would you like on the same plot?"<<endl;
    cin>>nComparisons;
    while(nComparisons<0||nComparisons>nLayers){
      cout<<"Your response can be from 0 to "<<nLayers<<"."<<endl;
      cin>>nComparisons;
    }
    Lresponse.resize(nLayers);
    L.resize(nLayers);
    comparison.resize(nComparisons);
    //ask to name each layer
    cout<<"What would you like to compare? (Note that cut and branch must be called 'cut' and 'branch'.)"<<endl;
    if(nComparisons>0) cout<<"Your last "<<nComparisons<<" selection(s) will be overlaid on the plots."<<endl;
    for(int i=0;i<nLayers;i++){
      cout<<"Layer #"<<i<<": ";
      Lresponse[i].ReadLine(std::cin);
      //-----check for syntax/spelling errors in 'branch' and 'cut'
      bool branch_check=kFALSE;
      bool cut_check=kFALSE;
      if(Lresponse[i].Contains("ranc",kIgnoreCase)&&Lresponse[i]!="branch") branch_check=kTRUE;
      if(branch_check){
        cout<<"You entered "<<Lresponse[i]<<". Did you mean 'branch' (necessary syntax if you're comparing branches)? (y/n)";
        cin>>response;
        while(!(response=="y"||response=="n")){
          cout<<"y/n";
          cin>>response;
        }
        if(response=="y") Lresponse[i] = "branch";
      }
      if(Lresponse[i].Contains("ut",kIgnoreCase)&&Lresponse[i]!="cut") cut_check=kTRUE;
      if(cut_check){
        cout<<"You entered "<<Lresponse[i]<<". Did you mean 'cut' (necessary syntax if you're comparing cuts)? (y/n)";
        cin>>response;
        while(!(response=="y"||response=="n")){
          cout<<"y/n";
          cin>>response;
        }
        if(response=="y") Lresponse[i] = "cut";
      }
      //----end syntax/spelling check
      if(Lresponse[i]=="cut") runmode +="c";//make sure we go through those options
      if(Lresponse[i]=="branch") runmode +="b";
      if(i>=(nLayers-nComparisons))//now we're in the realm of comparisons
        comparison[i-(nLayers-nComparisons)]=Lresponse[i];
    }
    //------check that all levels are unique------//
    bool yes=kTRUE;//do any Lresponse[i] match any other?
    while(yes){
      yes=kFALSE;
      for(int i=0;i<4;i++){
        for(int j=0;j<4;j++){
          if(i!=j){
            while(Lresponse[i]==Lresponse[j]){
              yes=kTRUE;
              cout<<"all 4 levels must be unique"<<endl;
              cout<<"you entered "<<Lresponse[i]<<" for both level "<<i<<" and level "<<j<<endl;
              cout<<"please change "<<Lresponse[i]<<" to something unique or your output won't make sense"<<endl;
              cout<<"what would you like level "<<i<<" to be?"<<endl;
              Lresponse[i].ReadLine(std::cin);
            }
          }
        }
      }
    }
    //ask to fill each layer
    cout<<"We're going to fill each layer."<<endl;
    nhpc=1;
    nCanvases=1;
    for(int i=0;i<nLayers;i++){
      cout<<"How many "<<Lresponse[i]<<"?"<<endl;
      cin>>nL[i];
      //number of files equals the product of all the variations, except for branch and cuts
      if(!(Lresponse[i]=="cut"||Lresponse[i]=="branch")) nFiles *= nL[i];
      for(int j=0;j<nL[i];j++){
        if(!(Lresponse[i]=="cut"||Lresponse[i]=="branch")){//filled in separate vectors; their L[][] are empty
          cout<<"What is "<<Lresponse[i]<<" #"<<j<<"?"<<endl;
          response.ReadLine(std::cin);
          L[i].push_back(response);
        } else{L[i].push_back("");}//empty for easier filling of titles later
      }
      if(i>=(nLayers-nComparisons)){ nhpc*=nL[i];//now we're in the realm of comparisons
      }else{nCanvases *= nL[i];}
    }
    //ask for files
    f.resize(nFiles);
    tree.resize(nFiles);
    cut.resize(nFiles);
    branch.resize(nFiles);
    TString same;
    cout<<"Are all the files in the same folder? (y/n)"<<endl;
    cin>>same;
    while(!(same=="y"||same=="n")){
      cout<<"y/n?"<<endl;
      cin>>same;
    }
    TString filelocation="";
    if(same=="y"){
      cout<<"What folder (include '/' at the end)?"<<endl;
      filelocation.ReadLine(std::cin);
      while(filelocation[filelocation.Length()-1] != "/"){
        cout<<"Try again. Include '/' at the end."<<endl;
        filelocation.ReadLine(std::cin);
      }
    }
    storeAll(L,0,"",list);//list now holds all combinations of L, with Lresponse[0] iterating least frequently
    for(unsigned int i=0;i<list.size();i++){
      cout<<"File "<<i<<" is for "<<list[i]<<endl;
      cout<<"Where is it ";
      if(same=="y") cout<<"(e.g., decay.root)?"<<endl;
      if(same=="n") cout<<"(e.g., ~/tuples/decay.root)?"<<endl;
      response.ReadLine(std::cin);
      while(!(response.Contains("."))){
        cout<<"Include the file extension."<<endl<<"Where is it?"<<endl;
        response.ReadLine(std::cin);
      }
      placeholder=filelocation+response;
      f[i]=TFile::Open(placeholder);
      if(i==0) cout<<"Specify the folder and tree for your decay, e.g., 'Tuple_b2D0MuX/DecayTree':"<<endl;//ask for trees
      cout<<"File "<<i<<" has tree ";
      tree[i].ReadLine(std::cin);
    }
  }
  if(runmode.Contains("b")){ //ask for branches
    for(int i=0;i<nLayers;i++){//find the "branch" layer
      if(Lresponse[i]=="branch"){//only do the following for the "branch" layer
        cout<<"how many branches?"<<endl;
        cin>>nBranches;
        bL=i;//bL is the index of the layer for branches
        nL[i]=nBranches;//these two lines are just to make sure the numbers are right. Branches should not be called using L[][]
        L[i].resize(nBranches);
        response="";
        cout<<"do the names of the branches vary with the file? (y/n)"<<endl;
        cin>>response;
        while(!(response=="y"||response=="n")){
          cout<<"y/n"<<endl;
          cin>>response;
        }
        cout<<"what are the names of the branches you want to draw?"<<endl;
        for(int bi=0; bi<nBranches; bi++){
          for(int fi=0;fi<nFiles;fi++){
            if(bi==0) branch[fi].resize(nBranches);
            if(response=="y") cout<<"for file "<<fi<<", corresponding to "<<list[fi];
            if((response=="n"&&fi==0)||response=="y"){
              cout<<"branch "<<bi<<" = ";
              branch[fi][bi].ReadLine(std::cin);
            }
            if(response=="n") branch[fi][bi]=branch[0][bi];
            if(fi==0){
              cout<<"please select the binning for this branch:"<<endl;
              cout<<"Recommendations:"<<endl;
              cout<<"for nLongTracks: '131','0','262'"<<endl;
              cout<<"for nTracks: '104','0','1144'"<<endl;
              cout<<"nBins = ";
              cin>>nBins[bi];
              cout<<"loBin = ";
              cin>>loBin[bi];
              cout<<"hiBin = ";
              cin>>hiBin[bi];
              cout<<endl;
            }
          }
        }
      }
    }
  }
  if(runmode.Contains("c")){ //ask for cuts
    for(int i=0;i<nLayers;i++){//find the "cut" layer
      if(Lresponse[i]=="cut"){//only do the following for the "cut" layer
        TString fb="";
        cout<<"do the cuts vary by file, branch, both, or neither? (f,b,f/b,n)"<<endl;
        cin>>fb;
        while(!(fb.Contains("f")||fb.Contains("b")||fb.Contains("n")) \
              ||((fb.Contains("f")||fb.Contains("b"))&&fb.Contains("n"))){
          cout<<"f,b,f/b,n?"<<endl;
          cin>>fb;
        }
        cout<<"how many variations of cuts?"<<endl;
        cin>>nCuts;
        cL=i;//cL is the index for the cuts layer
        nL[i]=nCuts;//these two lines are just to match numbers; cuts should not be called using L[][]
        L[i].resize(nCuts);
        for(int j=0; j<nFiles; j++)
          cut[j][i].resize(nL[i]);
        cout<<"what are the cuts?"<<endl;
        for(int ci=0; ci<nCuts;ci++){
          for(int bi=0; bi<nBranches; bi++){
            for(int fi=0;fi<nFiles;fi++){
              cut[fi].resize(nBranches);
              cut[fi][bi].resize(nCuts);
              if(fb.Contains("f")) cout<<"for file "<<fi<<", corresponding to "<<list[fi];
              if(fb.Contains("b")) cout<<"for branch "<<bi<<", "<<branch[fi][bi]<<",";
              cout<<endl;
              if((fb=="n"&&fi==0&&bi==0)||(fb=="f"&&bi==0)||(fb=="b"&&fi==0)||(fb.Contains("f")&&fb.Contains("b"))){
                cout<<"cut "<<ci<<" = ";
                cut[fi][bi][ci].ReadLine(std::cin);
              }
              if(fb=="n") cut[fi][bi][ci]=cut[0][0][ci];
              if(fb=="f") cut[fi][bi][ci]=cut[fi][0][ci];
              if(fb=="b") cut[fi][bi][ci]=cut[0][bi][ci];
            }
          }
        }
      }
    } 
  }
  //------all parameters have been set-------//
  //------------------------------------canvas loop-----------------------------//
  //create necessary counters, canvases, legends, etc.
  cout<<endl;
  vector<TCanvas*> c(nCanvases);//each canvas holds one stack of histograms
  vector<TLegend*> leg(nCanvases);//one legend per canvas
  vector<THStack*> hs(nCanvases);//one stack per canvas
  vector< vector<TH1F*> > h;
  h.resize(nCanvases, vector<TH1F*>(nhpc));
  TCanvas *cf = new TCanvas("cf","combined");//canvas to hold everything
  float sqnc = sqrt(nCanvases), sqncu = ceil(sqnc), sqncd = floor(sqnc);
  while(sqncu*sqncd<nCanvases) sqncu++;
  cf->Divide(sqncu,sqncd);//canvas divided to be able to hold all other canvases
  TLegend *legf = new TLegend(0.84, 0.84, .99, .95);//legend for cf
  vector<int> Li(nLayers);//counters to help with hierarchy in the loop; L[i][Li[i]] refers to the Lith element of the ith layer
  for(int i=0;i<nLayers;i++){
    Li[i]=0;//initialize all counters to 0
  }
  vector<int> plL(nLayers); //products of things in lower levels to tell when to increment Lii
  for(int i=0;i<nLayers;i++){
    plL[i]=1;//initialize all elements to 1
  }
  for(int i=0; i<nLayers; i++){
    for(int j=(nLayers-1); j>i; j--){
      plL[i]*=nL[j];//find the products
    }
  }
  int pli=0;//this counts the number of plots generated; helps iterate Li[i]
  
  cout<<"starting canvas loop..."<<endl;
  //actual start of the loop
  for(int ci=0; ci<nCanvases; ci++){
    cout<<ci<<" out of "<<nCanvases<<endl;
    
    //create necessary canvasy things
    TString cistring = Form("%d",ci);
    placeholder = "c"+cistring;
    c[ci] = new TCanvas(placeholder,placeholder,1200,800); //create the canvases
    c[ci]->cd();
    gStyle->SetOptStat("");
    leg[ci] = new TLegend(0.7, 0.7, .97, .93);//create legend
    placeholder = "hs"+cistring;
    hs[ci] = new THStack(placeholder,placeholder); //create the stack to hold the histograms
    TString stacktitle="";

    //histogram loop
    for(int hi=0; hi<nhpc; hi++){
      int file_num=0;
      for(int i=0;i<nLayers;i++)
        if(!(Lresponse[i]=="cut"||Lresponse[i]=="branch"))//cuts and branches do not get their own files
          file_num += Li[i]*plL[i];//takes advantage of the order files are asked for
      //create convenient strings
      TString histring = Form("%d",hi);
      TString hname = "h"+cistring+histring;
      //create histograms
      h[ci][hi] = new TH1F(hname,branch[file_num][Li[bL]],nBins[Li[bL]],loBin[Li[bL]],hiBin[Li[bL]]);
      cout<<"histogram loop "<<hi<<" strings and histograms created"<<endl;
      cout<<"using file "<<file_num<<endl;
      //navigate files
      cout<<"navigating file..."<<endl;
      TTree *MyTree;
      f[file_num]->GetObject(tree[file_num],MyTree);
      //draw histograms
      cout<<"drawing histogram "<<hi<<"..."<<endl;
      h[ci][hi]->SetLineColor(hi+1);
      placeholder = branch[file_num][Li[bL]]+">>"+hname;
      MyTree->Draw(placeholder,cut[file_num][Li[bL]][Li[cL]],drawopt);
      pli++;//iterate the number of plots that have been drawn
      cout<<"stacking histogram "<<hi<<"..."<<endl;
      hs[ci]->Add(h[ci][hi]);//stack histograms
      
      //loop over layers
      TString leglabel="";
      for(int i=0;i<nLayers;i++){
        //determine the name of the stack title
        bool yes=kFALSE;
        for(int j=0;j<nComparisons;j++) if(Lresponse[i]==comparison[j]) yes=kTRUE;//is this layer being compared?
        if(yes==kTRUE){//if it is, we want it in the legend entry
          if(leglabel!="") leglabel+=", ";
          leglabel+=L[i][Li[i]];
          if(Lresponse[i]=="cut") leglabel+=cut[file_num][Li[bL]][Li[cL]];
          if(Lresponse[i]=="branch") leglabel+=branch[file_num][Li[bL]];
        }
        if(hi==0){//since stacktitle reflects non-compared layers, it only needs to change per canvas
          if(yes==kFALSE){//if it's not, we want it in the title
            if(stacktitle!="") stacktitle+=": ";
            stacktitle+=L[i][Li[i]];
            if(Lresponse[i]=="cut") stacktitle+=cut[file_num][Li[bL]][Li[cL]];
            if(Lresponse[i]=="branch") stacktitle+=branch[file_num][Li[bL]];
          }
        }

        //iterate layer counters
        if(plL[i]==1){Li[i]++;//if it's at the lowest hierarchy, iterate
        }else{ if((pli%plL[i]==0)&&(pli!=0))Li[i]++;}//if all variations of plots lower than it have been plotted, iterate
        if(Li[i]==nL[i]) Li[i]=0;//reset the iteration if it's reached the end
      }//end layer loop

      //fill legends
      leg[ci]->AddEntry(h[ci][hi],leglabel,"l");
      if(ci==0) legf->AddEntry(h[ci][hi],leglabel,"l");//each canvas has the same legend
    }//end histogram loop

    //draw stacked histograms
    cout<<"drawing stack "<<ci<<": "<<stacktitle<<"..."<<endl;
    hs[ci]->SetTitle(stacktitle);
    hs[ci]->Draw("nostack");
    if(nComparisons>0) leg[ci]->Draw();
    cf->cd(ci+1);
    hs[ci]->Draw("nostack");//not using c[ci]->DrawClonePad() because too many legends
    //save stuff:
    cout<<"saving files..."<<endl;
    placeholder = outputlocation+filename+"(";//the closing page is added after the loop
    c[ci]->Print(placeholder);
    if(runmode.Contains("C")){
      placeholder = outputlocation+"c"+cistring+"_"+stacktitle+".C";
      c[ci]->SaveAs(placeholder);
    }
    cout<<endl;
  }//end canvas loop
  cf->cd();
  if(nComparisons>0) legf->Draw();
  placeholder = outputlocation+filename+")";
  cf->Print(placeholder);
  for(int i=0;i<nBranches;i++){
    for(int j=0;j<nFiles;j++){
      for(int k=0;k<nCuts;k++){
        if(cut[j][i][k]!="")
          cout<<"in file "<<j<<", branch "<<branch[j][i]<<" had cuts: "<<cut[j][i][k]<<endl;
      }    
    }
  }
  gROOT->SetBatch(kFALSE);
  cout<<"done"<<endl;
}
  
