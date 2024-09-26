import streamlit as st
import pandas as pd
import seaborn as sns
import time  # For simulating progress
from bravado.client import SwaggerClient

# Define the URL for cBioPortal's Swagger API documentation
api_url = 'https://www.cbioportal.org/api/v2/api-docs'

# Initialize the client
client = SwaggerClient.from_url(api_url, config={
    'validate_requests': False,
    'validate_responses': False,
    'validate_swagger_spec': False
})

# Define function to fetch mutations for a molecular profile
def get_mutations(molecular_profile_id, sample_list_id):
    try:
        # Simulate loading time with progress bar
        progress_bar = st.empty()
        progress = progress_bar.progress(0)
        for percent in range(0, 100, 10):
            time.sleep(0.1)
            progress.progress(percent + 10)

        # Call the API
        response = client.Mutations.getMutationsInMolecularProfileBySampleListIdUsingGET(
            molecularProfileId=molecular_profile_id,
            sampleListId=sample_list_id,
            projection='DETAILED'
        ).result()

        # Return the response for further processing
        progress_bar.empty()  # Remove progress bar once loading is done
        return response
    except Exception as e:
        # Provide a more detailed error message
        st.error(f"An error occurred: {str(e)}")
        return []

# Define function to process and display the data
def display_mutation_data(mutations):
    if not mutations:
        st.write("No data available.")
        return

    # Extract relevant data
    data = []
    for mutation in mutations:
        mutation_dict = {
            'Gene': mutation.gene.hugoGeneSymbol if mutation.gene else 'N/A',
            'Mutation Type': mutation.mutationType,
            'Protein Change': mutation.proteinChange,
            'Tumor Alt Count': mutation.tumorAltCount if mutation.tumorAltCount is not None else 0,
            'Tumor Ref Count': mutation.tumorRefCount if mutation.tumorRefCount is not None else 0,
            'Reference Allele': mutation.referenceAllele,
            'Variant Allele': mutation.variantAllele
        }
        data.append(mutation_dict)
    
    df = pd.DataFrame(data)
    
    if df.empty:
        st.write("No mutation data available.")
        return
    
    # Display the top 5 mutations
    top_mutations = df.nlargest(5, 'Tumor Alt Count')
    
    # Create a bar chart for visualization using Seaborn
    st.write("Mutation Counts Chart:")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Gene', y='Tumor Alt Count', data=top_mutations, palette=['#7877e6'])
    plt.xlabel('Gene', color='white')
    plt.ylabel('Tumor Alt Count', color='white')
    plt.title('Top 5 Mutations by Tumor Alt Count', color='white')
    plt.gca().set_facecolor('#2a2a36')
    plt.gcf().patch.set_facecolor('#2a2a36')
    plt.xticks(color='white')
    plt.yticks(color='white')
    st.pyplot(plt)

    # Display the results in a table
    st.write("Top 5 mutations based on tumor alt count:")
    st.dataframe(top_mutations, use_container_width=True)

    # Print raw response for debugging
    st.write(f"Raw API response for mutations:")
    st.write(mutations)

# Define cancer types and sample list IDs
cancer_types = {
    'Adrenocortical Carcinoma': ('acc_tcga_mutations', 'acc_tcga_all'),
    'Bladder Urothelial Carcinoma': ('blca_tcga_mutations', 'blca_tcga_all'),
    'Breast Cancer': ('brca_tcga_mutations', 'brca_tcga_all'),
    'Cervical Cancer': ('cesc_tcga_mutations', 'cesc_tcga_all'),
    'Colorectal Cancer': ('coad_tcga_mutations', 'coad_tcga_all'),
    'Esophageal Cancer': ('esca_tcga_mutations', 'esca_tcga_all'),
    'Glioblastoma Multiforme': ('gbm_tcga_mutations', 'gbm_tcga_all'),
    'Head and Neck Squamous Cell Carcinoma': ('hnsc_tcga_mutations', 'hnsc_tcga_all'),
    'Kidney Renal Clear Cell Carcinoma': ('kirc_tcga_mutations', 'kirc_tcga_all'),
    'Kidney Renal Papillary Cell Carcinoma': ('kirp_tcga_mutations', 'kirp_tcga_all'),
    'Liver Hepatocellular Carcinoma': ('lihc_tcga_mutations', 'lihc_tcga_all'),
    'Lung Adenocarcinoma': ('luad_tcga_mutations', 'luad_tcga_all'),
    'Lung Squamous Cell Carcinoma': ('lusc_tcga_mutations', 'lusc_tcga_all'),
    'Ovarian Cancer': ('ov_tcga_mutations', 'ov_tcga_all'),
    'Pancreatic Adenocarcinoma': ('paad_tcga_mutations', 'paad_tcga_all'),
    'Prostate Adenocarcinoma': ('prad_tcga_mutations', 'prad_tcga_all'),
    'Sarcoma': ('sarc_tcga_mutations', 'sarc_tcga_all'),
    'Skin Cutaneous Melanoma': ('skcm_tcga_mutations', 'skcm_tcga_all'),
    'Stomach Adenocarcinoma': ('stad_tcga_mutations', 'stad_tcga_all'),
    'Testicular Germ Cell Tumors': ('tgct_tcga_mutations', 'tgct_tcga_all'),
    'Thymoma': ('thym_tcga_mutations', 'thym_tcga_all'),
    'Thyroid Carcinoma': ('thca_tcga_mutations', 'thca_tcga_all'),
    'Uterine Carcinosarcoma': ('ucs_tcga_mutations', 'ucs_tcga_all'),
    'Uterine Corpus Endometrial Carcinoma': ('ucec_tcga_mutations', 'ucec_tcga_all')
}

# Set page configuration
st.set_page_config(page_title="Mutation Data Viewer", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for styling the progress bar and other elements
st.markdown(
    """
    <style>
    .reportview-container {
        background: #2a2a36;
    }
    .sidebar .sidebar-content {
        background: #2a2a36;
        color: white;
    }
    .widget-container {
        color: white;
    }
    .stButton > button {
        background-color: #7877e6;
        color: white;
        border: none;
    }
    .stTable th {
        color: white;
    }
    .stTable td {
        color: white;
    }
    .stMarkdown {
        color: white;
    }
    /* Gradient purple progress bar */
    .stProgress > div > div {
        background: linear-gradient(to right, #6a0dad, #ba55d3);
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("Mutation Data Viewer")

# Select cancer type
selected_cancer = st.selectbox("Select Cancer Type", list(cancer_types.keys()))

# Fetch and display data based on selected cancer type
if st.button("Fetch Mutations"):
    molecular_profile_id, sample_list_id = cancer_types[selected_cancer]
    
    st.write(f"Fetching data for {selected_cancer}...")
    mutations = get_mutations(molecular_profile_id, sample_list_id)
    
    if mutations:  # Only display if mutations are found
        display_mutation_data(mutations)
    else:
        st.write(f"No data found for {selected_cancer}.")
