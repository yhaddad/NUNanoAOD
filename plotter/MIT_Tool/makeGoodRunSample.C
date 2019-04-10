#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TSystem.h>
#include <TString.h>
#include <TH1D.h>
#include <TH2D.h>
#include <TMath.h>
#include <set>
#include <fstream>
#include <stdexcept>
#include <string>
#include <cstdlib>
#include <iostream>

#include "MitAna/DataCont/interface/RunLumiRangeMap.h"

typedef std::map<ULong64_t, std::set<ULong64_t> > EventList;

EventList
readEventList(char const* _fileName)
{
  EventList list;
  ifstream listFile(_fileName);
  if (!listFile.is_open())
    throw std::runtime_error(_fileName);

  unsigned iL(0);
  std::string line;
  while (true) {
    std::getline(listFile, line);
    if (!listFile.good())
      break;
    
    if (line.find(":") == std::string::npos || line.find(":") == line.rfind(":"))
      continue;

    unsigned run(std::atoi(line.substr(0, line.find(":")).c_str()));
    unsigned event(std::atoi(line.substr(line.rfind(":") + 1).c_str()));

    list[run].insert(event);

    ++iL;
  }

  std::cout << "Loaded " << iL << " events" << std::endl;

  return list;
}

void makeGoodRunSample(
 TString input_file     = "nero_old.root",
 TString outputFileName = "nero_new.root",
 string jsonFile        = "/home/ceballos/cms/cmssw/046/CMSSW_8_0_26_patch1/src/MitAnalysisRunII/json/80x/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
 ){

  mithep::RunLumiRangeMap rlrm;
  rlrm.AddJSONFile(jsonFile.c_str()); 

  TString runName = "run";
  TString eventName = "event";
  TString lumiName = "luminosityBlock";
  TString treeName = "Events";

  TFile *the_input_file = TFile::Open(input_file.Data());
  TTree *the_input_tree = (TTree*)the_input_file->FindObjectAny(treeName.Data());
  int run,lumi;
  ULong64_t event;

  the_input_tree->SetBranchAddress(runName.Data(),&run);
  the_input_tree->SetBranchAddress(lumiName.Data(),&lumi);
  the_input_tree->SetBranchAddress(eventName.Data(),&event);
 
  ULong64_t N_all  = the_input_tree->GetEntries();
  ULong64_t N_good = 0;

  TFile *outputFile = new TFile(outputFileName.Data(), "RECREATE");
  outputFile->cd();
  TTree *normalizedTree = the_input_tree->CloneTree(0);

  //dubplicate check
  std::map<ULong64_t, std::set<ULong64_t> > DoubleChecker;
  ULong64_t doubleCount = 0;
  
  for (int i=0; i<the_input_tree->GetEntries(); ++i) {
    the_input_tree->GetEntry(i);
    if(i%100000==0) printf("event %d out of %d\n",i,(int)the_input_tree->GetEntries());

    //------------------------------
    // check if double counting //Remove for MC
    //------------------------------
    Bool_t DuplicateEvent = kFALSE;
    std::map<ULong64_t, std::set<ULong64_t> >::iterator runner = DoubleChecker.find(run);
    if (runner == DoubleChecker.end()){
      std::set<ULong64_t> evtTemp;
      evtTemp.insert(run);
      DoubleChecker.insert( make_pair(run, evtTemp));
    }
    else{
      std::set<ULong64_t>::iterator evter = (*runner).second.find(event);
      if (evter == (*runner).second.end()){
        (*runner).second.insert(event);
      }
      else { DuplicateEvent = kTRUE;
      }
    }
    if(DuplicateEvent) doubleCount++;
    if(DuplicateEvent) continue;

    mithep::RunLumiRangeMap::RunLumiPairType rl(run, lumi);      

    if(!rlrm.HasRunLumi(rl)) continue;

    N_good++;
    normalizedTree->Fill(); 
  }
  printf("N good/all = %llu / %llu = %f | duplicates: %llu\n",N_good,N_all-doubleCount,(double)N_good/(N_all-doubleCount),doubleCount);
  normalizedTree->Write();
  outputFile->Close();
}
