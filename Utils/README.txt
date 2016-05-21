This directory creates generic scripts than can be used to create snap-formatted tsvs for modes
and crossnets. This directory currently consists of three files:

1. create_snap_mode_table.py
	Input:    - original dataset, in tsv form
	Output:   - Snap mode table tsv (snap_nid\tdataset_id)
	          - dataset specific mode snap table tsv (snap_nid\tdataset_entity_id)
2. create_snap_crossnet_table.py
	Input:    - Source dataset specific snap mode table tsv
	          - Destination dataset specific snap mode table tsv
	          - the dataset (in tsv form) specifying edges.
	Output:   - Snap crossnet table tsv (snap_eid\tdataset_id\tsnap_src_nid\tsnap_dst_nid) 
	          - he dataset specific snap table tsv (snap_eid\tsrc_dataset_id\tdst_dataset_id)
3. create_snap_mode_equiv_table.py
	Input:    - First dataset specific snap mode table tsv
	          - Second dataset specific snap mode table tsv
	          - (Optional) the dataset (in tsv form) specifying id equivalences
	Output:   - Snap mode equivlance table (snap_nid\tsnap_nid)


It also contains scripts to pull out unique node ids and create an edge list (i.e. remove 
extraneous fields):

4. extract_unique_node_ids.py
	Description: Extracts node ids from a tsv and writes all the unique ids to a tsv.
	Input:    - dataset, in tsv form
	Output:   - tsv, where each line contains a single node id
5. extract_edge_list.py 
	Description: Extracts src and dst node ids from a file, creates a tsv edge list. Can process
	             1-to-1, 1-to-many, many-to-1, and many-to-many relationships in input file.
	Input:    - dataset, in tsv form
	Output:   - tsv, where each line contains the source node id and the destination node id.


Below are details on the arguments and usage for each script (taken from the header of each file):


########################################
###     create_snap_mode_table.py    ###
########################################

Script that creates snap tables for a given mode.

Usage:
python create_snap_mode_table.py <input_file_path> <mode_name> <dataset_name> <dataset_id>

Positional Arguments:
input_file_path:         Path to the input file; Input file should be a tsv.
mode_name:               Name of the mode being created e.g. genes
dataset_name:            Name of dataset being used to create the snap mode tables i.e. the 
                         dataset the input file comes from. e.g. STRING
dataset_id:              unique integer id for this dataset.


Optional arguments:
--node_index:            If there are multiple columns in the input tsv, the index of the column with the node id.
                         Defaults to 0.
--output_dir:            Directory to create output files. Defaults to the current working directory.
--full_mode_file:        Name of output file tsv containing a list of <snap_id>\t<dataset_id>.
                         Defaults to output_dir/miner-<mode_name>-<date>.tsv
--db_node_file:          Name of output file tsv for a specific dataset; contains a list of <snap id>\t<dataset_specific_entity_id>
                         Defaults to output_dir/miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv
--snap_id_counter_start  Start assigning snap ids from this integer value; this number MUST be greater
                         than any id found in the full mode file.

Example usage:
Creating files for genes using two datasets, GeneOntology and HUGO:

Input files: hugo.tsv and go.tsv

Output directory: outputs/genes/

Output files: miner-gene-20160520.tsv, miner-gene-0-GO-20160520.tsv, miner-gene-1-HUGO-20160520.tsv

Workflow:

python create_snap_mode_table.py go.tsv gene GO 0 --output_dir outputs/genes/
python create_snap_mode_table.py hugo.tsv gene HUGO 1 --output_dir outputs/genes/


############################################
###     create_snap_crossnet_table.py    ###
############################################

Script that creates snap tables for a given crossnet.

Usage:
python create_snap_crossnet_table.py <input_file_path> <src_file_path> <dst_file_path> <dataset_name> <dataset_id>

Positional Arguments:
input_file_path:         Path to the input file; Input file should be a tsv.
src_file_path:           Path to a dataset specific file, as outputted by create_snap_mode_table.py,
                         corresponding to the source mode. File name MUST MATCH FORMAT:
                         miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv
dst_file_path:           Path to a dataset specific file, as outputted by create_snap_mode_table.py,
                         corresponding to the destination mode. File name MUST MATCH FORMAT:
                         miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv
dataset_name:            Name of dataset being used to create the snap crossnet tables i.e. the 
                         dataset the input file comes from. e.g. STRING
dataset_id:              unique integer id for this dataset.


Optional arguments:
--src_node_index:        If there are multiple columns in the input tsv, the index of the column with the src node id.
                         Defaults to 0.
--dst_node_index:        If there are multiple columns in the input tsv, the index of the column with the dst node id.
                         Defaults to 1.
--output_dir:            Directory to create output files. Defaults to the current working directory.
--full_crossnet_file:    Name of output file tsv containing a list of <snap_id>\t<dataset_id>.
                         Defaults to output_dir/miner-<src_mode_name>-<dst_mode_name>-<date>.tsv
--db_edge_file:          Name of output file tsv for a specific dataset; contains a list of <snap id>\t<dataset_specific_entity_id>
                         Defaults to output_dir/miner-<src_mode_name>-<dst_mode_name>-<dataset_id>-<dataset>-<date>.tsv
--snap_id_counter_start  Start assigning snap ids from this integer value; this number MUST be greater
                         than any id found in the full crossnet file.
