import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *

finalMuons = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag("slimmedMuons"),
    cut = cms.string("pt > 5 && track.isNonnull && (isGlobalMuon || isTrackerMuon) && isPFMuon")
)

muonTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("linkedObjects","muons"),
    cut = cms.string(""), #we should not filter on cross linked collections
    name = cms.string("Muon"),
    doc  = cms.string("slimmedMuons after basic selection (" + finalMuons.cut.value()+")"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the muons
    variables = cms.PSet(CandVars,
        dxy   = Var("dB", float, doc = "dxy wrt first PV, in cm"),
        ptErr   = Var("bestTrack().ptError()", float, doc = "ptError of the muon track", precision=6),
        segmentComp   = Var("segmentCompatibility()", float, doc = "ptError of the muon track", precision=6),
        nStations = Var("numberOfMatchedStations", int, doc = "number of matched stations with default arbitration (segment & track)"),
        jet = Var("?hasUserCand('jet')?userCand('jet').key():-1", int, doc="index of the associated jet (-1 if none)"),
        mediumId = Var("isPFMuon && innerTrack.validFraction >= 0.49 && ( isGlobalMuon && globalTrack.normalizedChi2 < 3 && combinedQuality.chi2LocalPosition < 12 && combinedQuality.trkKink < 20 && segmentCompatibility >= 0.303 || segmentCompatibility >= 0.451 )", bool, doc = "POG Medium muon ID (2016 tune)"),
    ),
)


muonSequence = cms.Sequence(finalMuons)
muonTables = cms.Sequence ( muonTable)

