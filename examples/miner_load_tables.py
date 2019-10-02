'''
file : miner_load_tables.py
author : Agrim Gupta
edited by : Farzaan Kaiyom

Example to illustrate how to load the miner dataset into a multi-modal network. 

Usage: miner_load_tables.py <config_file>

Positional Arguments:
config_file  : Path to the config file. The config file contatins the path to all the modes and cross-net tsv files.

Optional Arguments: 
--output_dir : Directory to create output files. Defaults to the current working directory.
--loglevel   : Enable logging. Defaults to warning level. 

Example Usage: 
Input File   : Config.txt

Command Line : 
python miner_load_tables.py config.txt --loglevel info 

Output: 
miner.graph
'''

import sys
sys.path.insert(0, './../../swig/')
import snap
import ConfigParser
import argparse
import logging
import os

parser = argparse.ArgumentParser(description='Generate a Multi-Modal Network')
parser.add_argument('config_file', help='path of a config file.')
parser.add_argument('--output_dir', help='output path to save the Multi-Modal Network', default='.')
parser.add_argument('--loglevel', help='info for debug print.')
parser.add_argument('--outputf', help='output file name.', default='miner.graph')
args = parser.parse_args()
config = ConfigParser.ConfigParser()
config.readfp(open(args.config_file))
if args.loglevel:
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    logging.basicConfig(level=numeric_level)

context = snap.TTableContext()
# Construct the graph
logging.info('Building Multi-Modal Network')
Graph = snap.TMMNet.New()

