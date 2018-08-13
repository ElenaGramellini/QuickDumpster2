#define SanityChecks_PionMC_cxx
#include "SanityChecks_PionMC.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include <TVector3.h>

/////////////////////////////////// Reco End Point Z //////////////////////////////////////////
TH1D *hRecoEndZ = new TH1D("hRecoEndZ", "End Point Z Position", 210, -5, 100);
/////////////////////////////////// Reco End Point Y //////////////////////////////////////////
TH1D *hRecoEndY = new TH1D("hRecoEndY", "End Point Y Position", 100, -25, 25);
/////////////////////////////////// Reco End Point X //////////////////////////////////////////
TH1D *hRecoEndX = new TH1D("hRecoEndX", "End Point X Position", 110, -5, 50);

/////////////////////////////////// KE vs Length//////////////////////////////////////////
TH2D *hRecoIntKEvsLength = new TH2D("hRecoIntKEvsLength", "Interacting KE vs Length", 110, 0, 110, 750, 0, 1500);


void SanityChecks_PionMC::Loop()
{
if (fChain == 0) return;
Long64_t nentries = fChain->GetEntriesFast();
Long64_t nbytes = 0, nb = 0;

int nTotalEvents = 0;

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

float lengthOfTrack = sqrt( ((recoEndZ - recoVtxZ)*(recoEndZ - recoVtxZ)) + 
                            ((recoEndY - recoVtxY)*(recoEndY - recoVtxY)) + 
			    ((recoEndX - recoVtxX)*(recoEndX - recoVtxX)) );
			    
// ### Finding the final KE at the for the end of the track ###
float FinalKE = 0;
bool FoundIt = false;
for(int ii =0; ii < recoPoints; ii++)
   {
   if(recoIncidentKE[ii] < 0.01 && !FoundIt)
      {FinalKE = recoIncidentKE[ii - 1]; FoundIt = true;}
   
   
   }
//std::cout<<"FinalKE = "<<FinalKE<<std::endl;
hRecoIntKEvsLength->Fill(lengthOfTrack, FinalKE);
   
hRecoEndZ->Fill(recoEndZ);
hRecoEndY->Fill(recoEndY);
hRecoEndX->Fill(recoEndX);

//if(recoInteractingKE < 200){std::cout<<run<<","<<subrun<<","<<eventN<<std::endl;}


}//<---End jentry loops

// ====================================================
// ======  Make histogram file for data sample  ======= 
TFile myfile("./PionMC_SanityPlots.root","RECREATE");
hRecoEndZ->Write();
hRecoEndY->Write();
hRecoEndX->Write();
hRecoIntKEvsLength->Write();

}//<---End SanityChecks_PionMC::Loop()



