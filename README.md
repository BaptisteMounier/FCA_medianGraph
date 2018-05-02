# FCA_medianGraph
## Datas sets
* cla_v1: example in cla
* cla_v2: example in cla with one additionnal n5 on the commun axe
* cla_v3: two examples of cla side by side

## Results
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
* Need to verify merge method on lattice with cross-connections (like crown)
* Enable export for Latviz and others main graphs generators applications
* Create GUI
## Problems
* Can be a problem with lattice with cross-connections (like crown)