# Loading Modes
try:
    chemical_mode_file = config.get('Modes', 'Chemical')
    cmschema = snap.Schema()
    cmschema.Add(snap.TStrTAttrPr("ChemicalId", snap.atStr))
    cmschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    chemical_mode = snap.TTable.LoadSS(cmschema, chemical_mode_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Chemical Mode')
    snap.LoadModeNetToNet(Graph, "Chemical", chemical_mode, "ChemicalId", snap.TStr64V())
except ConfigParser.NoOptionError: 
    logging.info('Skipping Chemical Mode')

try:
    function_mode_file = config.get('Modes', 'Function')
    fmschema = snap.Schema()
    fmschema.Add(snap.TStrTAttrPr("FunctionId", snap.atStr))
    fmschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    function_mode = snap.TTable.LoadSS(fmschema, function_mode_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Function Mode')
    snap.LoadModeNetToNet(Graph, "Function", function_mode, "FunctionId", snap.TStr64V())
except ConfigParser.NoOptionError:
    logging.info('Skipping Function Mode')

try:
    gene_mode_file = config.get('Modes', 'Gene')
    gmschema = snap.Schema()
    gmschema.Add(snap.TStrTAttrPr("GeneId", snap.atStr))
    gmschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    gene_mode = snap.TTable.LoadSS(gmschema, gene_mode_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Gene Mode')
    snap.LoadModeNetToNet(Graph, "Gene", gene_mode, "GeneId", snap.T64StrV())
except ConfigParser.NoOptionError:
    logging.info('Skipping Gene Mode')

try:
    protein_mode_file = config.get('Modes', 'Protein')
    pmschema = snap.Schema()
    pmschema.Add(snap.TStrTAttrPr("ProteinId", snap.atStr))
    pmschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    protein_mode = snap.TTable.LoadSS(pmschema, protein_mode_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Protein Mode')
    snap.LoadModeNetToNet(Graph, "Protein", protein_mode, "ProteinId", snap.TStr64V())
except ConfigParser.NoOptionError:
    logging.info('Skipping Protein Mode')

try:
    disease_mode_file = config.get('Modes', 'Disease')
    dmschema = snap.Schema()
    dmschema.Add(snap.TStrTAttrPr("DiseaseId", snap.atStr))
    dmschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    disease_mode = snap.TTable.LoadSS(dmschema, disease_mode_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Disease Mode')
    snap.LoadModeNetToNet(Graph, "Disease", disease_mode, "DiseaseId", snap.TStr64V())
except ConfigParser.NoOptionError:
    logging.info('Skipping Disease Mode')

# Loading Cross-Nets
try:
    chemical_chemical_crossnet_file = config.get('Cross-Net', 'Chemical-Chemical')
    cccschema = snap.Schema()
    cccschema.Add(snap.TStrTAttrPr("CCEdgeId", snap.atStr))
    cccschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    cccschema.Add(snap.TStrTAttrPr("CSrcId", snap.atStr))
    cccschema.Add(snap.TStrTAttrPr("CDstId", snap.atStr))
    cccschema.Add(snap.TStrTAttrPr("desc", snap.atStr))
    chemical_chemical_crossnet = snap.TTable.LoadSS(cccschema, chemical_chemical_crossnet_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Chemical-Chemical Cross-Net')
    snap.LoadCrossNetToNet(Graph, "Chemical", "Chemical", "Chemical-Chemical", chemical_chemical_crossnet, "CSrcId", "CDstId", snap.TStr64V())
except ConfigParser.NoOptionError:
    logging.info('Skipping Chemical-Chemical Cross-Net')

try:
    chemical_gene_crossnet_file = config.get('Cross-Net', 'Chemical-Gene')
    cgcschema = snap.Schema()
    cgcschema.Add(snap.TStrTAttrPr("CGEdgeId", snap.atStr))
    cgcschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    cgcschema.Add(snap.TStrTAttrPr("CSrcId", snap.atStr))
    cgcschema.Add(snap.TStrTAttrPr("GDstId", snap.atStr))
    chemical_gene_crossnet = snap.TTable.LoadSS(cgcschema, chemical_gene_crossnet_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Chemical-Gene Cross-Net')
    snap.LoadCrossNetToNet(Graph, "Chemical", "Gene", "Chemical-Gene", chemical_gene_crossnet, "CSrcId", "GDstId", snap.TStr64V())
except ConfigParser.NoOptionError:
    logging.info('Skipping Chemical-Gene Cross-Net')

try:
    function_function_crossnet_file = config.get('Cross-Net', 'Function-Function')
    ffcschema = snap.Schema()
    ffcschema.Add(snap.TStrTAttrPr("FFEdgeId", snap.atStr))
    ffcschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    ffcschema.Add(snap.TStrTAttrPr("FSrcId", snap.atStr))
    ffcschema.Add(snap.TStrTAttrPr("FDstId", snap.atStr))
    function_function_crossnet = snap.TTable.LoadSS(ffcschema, function_function_crossnet_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Function-Function Cross-Net')
    snap.LoadCrossNetToNet(Graph, "Function", "Function", "Function-Function", function_function_crossnet, "FSrcId", "FDstId", snap.TStr64V())
except ConfigParser.NoOptionError:
    logging.info('Skipping Function-Function Cross-Net')

try:
    gene_function_crossnet_file = config.get('Cross-Net', 'Gene-Function')
    gfcschema = snap.Schema()
    gfcschema.Add(snap.TStrTAttrPr("GFEdgeId", snap.atStr))
    gfcschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    gfcschema.Add(snap.TStrTAttrPr("GSrcId", snap.atStr))
    gfcschema.Add(snap.TStrTAttrPr("FDstId", snap.atStr))
    gene_function_crossnet = snap.TTable.LoadSS(gfcschema, gene_function_crossnet_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Gene-Function Cross-Net')
    snap.LoadCrossNetToNet(Graph, "Gene", "Function", "Gene-Function", gene_function_crossnet, "GSrcId", "FDstId", snap.TStr64V())
except ConfigParser.NoOptionError:
    logging.info('Skipping Gene-Function Cross-Net')

try:
    gene_protein_crossnet_file = config.get('Cross-Net', 'Gene-Protein')
    gpcschema = snap.Schema()
    gpcschema.Add(snap.TStrTAttrPr("GPEdgeId", snap.atStr))
    gpcschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    gpcschema.Add(snap.TStrTAttrPr("GSrcId", snap.atStr))
    gpcschema.Add(snap.TStrTAttrPr("PDstId", snap.atStr))
    gene_protein_crossnet = snap.TTable.LoadSS(gpcschema, gene_protein_crossnet_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Gene-Protein Cross-Net')
    snap.LoadCrossNetToNet(Graph, "Gene", "Protein", "Gene-Protein", gene_protein_crossnet, "GSrcId", "PDstId", snap.TStr64V())
except ConfigParser.NoOptionError:
    logging.info('Skipping Gene-Protein Cross-Net')
try:
    protein_protein_crossnet_file = config.get('Cross-Net', 'Protein-Protein')
    ppcschema = snap.Schema()
    ppcschema.Add(snap.TStrTAttrPr("PPEdgeId", snap.atStr))
    ppcschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    ppcschema.Add(snap.TStrTAttrPr("PSrcId", snap.atStr))
    ppcschema.Add(snap.TStrTAttrPr("PDstId", snap.atStr))
    protein_protein_crossnet = snap.TTable.LoadSS(ppcschema, protein_protein_crossnet_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Protein-Protein Cross-Net')
    snap.LoadCrossNetToNet(Graph, "Protein", "Protein", "Protein-Protein", protein_protein_crossnet, "PSrcId", "PDstId", snap.TStr64V())
except ConfigParser.NoOptionError:
    logging.info('Skipping Protein-Protein Cross-Net')
try:
    disease_disease_crossnet_file = config.get('Cross-Net', 'Disease-Disease')
    ddcschema = snap.Schema()
    ddcschema.Add(snap.TStrTAttrPr("DDEdgeId", snap.atStr))
    ddcschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    ddcschema.Add(snap.TStrTAttrPr("DSrcId", snap.atStr))
    ddcschema.Add(snap.TStrTAttrPr("DDstId", snap.atStr))
    disease_disease_crossnet = snap.TTable.LoadSS(ddcschema, disease_disease_crossnet_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Disease-Disease Cross-Net')
    snap.LoadCrossNetToNet(Graph, "Disease", "Disease", "Disease-Disease", disease_disease_crossnet, "DSrcId", "DDstId", snap.TStr64V())
except ConfigParser.NoOptionError:
    logging.info('Skipping Disease-Disease Cross-Net')

try:
    disease_gene_crossnet_file = config.get('Cross-Net', 'Disease-Gene')
    dgcschema = snap.Schema()
    dgcschema.Add(snap.TStrTAttrPr("DGEdgeId", snap.atStr))
    dgcschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    dgcschema.Add(snap.TStrTAttrPr("DSrcId", snap.atStr))
    dgcschema.Add(snap.TStrTAttrPr("GDstId", snap.atStr))
    disease_gene_crossnet = snap.TTable.LoadSS(dgcschema, disease_gene_crossnet_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Disease-Gene Cross-Net')
    snap.LoadCrossNetToNet(Graph, "Disease", "Gene", "Disease-Gene", disease_gene_crossnet, "DSrcId", "GDstId", snap.TStr64V())
except ConfigParser.NoOptionError:
    logging.info('Skipping Disease-Gene Cross-Net')

try:
    disease_function_crossnet_file = config.get('Cross-Net', 'Disease-Function')
    dfcschema = snap.Schema()
    dfcschema.Add(snap.TStrTAttrPr("DFEdgeId", snap.atStr))
    dfcschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    dfcschema.Add(snap.TStrTAttrPr("DSrcId", snap.atStr))
    dfcschema.Add(snap.TStrTAttrPr("FDstId", snap.atStr))
    disease_function_crossnet = snap.TTable.LoadSS(dfcschema, disease_function_crossnet_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Disease-Function Cross-Net')
    snap.LoadCrossNetToNet(Graph, "Disease", "Function", "Disease-Function", disease_function_crossnet, "DSrcId", "FDstId", snap.TStr64V())
except ConfigParser.NoOptionError:
    logging.info('Skipping Disease-Function Cross-Net')

try:
    disease_chemical_crossnet_file = config.get('Cross-Net', 'Disease-Chemical')
    dccschema = snap.Schema()
    dccschema.Add(snap.TStrTAttrPr("DCEdgeId", snap.atStr))
    dccschema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    dccschema.Add(snap.TStrTAttrPr("DSrcId", snap.atStr))
    dccschema.Add(snap.TStrTAttrPr("CDstId", snap.atStr))
    disease_chemical_crossnet = snap.TTable.LoadSS(dccschema, disease_chemical_crossnet_file, context, "\t", snap.TBool(False))
    logging.info('Done loading Disease-Chemical Cross-Net')
    snap.LoadCrossNetToNet(Graph, "Disease", "Chemical", "Disease-Chemical", disease_chemical_crossnet, "DSrcId", "CDstId", snap.TStr64V())
except ConfigParser.NoOptionError:
    logging.info('Skipping Disease-Chemical Cross-Net')

# Save the graph
logging.info('Saving Multi-Modal Network to disk')
outputPath = os.path.join(args.output_dir, args.outputf)
FOut = snap.TFOut(outputPath)
Graph.Save(FOut)
FOut.Flush()
