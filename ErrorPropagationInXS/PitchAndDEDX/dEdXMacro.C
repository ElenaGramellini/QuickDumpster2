#define dEdXMacro_cxx
#include "dEdXMacro.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include <TVector3.h>

/////////////////////////////////// Reco dE/dX //////////////////////////////////////////
TH1D *hRecodEdX  = new TH1D("hRecodEdX", "Matched Track dE/dX", 200, 0, 50);
TH1D *hRecoPitch = new TH1D("hRecoPitch","Matched Track Pitch", 200, 0, 4);

/////////////////////////////////// Deposited Energy //////////////////////////////////////////
TH1D *hRecoDepositedE = new TH1D("hRecoDepositedE", "Matched Track Depositied Energy", 1200, 0, 60);

void dEdXMacro::Loop()
{
if (fChain == 0) return;
Long64_t nentries = fChain->GetEntriesFast();
Long64_t nbytes = 0, nb = 0;

int nTotalEvents = 0;

// ### Loop over all entries ###
for (Long64_t jentry=0; jentry<nentries;jentry++) 
   {
   Long64_t ientry = LoadTree(jentry);
   if (ientry < 0) break;
   nb = fChain->GetEntry(jentry);   nbytes += nb;
   
   // #############################
   // ### Counting Total Events ###
   // #############################
   nTotalEvents++;
   
   // === Outputting every nEvents to the screen ===
   if(nTotalEvents % 500 == 0){std::cout<<"Event = "<<nTotalEvents<<std::endl;}
   
   // ############################
   // ### Loop over recoPoints ###
   // ############################
   for(int nRecoPts = 0; nRecoPts < recoPoints; nRecoPts++)
      {
	if(recoEnDep[nRecoPts] < 0.08){continue;}
	if(recoPitch[nRecoPts] < 0.08){continue;}
	if(recoDEDX [nRecoPts] < 0.08){continue;}
	hRecodEdX->Fill(recoDEDX[nRecoPts]);
	hRecoDepositedE->Fill(recoEnDep[nRecoPts]);
	hRecoPitch->Fill(recoPitch[nRecoPts]);
      
      }//<---end nRecoPts
      
      
   }//<---End jentry loop

// ### Labeling the axis ###
hRecodEdX->GetXaxis()->SetTitle("dE/dX (MeV/cm)");
hRecodEdX->GetXaxis()->CenterTitle();

hRecodEdX->GetYaxis()->SetTitle("Events / 0.25 (MeV/cm)");
hRecodEdX->GetYaxis()->CenterTitle();

// ==================================================
// == Initializing the parameters which record the ==
// == fit parameters (3 for gaussian 3 for landau) ==
// ==================================================
Double_t par_01[6];
Double_t par_02[6];
TF1 *dedx_landau = new TF1("dedx_landau","landau",0, 50);
TF1 *combined_dedx = new TF1("combined_dedx","landau",0,50);

// ### Fitting the data dE/dX with Landau as a seed ###
hRecodEdX->Fit(dedx_landau,"R+0LLi","0",1.0, 40);



// ====================================================
// ======  Make histogram file for data sample  ======= 
TFile myfile("./PionMC_dEdXPlot.root","RECREATE");
   
hRecodEdX->Write();
dedx_landau->Write();   
hRecoDepositedE->Write();
 hRecoPitch->Write();
   
}//<---End Loop Function
