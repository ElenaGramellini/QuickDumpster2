{

// ######################################################################################################

// ######################################################################################################
double PionPercentage     = 0.6884635832;
double MuonPercentage     = 0.0455874534822;
double ElectronPercentage = 0.265948963317;


/*double PionPercentage     = 1.0;
double MuonPercentage     = 1.0;
double ElectronPercentage = 1.0;
double PhotonPercentage   = 1.0;
double KaonPercentage     = 1.0;*/


// #######################
// ### Load Data Plots ###
// #######################
TFile *f1 = new TFile("./Data_dEdXPlot.root");

// ###################################
// ### Load Pion Monte Carlo Plots ###
// ###################################
TFile *f2 = new TFile("./PionMC_dEdXPlot.root");

// ###################################
// ### Load Muon Monte Carlo Plots ###
// ###################################
TFile *f3 = new TFile("./MuonMC_dEdXPlot.root");

// #######################################
// ### Load Electron Monte Carlo Plots ###
// #######################################
TFile *f4 = new TFile("./ElectronMC_dEdXPlot.root");


std::cout<<"Loaded files"<<std::endl;

//--------------------------------------------------------------------------------------------------------------
//					dE/dX Plot
//--------------------------------------------------------------------------------------------------------------

// ###################################
// ### Getting the data dE/dX plot ###
// ###################################
TH1F *hDatadEdXPlot = (TH1F*)f1->Get("hRecoDepositedE");

// ### Labeling the axis ###
hDatadEdXPlot->GetXaxis()->SetTitle("Deposited Energy (MeV)");
hDatadEdXPlot->GetXaxis()->CenterTitle();

hDatadEdXPlot->GetYaxis()->SetTitle("Entries / 0.5 (MeV)");
hDatadEdXPlot->GetYaxis()->CenterTitle(); 

std::cout<<"Loaded Data Plot"<<std::endl;

std::cout<<std::endl;
   

// ######################################
// ### Getting the Pion MC dE/dX plot ###
// ######################################
TH1F *hPiondEdX = (TH1F*)f2->Get("hRecoDepositedE");

// ### Labeling the axis ###
hPiondEdX->GetXaxis()->SetTitle("Deposited Energy (MeV)");
hPiondEdX->GetXaxis()->CenterTitle();

hPiondEdX->GetYaxis()->SetTitle("Entries / 0.50 (MeV)");
hPiondEdX->GetYaxis()->CenterTitle(); 

std::cout<<"Loaded Pion MC Plot"<<std::endl;

// == Scale Pions ===
hPiondEdX->Sumw2();
hPiondEdX->Scale(PionPercentage);

int pionNumber = hPiondEdX->Integral();
std::cout<<"# of Pion = "<<pionNumber<<std::endl;



// ######################################
// ### Getting the Muon MC dE/dX plot ###
// ######################################
TH1F *hMuonMCdEdX = (TH1F*)f3->Get("hRecoDepositedE");

// ### Labeling the axis ###
hMuonMCdEdX->GetXaxis()->SetTitle("Depositied Energy (MeV)");
hMuonMCdEdX->GetXaxis()->CenterTitle();

hMuonMCdEdX->GetYaxis()->SetTitle("Entries / 0.50 (MeV)");
hMuonMCdEdX->GetYaxis()->CenterTitle(); 

std::cout<<"Loaded Muon MC Plot"<<std::endl;

// == Scale Muons ===
hMuonMCdEdX->Sumw2();
hMuonMCdEdX->Scale(MuonPercentage);
int muonNumber = hMuonMCdEdX->Integral();
std::cout<<"# of Muon = "<<muonNumber<<std::endl;



// ##########################################
// ### Getting the Electron MC dE/dX plot ###
// ##########################################
TH1F *hElectronMCdEdX = (TH1F*)f4->Get("hRecoDepositedE");

// ### Labeling the axis ###
hElectronMCdEdX->GetXaxis()->SetTitle("dE/dX (MeV/cm)");
hElectronMCdEdX->GetXaxis()->CenterTitle();

hElectronMCdEdX->GetYaxis()->SetTitle("Events / 0.25 (MeV/cm)");
hElectronMCdEdX->GetYaxis()->CenterTitle(); 

std::cout<<"Loaded Muon MC Plot"<<std::endl;

// == Scale Electron ===
hElectronMCdEdX->Sumw2();
hElectronMCdEdX->Scale(ElectronPercentage);
std::cout<<"# of Electron = "<<hElectronMCdEdX->Integral()<<std::endl;



// ============================================================================
// ======================= Normalizing MC to Data =============================
// ============================================================================

double PionMCIntegraldEdX     = hPiondEdX->Integral() ;
double MuonMCIntegraldEdX     = hMuonMCdEdX->Integral() ;
double ElectronMCIntegraldEdX = hElectronMCdEdX->Integral() ;



// ### Overall MC scale factor ###
double MCIntegralTrkLength = PionMCIntegraldEdX + MuonMCIntegraldEdX + ElectronMCIntegraldEdX ;
double DataIntegralTrkLength = hDatadEdXPlot->Integral();

double scaleMCdEdX = DataIntegralTrkLength/MCIntegralTrkLength;

hPiondEdX->Scale(scaleMCdEdX);
hMuonMCdEdX->Scale(scaleMCdEdX);
hElectronMCdEdX->Scale(scaleMCdEdX);



int dataNum = hDatadEdXPlot->Integral();
std::cout<<"# of data events = "<<dataNum<<std::endl;


// ########################
// ### Making a TCanvas ###
// ########################
TCanvas *c09 = new TCanvas("c09", "Track Pitch");
c09->SetTicks();
c09->SetFillColor(kWhite);


hPiondEdX->SetLineColor(kBlue);
hPiondEdX->SetLineStyle(0);
hPiondEdX->SetLineWidth(3);
hPiondEdX->SetFillColor(kBlue);
hPiondEdX->SetFillStyle(3006);

hElectronMCdEdX->SetLineColor(kRed);
hElectronMCdEdX->SetLineStyle(0);
hElectronMCdEdX->SetLineWidth(3);
hElectronMCdEdX->SetFillColor(kRed);
hElectronMCdEdX->SetFillStyle(3006);

hMuonMCdEdX->SetLineColor(kGreen+3);
hMuonMCdEdX->SetLineStyle(0);
hMuonMCdEdX->SetLineWidth(3);
hMuonMCdEdX->SetFillColor(kGreen+3);
hMuonMCdEdX->SetFillStyle(3006);


hDatadEdXPlot->SetLineColor(kBlack);
hDatadEdXPlot->SetLineStyle(0);
hDatadEdXPlot->SetLineWidth(3);
hDatadEdXPlot->SetMarkerStyle(8);
hDatadEdXPlot->SetMarkerSize(0.9);


// ### Making a stacked histogram ###
THStack *hstacked = new THStack("hstacked","Stacked 1D histograms");

// ### Labeling the axis ###
//hstacked->GetXaxis()->SetTitle("Track Length (cm)");
//hstacked->GetXaxis()->CenterTitle();

//hstacked->GetYaxis()->SetTitle("Events / 0.5 cm");
//hstacked->GetYaxis()->CenterTitle(); 

hstacked->Add(hMuonMCdEdX);
hstacked->Add(hElectronMCdEdX);
hstacked->Add(hPiondEdX);

// ### Drawing the histograms ###
hstacked->Draw("histo");
hDatadEdXPlot->Draw("E1same");


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
leg->AddEntry(hDatadEdXPlot,"Data");
leg->AddEntry(hPiondEdX,"Pion MC"); 
leg->AddEntry(hMuonMCdEdX,"Muon MC");
leg->AddEntry(hElectronMCdEdX,"Electron MC");
leg->Draw();




}//<---End File
