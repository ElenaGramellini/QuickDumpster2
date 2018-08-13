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
TFile *f1 = new TFile("PionData_dEdXPlot.root");

// ###################################
// ### Load Pion Monte Carlo Plots ###
// ###################################
TFile *f2 = new TFile("PionMC_dEdXPlot.root");

//--------------------------------------------------------------------------------------------------------------
//						dE/dX Plots
//--------------------------------------------------------------------------------------------------------------

// ### Getting the data dE/dX plot ###
TH1F *hDatadEdX = (TH1F*)f1->Get("hRecodEdX");
 hDatadEdX->SetBinContent(1,0);
// ### Labeling the axis ###
hDatadEdX->GetXaxis()->SetTitle("dE/dX (MeV / cm)");
hDatadEdX->GetXaxis()->CenterTitle();

hDatadEdX->GetYaxis()->SetTitle("Events / 0.25 MeV/cm");
hDatadEdX->GetYaxis()->CenterTitle(); 

// ### Getting the MC dE/dX plot ###
TH1F *hMCdEdX = (TH1F*)f2->Get("hRecodEdX");

// ### Labeling the axis ###
hMCdEdX->GetXaxis()->SetTitle("dE/dX (MeV / cm)");
hMCdEdX->GetXaxis()->CenterTitle();

hDatadEdX->GetYaxis()->SetTitle("Events / 0.25 MeV/cm");
hDatadEdX->GetYaxis()->CenterTitle(); 

// ### Normalizing MC to Data ###
double MCIntegral = hMCdEdX->Integral();
double DataIntegral = hDatadEdX->Integral();

double scaleMC = DataIntegral/MCIntegral;


// ==================================================
// == Initializing the parameters which record the ==
// == fit parameters (3 for gaussian 3 for landau) ==
// ==================================================
Double_t par_03[6];
Double_t par_02[6];
TF1 *data_dedx_landau = new TF1("data_dedx_landau","landau",0, 50);
TF1 *combined_data_dedx   = new TF1("combined_data_dedx","landau",0,50);


TF1 *mc_dedx_landau   = new TF1("mc_dedx_landau","landau",0, 50);
TF1 *combined_mc_dedx   = new TF1("combined_mc_dedx","landau",0.,50);

// ### Scaling MC ###
hMCdEdX->Sumw2();
hMCdEdX->Scale(scaleMC);

// ### Fitting the data dE/dX with Landau as a seed ###
hDatadEdX->Fit(data_dedx_landau,"R+0LLi","0",1, 40);

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

hDatadEdX->Fit(combined_data_dedx,"R0LLi","0",1,40);
// #######################################
// ### Making a histogram from the fit ###
// #######################################
combined_data_dedx->GetParameters(par_03);
combined_data_dedx->SetRange(0,50);
TH1D* dataFit_histo = (TH1D*)combined_data_dedx->GetHistogram();
//dataFit_histo->SetFillColor(kBlack);
dataFit_histo->SetFillStyle(0);
dataFit_histo->SetLineColor(kRed);
dataFit_histo->SetLineWidth(2);


// ### Fitting the MC dE/dX with Landau as a seed ###
hMCdEdX->Fit(mc_dedx_landau,"R+0LLi","0",1.0 , 15);

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
hMCdEdX->Fit(combined_mc_dedx,"R0LLi","0",1.0,40);

// #######################################
// ### Making a histogram from the fit ###
// #######################################
combined_mc_dedx->GetParameters(par_02);
combined_mc_dedx->SetRange(0.0,50);
TH1D* MCFit_histo = (TH1D*)combined_mc_dedx->GetHistogram();
//MCFit_histo->SetFillColor(kAzure+9);
MCFit_histo->SetFillStyle(0);
MCFit_histo->SetLineColor(kAzure+9);
MCFit_histo->SetLineWidth(2);


// ########################
// ### Making a TCanvas ###
// ########################
 TCanvas *c04 = new TCanvas("c04", "dEdX",600,600);
c04->SetTicks();
c04->SetFillColor(kWhite);


hMCdEdX->SetLineColor(kBlue);
hMCdEdX->SetLineStyle(0);
hMCdEdX->SetLineWidth(3);

hDatadEdX->SetLineColor(kBlack);
hDatadEdX->SetLineStyle(0);
hDatadEdX->SetLineWidth(3);
hDatadEdX->SetMarkerStyle(8);
hDatadEdX->SetMarkerSize(0.9);


// ### Drawing the histograms ###
hMCdEdX->Draw("histo");
dataFit_histo->Draw("Csames");
MCFit_histo->Draw("Csames");
hDatadEdX->Draw("E1same");


// ############################
// # Setting the Latex Header #
// ############################
TLatex *t = new TLatex();
t->SetNDC();
t->SetTextFont(62);
t->SetTextSize(0.04);
t->SetTextAlign(40);
t->DrawLatex(0.1,0.90,"LArIAT Preliminary");
t->DrawLatex(0.13,0.84,""); 


TLegend *leg = new TLegend();
leg = new TLegend(0.58,0.65,0.88,0.88);
leg->SetTextSize(0.04);
leg->SetTextAlign(12);
leg->SetFillColor(kWhite);
leg->SetLineColor(kWhite);
leg->SetShadowColor(kWhite);
leg->SetHeader("LArIAT Negative Polarity");
leg->AddEntry(hDatadEdX,"Data");
leg->AddEntry(hMCdEdX,"#pi^{-} MC"); 
leg->AddEntry(dataFit_histo,"Data Fit: MPV = 1.63 #sigma 0.17");
leg->AddEntry(MCFit_histo," MC  Fit: MPV = 1.67 #sigma 0.13");
leg->Draw();

}
