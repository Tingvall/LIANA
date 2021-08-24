params{
  // General parameters
  bed2D = false
  peaks = false
  genome = false
  genes = "No genes"
  bed2D_anno = false
  mode = "basic" //basic, multiple, differntial
  outdir = "$baseDir/result"
  prefix = "PLACseq"
  proximity_unannotated = false
  multiple_anno = "concentrate"  //keep, concentrate, qvalue
  skip_anno = false
  annotate_interactions = false
  network = false
  network_mode = "factor" //Options: all (for all plac-seq interactions), factor (default, for all interactions have factor binding in at least on anchor point) or genes (show only interactions realted to specified gene list). If run in differntial mode, the option differential is also available (simialr to factor but  only differntial peaks (specified by log2FC/padj) are included. Use expression for filtering on differntial expression (no need to specify gene.) )
  use_peakscore = false
  complete = false
  save_tmp = false
  help = false

  // Multiple mode specific
  upset_plot = false
  circos_plot = false
  filter_genes = false

  // Differntial mode specific
  peak_differential="No differntial peak"
  log2FC_column=3
  padj_column=9
  log2FC=1.5
  padj=0.05
  expression="No expression"
  skip_expression=false
  expression_padj_column=9
  expression_log2FC_column=3
  expression_padj=0.05
  expression_log2FC=1.5
}
