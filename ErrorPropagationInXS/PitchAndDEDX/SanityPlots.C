{

// ####################################################################
//        Script to make some sanity plots for the pion analysis
// ####################################################################

#include <TFile.h>
#include <TH1F.h>
#include <TCanvas.h>

// #######################
// ### Load Data Plots ###
// #######################
TFile *f1 = new TFile("./Data_SanityPlots.root");

// ###################################
// ### Load Pion Monte Carlo Plots ###
// ###################################
TFile *f2 = new TFile("./PionMC_SanityPlots.root");

//--------------------------------------------------------------------------------------------------------------
//						Final Kinetic Energy vs Length
//--------------------------------------------------------------------------------------------------------------

// ###################################
// ### Getting the data dE/dX plot ###
// ###################################
TH2F *hDataFinalKEvsLength = (TH2F*)f1->Get("hRecoIntKEvsLength");
TProfile *data_profx = hDataFinalKEvsLength->ProfileX("DataX");
TProfile *data_profy = hDataFinalKEvsLength->ProfileY("Datay");

// ### Labeling the axis ###
data_profx->GetXaxis()->SetTitle("Track Length (cm)");
data_profx->GetXaxis()->CenterTitle();

data_profx->GetYaxis()->SetTitle("<Final Kinetic Energy> (MeV)");
data_profx->GetYaxis()->CenterTitle(); 

data_profy->GetYaxis()->SetTitle("<Track Length> (cm)");
data_profy->GetYaxis()->CenterTitle();

data_profy->GetXaxis()->SetTitle("Final Kinetic Energy (MeV)");
data_profy->GetXaxis()->CenterTitle(); 

// ################################
// ### Getting the Pion MC plot ###
// ################################
TH2F *hPionMCFinalKEvsLength = (TH2F*)f2->Get("hRecoIntKEvsLength");
TProfile *mc_profx = hPionMCFinalKEvsLength->ProfileX("MCX");
TProfile *mc_profy = hPionMCFinalKEvsLength->ProfileY("MCY");
// ### Labeling the axis ###
mc_profx->GetXaxis()->SetTitle("Track Length (cm)");
mc_profx->GetXaxis()->CenterTitle();

mc_profx->GetYaxis()->SetTitle("<Final Kinetic Energy> (MeV)");
mc_profx->GetYaxis()->CenterTitle(); 

mc_profy->GetYaxis()->SetTitle("<Track Length> (cm)");
mc_profy->GetYaxis()->CenterTitle();

mc_profy->GetXaxis()->SetTitle("Final Kinetic Energy (MeV)");
mc_profy->GetXaxis()->CenterTitle(); 

data_profx->SetLineColor(kBlack);
data_profx->SetMarkerColor(kBlack);
data_profx->SetLineStyle(0);
data_profx->SetLineWidth(3);
data_profx->SetMarkerStyle(8);
data_profx->SetMarkerSize(0.9);

data_profy->SetLineColor(kBlack);
data_profy->SetMarkerColor(kBlack);
data_profy->SetLineStyle(0);
data_profy->SetLineWidth(3);
data_profy->SetMarkerStyle(8);
data_profy->SetMarkerSize(0.9);


mc_profx->SetLineColor(kBlue);
mc_profx->SetMarkerColor(kBlue);
mc_profx->SetLineStyle(0);
mc_profx->SetLineWidth(3);
mc_profx->SetMarkerStyle(4);
mc_profx->SetMarkerSize(0.9);

mc_profy->SetLineColor(kBlue);
mc_profy->SetMarkerColor(kBlue);
mc_profy->SetLineStyle(0);
mc_profy->SetLineWidth(3);
mc_profy->SetMarkerStyle(4);
mc_profy->SetMarkerSize(0.9);

// ########################
// ### Making a TCanvas ###
// ########################
TCanvas *c01 = new TCanvas("c01", "KE vs Track Length");
c01->SetTicks();
c01->SetFillColor(kWhite);

data_profx->Draw();
mc_profx->Draw("same");
c01->Update();

// ########################
// ### Making a TCanvas ###
// ########################
TCanvas *c02 = new TCanvas("c02", "Track Length vs KE");
c02->SetTicks();
c02->SetFillColor(kWhite);

data_profy->Draw();
mc_profy->Draw("same");
c02->Update();

}
