import streamlit as st
import py3Dmol
import requests
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Set Streamlit app's background color and button color
st.markdown("""
    <style>
        .stApp {
            background-color: #2a2a36;
        }
        div.stButton > button {
            background-color: #7877e6;
            color: white;
        }
        input {
            color: white;
        }
        div.stTextInput > div > input {
            background-color: #2a2a36;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# Function to fetch AlphaFold protein data or PDB data as fallback
def fetch_structure(uniprot_or_url):
    # Check AlphaFold first
    if uniprot_or_url.startswith('http'):  # If the input is a URL
        url = uniprot_or_url
    else:  # Otherwise treat it as a UniProt ID for AlphaFold
        url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_or_url}-F1-model_v4.pdb"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        # Try PDB if AlphaFold fails
        st.warning(f"AlphaFold not found for {uniprot_or_url}, checking PDB...")
        pdb_url = f"https://files.rcsb.org/view/{uniprot_or_url}.pdb"
        pdb_response = requests.get(pdb_url)
        if pdb_response.status_code == 200:
            return pdb_response.text
        else:
            st.error(f"No protein structure found for {uniprot_or_url} in both AlphaFold and PDB.")
            return None

# Function to visualize the protein using py3Dmol
def show_protein_structure(pdb_data):
    viewer = py3Dmol.view(width=800, height=600)
    viewer.setBackgroundColor('#2a2a36')  # Set background color after initialization
    viewer.addModel(pdb_data, 'pdb')
    viewer.setStyle({'cartoon': {'color': 'spectrum'}})
    viewer.zoomTo()
    viewer.show()

    return viewer

# Function to extract amino acids from PDB file
def extract_amino_acids(pdb_data):
    amino_acids = []
    for line in pdb_data.splitlines():
        if line.startswith("SEQRES"):
            amino_acids.extend(line[19:].split())
    return amino_acids

# Function to display the amino acid chart
def plot_amino_acid_distribution(amino_acids):
    aa_counts = Counter(amino_acids)
    aa_df = pd.DataFrame(list(aa_counts.items()), columns=['Amino Acid', 'Count']).sort_values(by='Count', ascending=False)

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#2a2a36')  # Set the figure background color
    ax.set_facecolor('#2a2a36')  # Set the axis background color
    ax.barh(aa_df['Amino Acid'], aa_df['Count'], color="#7877e6")
    
    ax.set_xlabel('Count', color='white')
    ax.set_ylabel('Amino Acid', color='white')
    ax.set_title('Amino Acid Distribution', color='white')
    
    plt.gca().invert_yaxis()  # Invert y-axis for better readability
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    st.pyplot(fig)

# Function to handle mutation inputs (e.g., S234C, L662Q)
def apply_mutation_to_pdb(pdb_data, mutations):
    pdb_lines = pdb_data.splitlines()
    mutated_pdb = []
    
    for line in pdb_lines:
        if line.startswith("ATOM"):
            res_name = line[17:20].strip()
            chain = line[21]
            res_seq = int(line[22:26].strip())
            atom_name = line[12:16].strip()

            for mutation in mutations:
                orig_aa = mutation[0]
                pos = int(mutation[1:-1])
                new_aa = mutation[-1]

                # Apply the mutation at the specific position
                if res_seq == pos and res_name == orig_aa:
                    line = line[:17] + new_aa + line[20:]

            mutated_pdb.append(line)
        else:
            mutated_pdb.append(line)

    return "\n".join(mutated_pdb)

# Streamlit App Layout
st.title("AlphaFold Protein Structure Viewer with Mutations")
st.markdown("<h3 style='color: white;'>Enter the UniProt IDs or URLs for the normal and mutated proteins</h3>", unsafe_allow_html=True)

# Input fields for normal protein, mutated protein 1, and mutated protein 2
normal_protein_input = st.text_input("Normal Protein UniProt ID/URL:", "Q8N6V4")
mutated1_protein_input = st.text_input("Mutated 1 Protein (e.g., S234C):", "")
mutated2_protein_input = st.text_input("Mutated 2 Protein (e.g., L662Q):", "")

# Initialize session state for managing displayed structure
if 'current_protein_viewer' not in st.session_state:
    st.session_state['current_protein_viewer'] = None
    st.session_state['current_amino_acids'] = None

# Create buttons to fetch the normal protein, mutated 1, and mutated 2
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Normal Protein"):
        pdb_data = fetch_structure(normal_protein_input)
        if pdb_data:
            st.session_state['current_protein_viewer'] = show_protein_structure(pdb_data)
            st.session_state['current_amino_acids'] = extract_amino_acids(pdb_data)

with col2:
    if st.button("Mutated 1"):
        if mutated1_protein_input:
            mutations = [mutated1_protein_input]
            pdb_data = fetch_structure(normal_protein_input)
            if pdb_data:
                mutated_pdb = apply_mutation_to_pdb(pdb_data, mutations)
                st.session_state['current_protein_viewer'] = show_protein_structure(mutated_pdb)
                st.session_state['current_amino_acids'] = extract_amino_acids(mutated_pdb)

with col3:
    if st.button("Mutated 2"):
        if mutated2_protein_input:
            mutations = [mutated2_protein_input]
            pdb_data = fetch_structure(normal_protein_input)
            if pdb_data:
                mutated_pdb = apply_mutation_to_pdb(pdb_data, mutations)
                st.session_state['current_protein_viewer'] = show_protein_structure(mutated_pdb)
                st.session_state['current_amino_acids'] = extract_amino_acids(mutated_pdb)

# Display the currently selected protein structure (if any)
if st.session_state['current_protein_viewer']:
    viewer_html = st.session_state['current_protein_viewer']._make_html()
    st.components.v1.html(viewer_html, height=600)

# Display the amino acid distribution chart for the current structure (if available)
if st.session_state['current_amino_acids']:
    st.markdown("<h3 style='color: white;'>Amino Acid Distribution</h3>", unsafe_allow_html=True)
    plot_amino_acid_distribution(st.session_state['current_amino_acids'])
