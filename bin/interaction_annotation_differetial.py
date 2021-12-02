#!/usr/bin/env python

### PROCESS 9 BASIC: INTERACTION CENTERED ANNOTATION - WITH PEAK OVERLAP ###
import pandas as pd
import numpy as np
import argparse

# PARSE ARGUMENTS
Description = 'INTERACTION-CENTERED ANNOTATION WITH PEAK OVERLAP IN BASIC MODE'
Epilog = """Example usage: interaction_annotation_basic.py <ANCHOR1_PEAK> <ANCHOR2_PEAK> <BED2D> --prefix <PREFIX> --sample <SAMPLE>"""

argParser = argparse.ArgumentParser(description=Description, epilog=Epilog)

# General arguments
argParser.add_argument('ANCHOR1_PEAK', help="Annotated anchor1 regions with peak overlap.")
argParser.add_argument('ANCHOR2_PEAK', help="Annotated anchor2 regions with peak overlap.")
argParser.add_argument('BED2D', help="2D-bed interactions.")
argParser.add_argument('--prefix', dest="PREFIX", help="Prefix for output file.")
argParser.add_argument('--sample', dest="SAMPLE", help="Name of sample.")
argParser.add_argument('--network', dest="NETWORK", help="Specifies if files for network visualization in Cytoscape should be created." , choices=['true', 'false'])
argParser.add_argument('--complete', dest="COMPLETE", help="If set to true, all available processes for the selected mode and provided inputs are run.", choices=['true', 'false'])

# Multiple mode specific arguments
argParser.add_argument('--upset_plot', dest="UPSET_PLOT", help="Specifies if Upset plot of peak overlap will be created.", choices=['true', 'false'])
argParser.add_argument('--circos_plot', dest="CIRCOS_PLOT", help="Specifies if Circos plot of peak overlap will be created.", choices=['true', 'false'])

args = argParser.parse_args()

# DEFINE FUNCTION
def interaction_annotation_basic(anchor_1_peak_collect, anchor_2_peak_collect, bed2D_index_anno, prefix, sample, network, complete, upset_plot, circos_plot):

    # Column names for loaded data
    anchor1_peak_name = ('Anchor1_Chr', 'Anchor1_Start', 'Anchor1_End', 'Peak1', 'Peak1_Chr', 'Peak1_Start', 'Peak1_End', 'Peak1_ID', 'Peak1_score')
    anchor2_peak_name = ('Anchor2_Chr', 'Anchor2_Start', 'Anchor2_End', 'Peak2', 'Peak2_Chr', 'Peak2_Start', 'Peak2_End', 'Peak2_ID', 'Peak2_score')

    # Load interaction centered peak overlaps 2and annotated 2D-bed
    anchor1_peaks = pd.read_table(anchor_1_peak_collect, index_col=3,names=anchor1_peak_name).sort_index()
    anchor2_peaks = pd.read_table(anchor_2_peak_collect, index_col=3,names=anchor2_peak_name).sort_index()
    bed2D_anno = pd.read_table(bed2D_index_anno, index_col=1).sort_index().iloc[:,1:]

    # Create Peak columns (chr:start-end) for anchor 1 & 2
    anchor1_peaks["Peak1_ID"] = anchor1_peaks["Peak1_Chr"].map(str) +':'+ (anchor1_peaks["Peak1_Start"]-1).map(str) +'-'+ anchor1_peaks["Peak1_End"].map(str)
    anchor2_peaks["Peak2_ID"] = anchor2_peaks["Peak2_Chr"].map(str) +':'+ (anchor2_peaks["Peak2_Start"]-1).map(str) +'-'+ anchor2_peaks["Peak2_End"].map(str)

    # Merging anchor points
    anchor1_peaks_anno =bed2D_anno.loc[:,['chr1', 's1','e1' ,'Entrez_ID_1', 'Gene_Name_1']].merge(anchor1_peaks.loc[:,['Peak1','Peak1_ID', 'Peak1_score']], left_index=True, right_index=True, how = 'left')
    anchor2_peaks_anno =bed2D_anno.loc[:,['chr2', 's2','e2' ,'Entrez_ID_2', 'Gene_Name_2','Q-Value_Bias','TSS_1', 'TSS_2']].merge(anchor2_peaks.loc[:,['Peak2','Peak2_ID', 'Peak2_score']], left_index=True, right_index=True, how = 'left')
    anchors_peaks_anno = anchor1_peaks_anno.merge(anchor2_peaks_anno, left_index=True, right_index=True,how = 'outer').drop_duplicates()

    # Creation and use of function for adding 2 columns for each factor (overlap in anchor 1/2) with 1 if overlap
    def peak_in_anchor_1(row):
      if row['Peak1'] == f :
        return 1
      else:
        return ''
    def peak_in_anchor_2(row):
      if row['Peak2'] == f :
        return 1
      else:
        return ''

    factor = pd.unique(anchors_peaks_anno[['Peak1', 'Peak2']].dropna().values.ravel('K'))

    for f in factor:
        anchors_peaks_anno[f + '_1'] = anchors_peaks_anno.apply (lambda row: peak_in_anchor_1(row), axis=1)
    for f in factor:
        anchors_peaks_anno[f + '_2'] = anchors_peaks_anno.apply (lambda row: peak_in_anchor_2(row), axis=1)

    anchors_peaks_anno.index.name = 'Interaction'
    anchors_peaks_anno_original = anchors_peaks_anno.copy(deep=True)

    # Creating dictionary with each factors as a key and associated df with interactions with factor overlap in at least one anchor point
    factor_dict={}
    for f in factor:
        factor_dict[f] = anchors_peaks_anno[(anchors_peaks_anno['Peak1'] == f) | (anchors_peaks_anno['Peak2'] == f)]
        factor_dict[f].loc[factor_dict[f].Peak1 !=f,['Peak1', 'Peak1_ID', 'Peak1_score']] = ''
        factor_dict[f].loc[factor_dict[f].Peak2 !=f,['Peak2', 'Peak2_ID', 'Peak2_score']] = ''
        factor_dict[f] = factor_dict[f].groupby('Interaction').agg(lambda x: ', '.join(filter(None, list(x.unique().astype(str)))))

    anchors_peaks_anno = anchors_peaks_anno.groupby('Interaction').agg(lambda x: ', '.join(filter(None, list(x.unique().astype(str)))))

    # Saving annotated interactions files (all interaction and interactions with peak overlap)
    for f in factor:
        factor_dict[f].to_csv(str(f) + '_' + prefix + '_interactions.txt', index=False, sep='\t' )
    anchors_peaks_anno.to_csv(prefix + '_HOMER_annotated_interactions_with_peak_overlap.txt', index=True, sep='\t' )

    # Save files for Network
    if (network == 'true' or complete == 'true' or plot_upset =='true' or circos_plot =='true'):
      anchors_peaks_anno_original.to_csv(prefix + '_HOMER_annotated_interactions_with_peak_overlap_not_aggregated.txt', index=True, sep='\t' )


# RUN FUNCTION
interaction_annotation_basic(anchor_1_peak_collect=args.ANCHOR1_PEAK,anchor_2_peak_collect=args.ANCHOR2_PEAK,bed2D_index_anno=args.BED2D, prefix=args.PREFIX, sample=args.SAMPLE, network=args.NETWORK, complete=args.COMPLETE, upset_plot=args.UPSET_PLOT, circos_plot=args.CIRCOS_PLOT)

