from pprint import pprint
from collections import defaultdict
import os


# In[79]:

def parse_do_file_to_list(fname):
    """
    Reads the disease ontology in obo format from file
    given by fname, and returns the ontology as a list
    of dictionaries, one dictionary per entry.
    The dictionary for each entry is structured with
    the following fields
    {
        'id' (The disease ontology id)
        'name'
        'def'
        'synonym'
        'alt_id' (A list of alternate DOID ids)
        'xref' (A list of xrefs to MESH/OMIM ids)
        'is_a' (A DOID of what this disease is)
    
    }
    """
    f = open(fname, 'r')

    preamble = True # If we're in the top part of the file
    global_list = []
    curr_node_dict = {}
    for line in f:
        if preamble:
            if line.startswith('[Term]'):
                preamble = False
            continue
        spline = line.strip().split()
        if len(spline) == 0:
            global_list.append(curr_node_dict)
            curr_node_dict = {}
            continue
        if spline[0] == 'id:':
            if not spline[1].startswith('DOID'): # This means we've reached the bottom part of the file.
                break
            curr_node_dict['id'] = spline[1]
        elif spline[0] == 'name:':
            curr_node_dict['name'] = ' '.join(spline[1:])
        elif spline[0] == 'def:':
            curr_node_dict['def'] = ' '.join(spline[1:])
        elif spline[0] == 'synonym:':
            curr_node_dict['synonym'] = ' '.join(spline[1:])
        elif spline[0] == 'alt_id:':
            if 'alt_id' in curr_node_dict:
                curr_node_dict['alt_id'].append(spline[1])
            else:
                curr_node_dict['alt_id'] = [spline[1]]
        elif spline[0] == 'is_a:':
            curr_node_dict['is_a'] = spline[1]
        elif spline[0] == 'xref:':
            if 'xref' in curr_node_dict:
                curr_node_dict['xref'].append(spline[1])
            else:
                curr_node_dict['xref'] = [spline[1]]

                
    return global_list


# In[80]:

def parse_ctd_file_to_list(fname):
   """
   Parses the ctd_diseases.tsv file, and returns it as a list
   of entries, each entry represented as a dictionary with structure:
   {
       'name'
       'id'
       'alt_ids' (list of alternate disease ids)
       'defs'
       'parents' (list of parent ids)
       'syns'
   }
   """
   f = open(fname,'r')
   ctd_list = []
   for line in f:
       if line.startswith('#'):
           continue
       spline = line.strip('\n').split('\t')
       name = spline[0]
       disease_id = spline[1]
       alt_ids = spline[2]
       defs = spline[3]
       parents = spline[4]
       syns = spline[7]
       if len(alt_ids) > 0:
           alt_ids = alt_ids.split('|')
       else:
           alt_ids = []
       if len(parents) > 0:
           parents = parents.split('|')
       else:
           parents = []
       ctd_list.append({
               'name': name,
               'id': disease_id,
               'alt_ids': alt_ids,
               'defs': defs,
               'parents': parents,
               'syns': syns
           })
               
   return ctd_list


# In[81]:

def parse_omim_file_to_list(omim_dir):
    """
    Takes the OMIM directory as an argument, and
    returns a list of diseases from OMIM.
    First, it goes over the mim2gene file, and stores
    the OMIM numbers which correspond to diseases (phenotype).
    Then, it goes over the genemap and produces a list of entries
    which correspond to diseases, one dictionary per entry.
    Each dictionary has the following structure:
    {
        'id',
        'cyto_loc',
        'gene_symbols',
        'gene_name',
        'comments',
        'phenotypes',
        'mouse_symb'
    }
    """
    
    mim2gene_f = open(os.path.join(omim_dir, 'mim2gene.txt'), 'r')
    genemap_f = open(os.path.join(omim_dir, 'genemap.txt'), 'r')
    
    # The set of mim numbers corresponding to diseases.
    disease_mims = set()
    for line in mim2gene_f:
        if line.startswith('#'):
            continue
        sp_line = line.split('\t')
        mim_number = sp_line[0]
        mim_type = sp_line[1]
        if mim_type == 'phenotype':
            disease_mims.add(mim_number)
    
    omim_list = []
    # Now, go over genemap and populate the list.
    for line in genemap_f:
        if line.startswith('#'):
            continue

        sp_line = line.strip('\n').split('\t')
        mim_number = sp_line[8]
        if mim_number not in disease_mims:
            continue
        cyto_loc = sp_line[4]
        gene_symbols = sp_line[5]
        gene_name = sp_line[7]

        comments = sp_line[10]
        phenotypes = sp_line[11]
        mouse_gene_symbol = sp_line[12]
        omim_list.append({
                'id' : 'OMIM:' + mim_number,
                'cyto_loc': cyto_loc,
                'gene_symbols': gene_symbols,
                'gene_name': gene_name,
                'comments': comments,
                'phenotypes': phenotypes,
                'mouse_symb': mouse_gene_symbol
            })
    return omim_list


