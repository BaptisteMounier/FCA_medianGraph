# FCA_medianGraph
## Datas sets
* Default sets
  * cla_v1: example in cla
  * cla_v2: example in cla with one additionnal n5 on the common axe
  * cla_v3: two examples of cla side by side with one axe and top
  * cla_v4: two examples of cla side by side since contact
  * cla_v5: four examples of cla side by side since contact
  * And many more
* Format
  * 1st line for the labels of attributes
  * Use '' or '0' for blank and anything other for value

## Results
* Default
  * Do a serie of analyse (located in '/data/')
  * Uncomment and edit line 40 in 'main.py' to analyse one by one (source file aren't the same, in case of modification but forget to edit both)
* Graphs
  * .pdf and .gv
  * in '/data/graph/'
* Context
  * In the console at each stage
* Nomenclature
  * 'dataSetName_ext'
    * 'dataSetName': it's the name of the model likes 'cla_v1', 'cla_v2', etc
    * 'ext': it's the operation done on the data set
      * We can do multiple operation, lastest operation at the end of the name
      * 'd': distributivity on the whole lattice
      * 'df': distributivity on each first filter
      * 'df_preMerge': lattice before the merge (distributivity already done)
      * 'df_step1': first iteration of merge after distributivity
      * 'o4': lattice of the first filter 'o4'

# Reporting
## Done
* Take a unknow context
  * Create the graph (with Graphviz)
* Convert it into a standard context
* Convert it into a distributive context
  * ?
* Create distributive first filters context from global strandard one
  * Use cla2018 algorithm to convert contexts of first filters into distributives contexts
  * Merge result basically (local result of cla2018)
  * Merge similar nodes (optimal result of cla2018)
## To do
* Enable export for Latviz and others main graphs generators applications
* Create GUI
## Problems