# OncoGeneSearch
Here’s a **README.txt** template for your **biomed project** that integrates multiple APIs like **cBioPortal**, **AlphaFold**, and others to detect potential oncogenes and mutations in cancer types. It includes sections that explain the purpose of the project, how to install dependencies, how to use the app, and other relevant details. You can customize this as needed for your project.

---

## README.txt

### Project Title:  
**Oncogene Detection and Mutation Visualization App**

### Project Description:
This project aims to identify potential oncogenes or cancer regulator genes by using data from various biomedical databases and APIs, such as **cBioPortal**, **GEO profiles**, **AlphaFold**, and others. The app provides users with a list of the top mutations in the most probable genes for a given cancer type, detailed mutation information, and visualizes protein structures with possible mutations.

The app is built using **Streamlit** for the user interface, and it integrates several APIs to gather and analyze oncogenic data.

---

### Features:
- Fetch mutation data for specific cancer types from **cBioPortal**.
- Display the top 5 most probable mutations for the 5 most likely genes associated with a chosen cancer type.
- Use **AlphaFold** to display both normal and mutated protein structures.
- Provide a clean, user-friendly interface that displays the data in charts and tables.
- Include protein pathogenicity predictions and amino acid mutation visualizations.
- **Interactive**: Clickable charts to show protein details.

---

### Requirements:
1. **Python 3.8+**
2. **Streamlit** for the front end.
3. **Requests** for making API calls.
4. **Mol* Viewer** for interactive protein structure visualization.
5. **cBioPortal API**, **AlphaFold API**, and other relevant APIs.

#### Python Packages:
- `streamlit`
- `requests`
- `pandas`
- `matplotlib`
- `molstar` (for visualizing protein structures)
  
---

### Installation:

#### Step 1: Clone the Repository
```bash
git clone https://github.com/your-repo/oncogene-detection-app.git
cd oncogene-detection-app
```

#### Step 2: Install Required Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Set up API Keys
You may need to configure API access for cBioPortal and other services by setting up tokens (if required). Add these tokens to a `.env` file in the root directory:
```
CBIOPORTAL_API_TOKEN=your_cbioportal_token
ALPHAFOLD_API_URL=https://alphafold.ebi.ac.uk/api/
GEO_API_URL=https://www.ncbi.nlm.nih.gov/geo/
```

#### Step 4: Run the App
```bash
streamlit run app.py
```

---

### Usage:
1. **Select a Cancer Type**: Use the dropdown menu to choose a cancer type from the **PanCancer Atlas**.
2. **Fetch Mutation Data**: Click the "Fetch Data" button to retrieve the top 5 most probable mutations for the selected cancer type.
3. **View Mutation Details**: The app will display:
   - Charts of the most probable genes and mutations.
   - Detailed mutation data (gene, location, mutation type).
4. **Visualize Protein Structures**: Click on a gene in the chart to view its **normal** and **mutated** protein structures using the **AlphaFold** integration.
5. **Analyze Pathogenicity**: A clickable chart below the protein viewer will show pathogenicity predictions for specific amino acid mutations.

---

### API Documentation:

- **cBioPortal API**: Used to fetch mutation and gene data. More info [here](https://www.cbioportal.org/api).
- **AlphaFold API**: Fetches 3D models of proteins, normal and mutated.
- **GEO Profiles**: Optionally integrated for additional gene expression data.

---

### Project Structure:
```
- app.py              # Main Streamlit app script
- mutation_analysis.py # Script for querying mutation data from cBioPortal
- protein_viewer.py    # Script for visualizing proteins using Mol* Viewer
- utils/               # Helper functions and utilities
- .env                 # Environment variables file (for API tokens)
- requirements.txt     # Python dependencies
```

---

### Notes:
- If you encounter a `404` error when querying certain cancers in **cBioPortal**, it may be due to the API not having data for those specific cancers. Try selecting another type.
- The **AlphaFold** integration may take a few seconds to load depending on the complexity of the protein.

---

### Future Improvements:
- Add support for additional APIs (e.g., **JASPAR**, **OMIM**) for a more comprehensive analysis.
- Enhance the visualization features by allowing for comparison between multiple mutations within the same protein.

---

### Contact:
For any issues, feature requests, or contributions, please reach out to:  
**Your Name**  
**Email: your.email@example.com**

---

This file provides an overview of your biomed project and guides users on how to install and use it. Would you like any specific section expanded or adjusted?