# In[82]:

# The snap id count. We increment when we come across a new disease.
# Snap ids for diseases will be "SNAPD0", "SNAPD1" etc.
snap_max_id = 0

# Diseases have three kinds of ids -- disease ontology, OMIM and MESH.
# We have a separate table for each id, indexed by the constants below.
# There are OMIM ids both in CTD and OMIM. So, we have a separate table for both.
DOID_T = 0
CTD_OMIM_T = 1
CTD_MESH_T = 2
OMIM_T = 3

# Creating dicts to store all the mappings, back and forth.
doid_to_snap_dict = defaultdict(list)
mesh_to_snap_dict = defaultdict(list)
omim_to_snap_dict = defaultdict(list)

snap_to_doid_dict = defaultdict(list)
snap_to_mesh_dict = defaultdict(list)
snap_to_omim_dict = defaultdict(list)

# Output files
dir_table_out_f = open('disease_node_directory_table.tsv', 'w')
doid_out_f = open('doid_node_table.tsv', 'w')
ctd_mesh_out_f = open('ctd_mesh_node_table.tsv', 'w')
ctd_omim_out_f = open('ctd_omim_node_table.tsv', 'w')
omim_out_f = open('omim_node_table.tsv','w')
# First, we go over the disease ontology, assigning SNAP ids.

# Get the Disease Ontology as a list of one dictionary per entry.
do_list = parse_do_file_to_list('doid.obo')
# Get the CTD node table as a list of one dictionary per entry.
ctd_list = parse_ctd_file_to_list('CTD/0416_CTD/CTD_diseases.tsv')
# Get the OMIM node table as a list of one dictionary per entry.
omim_list = parse_omim_file_to_list('OMIM/0416_OMIM')


# In[83]:

# Start writing the Disease Ontology to a file, and mapping our dictionaries in the meantime.
for entry in do_list:
    
    curr_snap_id = 'SNAPD' + str(snap_max_id)
    snap_max_id += 1
    
    # To the directory table, we write the SNAP id and the index of the DOID table.
    dir_table_out_f.write(curr_snap_id + '\t' + str(DOID_T) + '\n')
    
    # To the doid table, we write all the info.
    name = entry['name'] if 'name' in entry else ''
    definition = entry['def'] if 'def' in entry else ''
    synonym = entry['synonym'] if 'synonym' in entry else ''
    doid_out_f.write('\t'.join([curr_snap_id, entry['id'], name, definition, synonym]))
    doid_out_f.write('\n')
    
    # Populate dictionaries
    doid_to_snap_dict[entry['id']].append(curr_snap_id)
    snap_to_doid_dict[curr_snap_id].append(entry['id'])
    
    if 'alt_id' in entry:
        for alt_id in entry['alt_id']:
            doid_to_snap_dict[alt_id].append(curr_snap_id)
            snap_to_doid_dict[curr_snap_id].append(alt_id)
    
    if 'xref' in entry:
        for xref in entry['xref']:
            if xref.startswith('OMIM'):
                omim_to_snap_dict[xref].append(curr_snap_id)
                snap_to_omim_dict[curr_snap_id].append(xref)
            elif xref.startswith('MSH'):
                # For consistency, use MESH:id instead of MSH:id
                mesh_id = xref[:1] + 'E' + xref[1:]
                
                mesh_to_snap_dict[mesh_id].append(curr_snap_id)
                snap_to_mesh_dict[curr_snap_id].append(mesh_id)


# In[85]:

