# Meta-graphs
The output folder for meta-graphs from `generate_full_MetaShift.py` 

<p align='center'>
  <img width='100%' src='../../docs/figures/Cat-MetaGraph.jpg'/>
<b>Figure: Meta-graph: visualizing the diverse data distributions within the “cat” class.  </b> 
MetaShift splits the data points of each class (e.g., Cat) into many subsets based on visual contexts. 
Each node in the meta-graph represents one subset. The weight of each edge is the overlap coefficient between the corresponding two subsets. Node colors indicate the graph-based community detection results. Inter-community edges are colored. Intra-community edges are grayed out for better visualization. The border color of each example image indicates its community in the meta-graph. We have one such meta-graph for each of the 410 classes in the MetaShift.
</p>


<p align='center'>
  <img width='100%' src='../../docs/figures/Dog-MetaGraph.jpg'/>
<b>Figure: Meta-graph for the “Dog” class, which captures meaningful semantics of the multi-modal data distribution of “Dog”. </b> 
</p>