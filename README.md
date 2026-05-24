<!-- Docu_Sort — Document Classification & Extraction Pipeline -->

A fully offline AI pipeline that ingests raw PDF documents, classifies them automatically, extracts structured fields, and enables semantic search — all without any paid or hosted API.

<!-- What It Does -->

1. **Ingests** all PDF/TXT files from the `documents/` folder
2. **Classifies** each document into: `Invoice` | `Resume` | `Utility Bill` | `Other` | `Unclassifiable`
3. **Extracts** structured fields per document type using regex
4. **Outputs** a clean `output.json` with all classifications and fields
5. **Builds** a local FAISS vector index for semantic search
6. **Allows** natural language queries to retrieve structured document data


<!-- Project Structure -->

```
DocuSort/
├── documents/              ← Put your PDF files here
├── main.py                 ← Pipeline runner + search CLI
├── extractor.py            ← PDF text extraction
├── classifier.py           ← Document type classification
├── field_extractor.py      ← Regex-based field extraction
├── search.py               ← FAISS index builder + semantic search
├── create_demo_data.py     ← Generates sample PDFs for testing
├── output.json             ← Generated after running pipeline
├── faiss.index             ← Generated after running pipeline
├── filenames_map.json      ← Generated after running pipeline
├── requirements.txt
└── README.md
```



<!-- Installation Steep -->

```bash
pip install -r requirements.txt
```


<!-- Usage -->

<!-- Step 1 — Add your documents -->

Place your PDF files inside the `documents/` folder.

Or generate sample demo PDFs:
```bash
python create_demo_data.py
```

<!-- Step 2 — Run the pipeline -->
```bash
python main.py
```

This will:
- Extract text from all documents
- Classify each document
- Extract structured fields
- Save `output.json`
- Build and save the FAISS index

<!-- Step 3 — Search documents -->
Interactive mode:
```bash
python main.py search
```

Direct query:
```bash
python main.py search "Find invoices from January"
python main.py search "Show resumes with Python skills"
python main.py search "Electricity bills with high usage"
```

<!-- Output Format -->

```json
{
  "invoice_1.pdf": {
    "class": "Invoice",
    "invoice_number": "INV-1001",
    "date": "January 15, 2025",
    "company": "ACME Corporation",
    "total_amount": 350.5
  },
  "resume_1.pdf": {
    "class": "Resume",
    "name": "John Doe",
    "email": "john.doe@gmail.com",
    "phone": "123-456-7890",
    "experience_years": 5
  },
  "utility_1.pdf": {
    "class": "Utility Bill",
    "account_number": "LESCO-8821-44X",
    "date": "February 5, 2025",
    "usage_kwh": 360.0,
    "amount_due": 5000.0
  }
}
```


<!-- Libraries & Methods -->

| Component         | Library / Method                             |
|-------------------|----------------------------------------------|
| PDF Extraction    | `pdfminer.six` — layout-aware text extractor |
| Classification    | Keyword scoring (rule-based, no model needed)|
| Field Extraction  | Python `re` — regex patterns per doc type    |
| Embeddings        | `sentence-transformers` — all-MiniLM-L6-v2   |
| Vector Store      | `faiss-cpu` — local IndexFlatL2              |
| Demo Data         | `fpdf2` — PDF generation for testing         |



<!-- Technical Rules Applied-->

- No OpenAI, Claude, Gemini, or any hosted API used
- Its fully offline and runs without internet after model download
- All are open-source libraries
- FAISS for local vector DB 
- CLI interface — no UI required