for entry in ctd_list:
    
    curr_snap_id = 'SNAPD' + str(snap_max_id)
    snap_max_id += 1
    
    # The string to write into the output file.
    str_to_write = '\t'.join([curr_snap_id, entry['id'], entry['name'], 
                              entry['defs'], entry['syns']])
    
    # Find the id; in CTD, it can be either an OMIM or a MESH id.
    if entry['id'].startswith('MESH'):
        dir_table_out_f.write(curr_snap_id + '\t' + str(CTD_MESH_T) + '\n')
        ctd_mesh_out_f.write(str_to_write + '\n')
        mesh_to_snap_dict[entry['id']].append(curr_snap_id)
        snap_to_mesh_dict[curr_snap_id].append(entry['id'])
    elif entry['id'].startswith('OMIM'):
        dir_table_out_f.write(curr_snap_id + '\t' + str(CTD_OMIM_T) + '\n')
        ctd_omim_out_f.write(str_to_write + '\n')
        omim_to_snap_dict[entry['id']].append(curr_snap_id)
        snap_to_omim_dict[curr_snap_id].append(entry['id'])
    else:
        assert False, "CTD has id which is neither MESH nor OMIM"  # Sanity check: this shouldn't happen.
         
    for alt_id in entry['alt_ids']:
        if alt_id.startswith('OMIM'):
            omim_to_snap_dict[alt_id].append(curr_snap_id)
            snap_to_omim_dict[curr_snap_id].append(alt_id)
        elif alt_id.startswith('MESH'):
            mesh_to_snap_dict[alt_id].append(curr_snap_id)
            snap_to_mesh_dict[curr_snap_id].append(alt_id)


# In[87]:

for entry in omim_list:
    curr_snap_id = 'SNAPD' + str(snap_max_id)
    snap_max_id += 1
    
    dir_table_out_f.write(curr_snap_id + '\t' + str(OMIM_T) + '\n')
    omim_out_f.write('\t'.join([curr_snap_id, entry['id'], entry['phenotypes'],
                                entry['gene_name'], entry['gene_symbols'], entry['cyto_loc'],
                               entry['mouse_symb']]) + '\n')
    
    omim_to_snap_dict[entry['id']].append(curr_snap_id)
    snap_to_omim_dict[curr_snap_id].append(entry['id'])


# In[88]:

# Close node table files.
dir_table_out_f.close()
doid_out_f.close()
ctd_mesh_out_f.close()
ctd_omim_out_f.close()
omim_out_f.close()


# In[2]:

# In[130]:

# Now, we generate the edge tables.

# We have different snap eid counts for each edge table
max_snap_eids = defaultdict(int)

# Disease-disease
# Files
dd_dir_table_out_f = open('disease_disease_edge_directory_table.tsv', 'w')
dd_doid_out_f = open('disease_disease_doid_table.tsv', 'w')
# The index of the Disease Ontology Table
DD_DOID_T = 0

# Disease-gene
# Files
dg_dir_table_out_f = open('disease_gene_edge_directory_table.tsv', 'w')
dg_ctd_out_f = open('disease_gene_ctd_table.tsv', 'w')
# The index of the CTD disease-gene link
DG_CTD_T = 0

# Disease-func
# Files
df_dir_table_out_f = open('disease_func_edge_directory_table.tsv', 'w')
df_ctd_out_f = open('disease_func_ctd_table.tsv', 'w')
# The index of the CTD disease-func link
DF_CTD_T = 0


# In[107]:

# First, the disease-disease table based on the is-a relationship in DOID

for entry in do_list:
    if 'is_a' in entry:
        curr_edge_id = 'SNAPDD' + str(max_snap_eids['DD'])
        max_snap_eids['DD'] = max_snap_eids['DD'] + 1
        
        
        # In case of multiple SNAP ids, we just take the first one
        # because that will give us the DOID entry which created the
        # SNAP id.
        src_snap_id = doid_to_snap_dict[entry['id']][0]
        dst_snap_id = doid_to_snap_dict[entry['is_a']][0]
        
        dd_dir_table_out_f.write('\t'.join([curr_edge_id, str(DD_DOID_T), src_snap_id, dst_snap_id]))
        dd_dir_table_out_f.write('\n')
        
        dd_doid_out_f.write(curr_edge_id + '\t' + entry['id'] + '\t' + entry['is_a'] + '\n')


# In[108]:

dd_dir_table_out_f.close()
dd_doid_out_f.close()


# In[3]:

# In[110]:

# First, to get the SNAP gene ids, we need to
# get the Uniprot ids for each gene, and then the
# corresponding SNAP id.

