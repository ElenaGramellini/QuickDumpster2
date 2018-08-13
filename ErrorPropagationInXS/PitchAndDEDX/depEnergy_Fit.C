{

// ####################################################################
// ### This script just makes a dead reckoning between pion MC and  ###
// ###       pion candidate data to get fits for comparisions       ###
// ####################################################################

#include <TFile.h>
#include <TH1F.h>
#include <TCanvas.h>


// #######################
// ### Load Data Plots ###
// #######################
TFile *f1 = new TFile("/lariat/app/users/jasaadi/v06_34_01_PionWeek/PlottingScripts/Data60A_dEdXPlot.root");

// ###################################
// ### Load Pion Monte Carlo Plots ###
// ###################################
TFile *f2 = new TFile("/lariat/app/users/jasaadi/v06_34_01_PionWeek/PlottingScripts/PionMC60A_dEdXPlot.root");

//--------------------------------------------------------------------------------------------------------------
//						dE/dX Plots
//--------------------------------------------------------------------------------------------------------------
 gStyle->SetOptStat(0);
 gStyle->SetOptFit(0);
// ### Getting the data dE/dX plot ###
TH1F *hDataDepE = (TH1F*)f1->Get("hRecoDepositedE");

// ### Labeling the axis ###
hDataDepE->GetXaxis()->SetTitle("Depositied Energy (MeV)");
//hDataDepE->GetXaxis()->CenterTitle();

hDataDepE->GetYaxis()->SetTitle("Entries / 0.02 MeV");
//hDataDepE->GetYaxis()->CenterTitle(); 

// ### Getting the MC dE/dX plot ###
TH1F *hMCDepE = (TH1F*)f2->Get("hRecoDepositedE");

// ### Labeling the axis ###
hMCDepE->GetXaxis()->SetTitle("Depositied Energy (MeV)");
//hMCDepE->GetXaxis()->CenterTitle();

hDataDepE->GetYaxis()->SetTitle("Entries / 0.02 MeV");
//hDataDepE->GetYaxis()->CenterTitle(); 

// ### Normalizing MC to Data ###
double MCIntegral = hMCDepE->Integral();
double DataIntegral = hDataDepE->Integral();

double scaleMC = DataIntegral/MCIntegral;


// ==================================================
// == Initializing the parameters which record the ==
// == fit parameters (3 for gaussian 3 for landau) ==
// ==================================================
Double_t par_03[6];
Double_t par_02[6];
TF1 *data_dedx_landau = new TF1("data_dedx_landau","landau",0.5, 30);
TF1 *combined_data_dedx   = new TF1("combined_data_dedx","landau",0,30);


TF1 *mc_dedx_landau   = new TF1("mc_dedx_landau","landau",0.5, 30);
TF1 *combined_mc_dedx   = new TF1("combined_mc_dedx","landau",0,30);

// ### Scaling MC ###
hMCDepE->Sumw2();
hMCDepE->Scale(scaleMC);

// ### Fitting the data dE/dX with Landau as a seed ###
hDataDepE->Fit(data_dedx_landau,"R+0LLi","0",0.5 , 5);

// ### Get the seed parameters for the Landau+Gaus fit ###
data_dedx_landau->GetParameters(&par_03[0]); //<---Getting parameters from fit 0,1,2


// ===============================================
// == Putting in parameters into combined plots ==
// ===============================================
combined_data_dedx->SetParameters(par_03);
//combined_data_dedx->SetParLimits(0,0,900000);


// ============================================
// ==== Doing the Landau + Gaussian Fit =======
// ============================================

std::cout<<std::endl;
std::cout<<"======================================="<<std::endl;
std::cout<<"Data dE/dX"<<std::endl;
std::cout<<"======================================="<<std::endl;
std::cout<<std::endl;

hDataDepE->Fit(combined_data_dedx,"R0LLi","0",0.5 ,5);
// #######################################
// ### Making a histogram from the fit ###
// #######################################
combined_data_dedx->GetParameters(par_03);
combined_data_dedx->SetRange(0,3.50);
TH1D* dataFit_histo = (TH1D*)combined_data_dedx->GetHistogram();
//dataFit_histo->SetFillColor(kBlack);
dataFit_histo->SetFillStyle(0);
dataFit_histo->SetLineColor(kRed);
dataFit_histo->SetLineWidth(2);


// ### Fitting the MC dE/dX with Landau as a seed ###
hMCDepE->Fit(mc_dedx_landau,"R+0LLi","0",0.5 , 3.5);

// ### Get the seed parameters for the Landau+Gaus fit ###
mc_dedx_landau->GetParameters(&par_02[0]); //<---Getting parameters from fit 0,1,2

// ===============================================
// == Putting in parameters into combined plots ==
// ===============================================
combined_mc_dedx->SetParameters(par_02);
//combined_mc_dedx->SetParLimits(0,47000000,48000000);


std::cout<<std::endl;
std::cout<<"======================================="<<std::endl;
std::cout<<"MC dE/dX"<<std::endl;
std::cout<<"======================================="<<std::endl;
std::cout<<std::endl;

// ============================================
// ==== Doing the Landau + Gaussian Fit =======
// ============================================
hMCDepE->Fit(combined_mc_dedx,"R0LLi","0",0.5 , 5);

// #######################################
// ### Making a histogram from the fit ###
// #######################################
combined_mc_dedx->GetParameters(par_02);
combined_mc_dedx->SetRange(0.5,3.50);
TH1D* MCFit_histo = (TH1D*)combined_mc_dedx->GetHistogram();
//MCFit_histo->SetFillColor(kAzure+9);
MCFit_histo->SetFillStyle(0);
MCFit_histo->SetLineColor(kAzure+9);
MCFit_histo->SetLineWidth(2);


// ########################
// ### Making a TCanvas ###
// ########################
 TCanvas *c04 = new TCanvas("c04", "Deposited Energy",600,600);
c04->SetTicks();
c04->SetGrid();
c04->SetFillColor(kWhite);


hMCDepE->SetLineColor(kBlue);
hMCDepE->SetLineStyle(0);
hMCDepE->SetLineWidth(3);

hDataDepE->SetLineColor(kBlack);
hDataDepE->SetLineStyle(0);
hDataDepE->SetLineWidth(3);
hDataDepE->SetMarkerStyle(8);
hDataDepE->SetMarkerSize(0.9);

 hMCDepE->GetXaxis()->SetRangeUser(0.,3.5);
hMCDepE->SetTitle("; Energy Deposited [MeV]; Normalized Entries per 0.05 MeV");
 hMCDepE->GetYaxis()->SetTitleOffset(1.5);
// ### Drawing the histograms ###
hMCDepE->Draw("histo");
dataFit_histo->Draw("Csames");
MCFit_histo->Draw("Csames");
hDataDepE->Draw("E1same");


// ############################
// # Setting the Latex Header #
// ############################
TLatex *t = new TLatex();
t->SetNDC();
t->SetTextFont(62);
t->SetTextSize(0.04);
t->SetTextAlign(40);
t->DrawLatex(0.6,0.90,"LArIAT Preliminary");
t->DrawLatex(0.13,0.84,""); 


TLegend *leg = new TLegend();
leg = new TLegend(0.38,0.65,0.48,0.88);
leg->SetTextSize(0.04);
leg->SetTextAlign(12);
leg->SetFillColor(kWhite);
leg->SetLineColor(kWhite);
leg->SetShadowColor(kWhite);
leg->SetHeader("LArIAT Negative Polarity -60A");
leg->AddEntry(hDataDepE,"Data");
leg->AddEntry(hMCDepE,"#pi^{-} MC"); 
leg->AddEntry(dataFit_histo,"Data Fit: MPV = 0.785 #sigma = 0.063");
leg->AddEntry(MCFit_histo," MC  Fit: MPV = 0.784 #sigma = 0.062");
leg->Draw();

}