--skip_missing_ids       Flag; If any of the ids in the input tsv do not have snap ids (which are fetched from
                         the src and dst files), skip the line and continue parsing the data.

Example usage:
Creating files for genes-function relationships using GeneOntology:

Input files: go.tsv, miner-gene-0-GO-20160520.tsv, miner-function-0-GO-20160520.tsv

Output directory: outputs/genes-functions/

Output files: miner-gene-function-20160520.tsv, miner-gene-function-0-GO-20160520.tsv

Workflow:

python create_snap_crossnet_table.py go.tsv miner-gene-0-GO-20160520.tsv miner-function-0-GO-20160520.tsv GO 0 --output_dir outputs/genes-functions/


##############################################
###     create_snap_mode_equiv_table.py    ###
##############################################

Script that creates snap equivalence table between two datasets for a given mode.

Usage:
python create_snap_mode_equiv_table.py <dataset1_file_path> <dataset2_file_path>

Positional Arguments:
dataset1_file_path:      Path to a dataset specific file, as outputted by create_snap_mode_table.py,
                         corresponding to the source mode. File name MUST MATCH FORMAT:
                         miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv
dataset2_file_path:      Path to a dataset specific file, as outputted by create_snap_mode_table.py,
                         corresponding to the destination mode. File name MUST MATCH FORMAT:
                         miner-<mode_name>-<dataset_id>-<dataset>-<date>.tsv


Optional arguments:
--mapping_file_path:     Path to a tsv file containing the mapping between the two datasets.
--ds1_node_index:        If there are multiple columns in the input tsv, the index of the column with the dataset1 entity id.
                         Defaults to 0.
--ds2_node_index:        If there are multiple columns in the input tsv, the index of the column with the dataset2 entity id.
                         Defaults to 1.
--output_dir:            Directory to create output files. Defaults to the current working directory.
--equiv_file:            Name of output file tsv containing a list of <snap_id>\t<snap_id>.
                         Defaults to output_dir/miner-<mode_name>-equiv-<date>.tsv
--skip_missing_ids       Flag; If any of the ids in the input tsv do not have snap ids (which are fetched from
                         the src and dst files), skip the line and continue parsing the data.

Example usage:
Creating equivalence file for genes using GeneOntoloty and HUGO

Input files: hugo.tsv, miner-gene-0-GO-20160520.tsv, miner-gene-1-HUGO-20160520.tsv

Output directory: outputs/genes/

Output files: miner-gene-equiv-20160520.tsv

Workflow:

python create_snap_mode_equiv_table.py miner-gene-0-GO-20160520.tsv miner-gene-1-HUGO-20160520.tsv --mapping_file_path hugo.tsv --output_dir outputs/genes/


#########################################
###     extract_unique_node_ids.py    ###
#########################################

Script that creates a tsv containing all the unique node ids from a given input file.

Usage:
python extract_unique_node_ids.py <input_file_path> <output_file_path> <dataset_name> <column_1> <column_2> ... <column_N>

Positional Arguments:
input_file_path:         Path to the input file; Input file should be a tsv.
output_file_path:        Path to the output file; Output file will be a tsv.
dataset_name:            Name of dataset nodes are being extracted from e.g. STRING
columns:                 Columns containing node ids. Can specify many.


Optional arguments:
--node_name:             String indicating how to refer to the node ids in the file scheme. Defaults to node_id.
--has_title:             If provided, skips over the first line of the file.
--verbose:               If provided, prints to the console for every million lines of the input file processed.

Example usage:
Extracting node ids from a STRING edgelist file, consisting of <src_node_id>\t<dst_node_id>

Input files: STRING.tsv

Output file: STRING-nodes.tsv

Workflow:

python extract_unique_node_ids.py STRING.tsv STRING-nodes.tsv STRING 0 1 --node_name ENSEMBL_peptide_id --verbose 


###################################
###     extract_edge_list.py    ###
###################################

Script that creates an edge list given the input file.

Usage:
python extract_unique_node_ids.py <input_file_path> <output_file_path> <dataset_name> <src_node_column> <dst_node_column>

Positional Arguments:
input_file_path:         Path to the input file; Input file should be a tsv.
output_file_path:        Path to the output file; Output file will be a tsv.
dataset_name:            Name of dataset nodes are being extracted from e.g. STRING
src_node_column:         Column containing source node(s)
dst_node_column:         Column containing destination node(s)

Optional arguments:
--src_node_name:         String indicating how to refer to the src node ids in the file scheme. Defaults to node_id1.
--dst_node_name:         String indicating how to refer to the dst node ids in the file scheme. Defaults to node_id2.
--has_title:             If provided, skips over the first line of the file.
--verbose:               If provided, prints to the console for every million lines of the input file processed.
--src_node_sep:          If the column containing the src node actually contains a list of nodes, the character separater
                         used to split the text into the different node ids. Relevant for many-to-one relationships.
                         By default assumes only one node id specified.
--dst_node_sep:          If the column containing the dst node actually contains a list of nodes, the character separater
                         used to split the text into the different node ids. Relevant for one-to-many relationships.
                         By default assumes only one node id specified.

Example usage:
Extracting edge list from a STRING protein-protein interactions file, which contains many other fields.

Input files: STRING.tsv; assume protein 1 at index 1 and protein 2 at index 5.

Output file: STRING-edges.tsv

Workflow:

python extract_edge_list.py STRING.tsv STRING-edges.tsv STRING 1 5 --src_node_name protein_1 --dst_node_name protein_2