# First, we load uniprot ids.
ctd_gene_node_f = open('CTD/0416_CTD/CTD_genes.tsv', 'r')
ncbi_to_uniprot_dict = {}
for line in ctd_gene_node_f:
    if line.startswith('#'):
        continue
    sp_line = line.strip('\n').split('\t')
    ncbi_id = sp_line[2]
    uniprot_ids = sp_line[7]
    if len(uniprot_ids) > 0:
        uniprot_ids = uniprot_ids.split('|')
        ncbi_to_uniprot_dict[ncbi_id] = uniprot_ids

# In[116]:

# Next, we go over the gene diseases file, and extract uniprot ids and mesh ids.
ctd_genes_diseases_f = open('CTD/0416_CTD/CTD_genes_diseases.tsv', 'r')

i = 0
uniprot_to_disease_info_dict = defaultdict(list)
for line in ctd_genes_diseases_f:
    i += 1
    if i % 500000 == 0:
        print i

    if line.startswith('#'):
        continue
    sp_line = line.strip('\n').split('\t')
    ncbi_id = sp_line[1]
    if ncbi_id not in ncbi_to_uniprot_dict:
        continue
    uniprot_ids = tuple(ncbi_to_uniprot_dict[ncbi_id])
    gene_symbol = sp_line[0]
    disease_name = sp_line[2]
    disease_id = sp_line[3]
    uniprot_to_disease_info_dict[uniprot_ids].append((disease_id, disease_name, gene_symbol))
    


# In[118]:

# Next, we load the mapping from UNIPROT ids to SNAP gene ids.
snap_to_uniprot_dict = {}
uniprot_to_snap_dict = defaultdict(list)

snap_to_uniprot_f = open('snap.genes.0.go', 'r')
for line in snap_to_uniprot_f:
    sp_line = line.strip('\n').split('\t')
    snap_id = 'SNAPG' + sp_line[0]
    uniprot = sp_line[1]
    snap_to_uniprot_dict[snap_id] = uniprot
    uniprot_to_snap_dict[uniprot].append(snap_id)


# In[4]:

# In[ ]:

# Now, we write the disease-gene maps to file

for entry in uniprot_to_disease_info_dict:
    gene_snap_id = None
    chosen_uniprot_id = None
    for uniprot_id in entry:
        if uniprot_id in uniprot_to_snap_dict:
            chosen_uniprot_id = uniprot_id
            gene_snap_id = uniprot_to_snap_dict[uniprot_id][0]
            break
    
    if gene_snap_id is None:
        continue

    for (disease_id, disease_name, gene_symbol) in uniprot_to_disease_info_dict[entry]:
        if disease_id.startswith('MESH'):
            disease_snap_id = mesh_to_snap_dict[disease_id][0]
        elif disease_id.startswith('OMIM'):
            disease_snap_id = omim_to_snap_dict[disease_id][0]
        else:
            assert False

        curr_edge_id = 'SNAPDG' + str(max_snap_eids['DG'])
        max_snap_eids['DG'] = max_snap_eids['DG'] + 1

        dg_dir_table_out_f.write('\t'.join([curr_edge_id, str(DG_CTD_T), disease_snap_id, gene_snap_id]))
        dg_dir_table_out_f.write('\n')

        dg_ctd_out_f.write(curr_edge_id + '\t' + disease_id + '\t' + chosen_uniprot_id + '\n')


# In[ ]:

dg_dir_table_out_f.close()
dg_ctd_out_f.close()


# In[5]:

def load_disease_functions_ctd(ctd_dir):
    f1 = open(os.path.join(ctd_dir, 'CTD_Disease-GO_biological_process_associations.tsv'), 'r')
    f2 = open(os.path.join(ctd_dir, 'CTD_Disease-GO_cellular_component_associations.tsv'), 'r')
    f3 = open(os.path.join(ctd_dir, 'CTD_Disease-GO_molecular_function_associations.tsv'), 'r')
    global_list = []
    for f in [f1, f2, f3]:
        for line in f:
            if line.startswith('#'):
                continue
            sp_line = line.strip('\n').split('\t')
            disease_id = 'MESH:' + sp_line[1]
            go_id = sp_line[3]
            global_list.append((disease_id, go_id))
    return global_list

disease_func_list = load_disease_functions_ctd('CTD/0416_CTD')


# In[6]:

pprint(disease_func_list[:10])


# In[7]:

snap_to_go_dict = {}
go_to_snap_dict = defaultdict(list)
snap_to_go_f = open('snap.func.0', 'r')
for line in snap_to_go_f:
    sp_line = line.strip('\n').split('\t')
    snap_id = 'SNAPF' + sp_line[0]
    go_id = sp_line[1]
    snap_to_go_dict[snap_id] = go_id
    go_to_snap_dict[go_id].append(snap_id)


# In[12]:

# Disease-func
# Files
df_dir_table_out_f = open('disease_func_edge_directory_table.tsv', 'w')
df_ctd_out_f = open('disease_func_ctd_table.tsv', 'w')
# The index of the CTD disease-func link
DF_CTD_T = 0
max_snap_eids['DF'] = 0
for (disease_id, go_id) in disease_func_list:
    try:
        disease_snap_id = mesh_to_snap_dict[disease_id][0]
        func_snap_id = go_to_snap_dict[go_id][0]
    except IndexError:
        continue
    curr_edge_id = 'SNAPDF' + str(max_snap_eids['DF'])
    max_snap_eids['DF'] = max_snap_eids['DF'] + 1

    df_dir_table_out_f.write('\t'.join([curr_edge_id, str(DF_CTD_T), disease_snap_id, func_snap_id]))
    df_dir_table_out_f.write('\n')

    df_ctd_out_f.write(curr_edge_id + '\t' + disease_id + '\t' + go_id + '\n')

df_dir_table_out_f.close()
df_ctd_out_f.close()


# In[14]:

# Get drug bank to chemicals mapping
ctd_chem_f = open('CTD/0416_CTD/CTD_chemicals.tsv', 'r')
chem_to_db_dict = {}
for line in ctd_chem_f:
    if line.startswith('#'):
        continue
    sp_line = line.strip('\n').split('\t')
    chemical_id = sp_line[1]
    drugbank_ids = sp_line[8]
    if len(drugbank_ids) > 0:
        drugbank_ids = drugbank_ids.split('|')
        chem_to_db_dict[chemical_id] = drugbank_ids


# In[15]:

chem_disease_list = []
chem_disease_f = open('CTD/0416_CTD/CTD_chemicals_diseases.tsv', 'r')
i = 0
for line in chem_disease_f:
    i += 1
    if i % 500000 == 0:
        print i
    if line.startswith('#'):
        continue
    sp_line = line.strip('\n').split('\t')
    chem_id = sp_line[1]
    disease_id = sp_line[4]
    chem_disease_list.append((chem_id, disease_id))


# In[16]:

# Load SNAP ids for DrugBank
snap_to_db_dict = {}
db_to_snap_dict = defaultdict(list)
snap_to_db_f = open('subSnapDrugbank.txt', 'r')
for line in snap_to_db_f:
    sp_line = line.strip('\n').split()
    snap_id = sp_line[0]
    db_id = sp_line[1]
    snap_to_db_dict[snap_id] = db_id
    db_to_snap_dict[db_id].append(snap_id)


# In[24]:

i = 0
for k, v in chem_to_db_dict.items():
    print k, v
    i += 1
    if i > 20:
        break


# In[27]:

# Disease-chem
# Files
dc_dir_table_out_f = open('disease_chem_edge_directory_table.tsv', 'w')
dc_ctd_out_f = open('disease_chem_ctd_table.tsv', 'w')
# The index of the CTD disease-func link
DC_CTD_T = 0
max_snap_eids['DC'] = 0
for (chem_id, disease_id) in chem_disease_list:
    chem_id = 'MESH:' + chem_id
    if chem_id not in chem_to_db_dict:
        continue
    chem_snap_id = None
    chosen_db_id = None
    for db_id in chem_to_db_dict[chem_id]:
        if db_id in db_to_snap_dict:
            chem_snap_id = db_to_snap_dict[db_id][0]
            chosen_db_id = db_id
            break
    if chem_snap_id is None:
        continue
    try:
        if disease_id.startswith('MESH'):
            disease_snap_id = mesh_to_snap_dict[disease_id][0]
        else:
            disease_snap_id = omim_to_snap_dict[disease_id][0]
    except IndexError:
        continue
    curr_edge_id = 'SNAPDC' + str(max_snap_eids['DC'])
    max_snap_eids['DC'] = max_snap_eids['DC'] + 1

    dc_dir_table_out_f.write('\t'.join([curr_edge_id, str(DC_CTD_T), disease_snap_id, chem_snap_id]))
    dc_dir_table_out_f.write('\n')

    dc_ctd_out_f.write(curr_edge_id + '\t' + disease_id + '\t' + chosen_db_id + '\n')

dc_dir_table_out_f.close()
dc_ctd_out_f.close()
