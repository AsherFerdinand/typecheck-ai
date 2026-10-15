# TypeCheck AI --- Automated Engineering Drawing Inspection Assistant

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Engineering](https://img.shields.io/badge/Domain-Engineering%20Digitalisation-1565C0)
![Status](https://img.shields.io/badge/Status-Prototype-orange)
![License](https://img.shields.io/badge/License-MIT-green)

**TypeCheck AI** is a portfolio project exploring how engineering
knowledge, rule-based automation, document processing, and optional AI
can be combined to assist with the inspection of technical drawings.

The prototype accepts a technical drawing in PDF format, extracts
available text and metadata, evaluates configurable inspection rules,
and presents traceable findings in a web interface. It is designed as an
engineering demonstrator---not as a certified compliance tool or a
replacement for qualified engineering review.

> **Project principle:** automate clear, repeatable checks; make
> uncertainty visible; keep engineering decisions traceable.

------------------------------------------------------------------------

## Table of Contents

-   [Project Overview](#project-overview)
-   [Why This Project?](#why-this-project)
-   [Objectives](#objectives)
-   [Core Features](#core-features)
-   [Workflow](#workflow)
-   [Example Inspection Rules](#example-inspection-rules)
-   [Technology Stack](#technology-stack)
-   [System Architecture](#system-architecture)
-   [Project Structure](#project-structure)
-   [Getting Started](#getting-started)
-   [Validation and Evaluation](#validation-and-evaluation)
-   [Cloud Deployment](#cloud-deployment)
-   [Limitations and Responsible Use](#limitations-and-responsible-use)
-   [Roadmap](#roadmap)
-   [Example Use Case](#example-use-case)
-   [Author](#author)

------------------------------------------------------------------------

## Project Overview

Technical drawing inspection can involve repetitive checks of drawing
identifiers, revision fields, dimensions, tolerance indications, and
required documentation. These checks can be time-consuming when
performed manually, particularly when criteria and recurring defects are
not organised consistently.

TypeCheck AI explores a structured workflow for assisting with those
checks:

1.  Upload an engineering drawing in PDF format.
2.  Extract readable text and document metadata.
3.  select the applicable inspection profile and criteria.
4.  Execute deterministic checks wherever the required information can
    be identified reliably.
5.  Classify each result as **Pass**, **Fail**, or **Review Required**.
6.  Present findings with the applicable rule and supporting evidence.
7.  Export a structured inspection report for human review.

The initial version focuses on a manageable set of document-level
checks. Later versions may add more advanced dimension parsing, image
processing, and AI-assisted explanations.

### Project scope

The first version is intended to demonstrate the workflow using
**synthetic or otherwise authorised sample drawings**. It does not claim
to validate legal type approval or automatically establish compliance
with a complete engineering standard.

## Why This Project?

This project connects four technical areas:

  -----------------------------------------------------------------------
  Area                                How it is applied
  ----------------------------------- -----------------------------------
  **Mechanical Engineering**          Interpret technical drawings,
                                      dimensions, tolerances, drawing
                                      metadata, and engineering
                                      inspection workflows.

  **AI / Machine Learning**           Use OCR for scanned documents and
                                      optionally use an LLM to explain
                                      findings or categorise text.

  **Software Development**            Build a modular Python application,
                                      rule engine, database, tests, and
                                      user interface.

  **Cloud Computing**                 Optionally deploy the application
                                      so authorised users can access it
                                      through a browser.
  -----------------------------------------------------------------------

The most important design decision is to use AI selectively. A clear
requirement such as "the drawing number field must not be empty" should
normally be checked using deterministic logic. AI is more appropriate
for tasks such as interpreting ambiguous text or drafting an
explanation, and its output must remain reviewable.

## Objectives

-   Create a structured and maintainable inspection-rule catalogue.
-   Convert inspection criteria into explicit, testable rules.
-   Extract text from text-based PDF drawings and support OCR for
    scanned documents.
-   Separate a confirmed failure from an inconclusive extraction result.
-   Provide traceable findings linked to the rule that triggered them.
-   Validate the tool against a manually labelled test dataset.
-   Estimate potential inspection-time savings using measured results.
-   Document technical limitations, assumptions, and automation
    feasibility.

## Core Features

### 1. Drawing upload and extraction

-   Upload a PDF through a browser-based interface.
-   Extract embedded PDF text using PyMuPDF.
-   Optionally apply OCR using Tesseract or EasyOCR when a drawing is
    scanned or has no usable text layer.
-   Preserve page references and, where feasible, the location of
    extracted text.

### 2. Configurable inspection rule engine

-   Store rules separately from application logic in JSON or SQLite.
-   Assign each rule an identifier, category, description, severity, and
    automation assessment.
-   Execute only rules applicable to the selected drawing profile.
-   Return a consistent result format for each check.

### 3. Structured findings

Each finding should include:

-   Rule ID and rule name
-   Inspection result: Pass, Fail, or Review Required
-   Evidence extracted from the document
-   Page number or location, when available
-   Explanation of the result
-   Confidence or extraction-quality indicator, where meaningful
-   Suggested next action

### 4. Defect library and feasibility matrix

-   Group recurring defects by category.
-   Record the data source and detection method required by each rule.
-   Assess automation feasibility, implementation effort, and the need
    for engineering review.
-   Prioritise rules using a documented scoring model.

### 5. Reporting

-   Display a summary of passed, failed, and review-required checks.
-   Export findings to CSV and a PDF inspection report.
-   Include the rule catalogue version and test/application version in
    the report where practical.

### 6. Optional AI-assisted explanation

A later version may use a large language model (LLM) to explain a
finding in plain language or categorise an unfamiliar defect
description. The model should receive the relevant rule and extracted
evidence as context. It must not silently override deterministic results
or declare regulatory compliance without an appropriate validated basis.

------------------------------------------------------------------------

## Workflow

``` mermaid
flowchart TD
    A["Upload technical drawing PDF"] --> B["Extract PDF text and metadata"]
    B --> C{"Text usable?"}
    C -- "Yes" --> D["Normalise extracted content"]
    C -- "No / scanned" --> E["OCR and image preprocessing"]
    E --> D
    D --> F["Select inspection profile"]
    F --> G["Load applicable rules"]
    G --> H["Execute deterministic checks"]
    H --> I["Classify each result"]
    I --> J["Pass"]
    I --> K["Fail"]
    I --> L["Review Required"]
    J --> M["Inspection summary and evidence"]
    K --> M
    L --> M
    M --> N["Annotated view and report export"]
    N --> O["Human validation and feedback"]
```

### Result semantics

-   **Pass:** The available evidence satisfies the configured rule.
-   **Fail:** The available evidence demonstrates that the configured
    rule is not satisfied.
-   **Review Required:** The tool cannot reach a reliable
    conclusion---for example, because OCR is uncertain, a required field
    cannot be located, or the check requires engineering judgement.

A missing extracted value must not automatically be treated as proof
that the drawing itself is defective. The application should distinguish
"not found" from "confirmed missing" wherever the extraction method
cannot guarantee reliable detection.

------------------------------------------------------------------------

## Example Inspection Rules

The following are **illustrative project rules**, not universal
regulatory or type-approval requirements. The applicable criteria for a
real inspection process must be established from the relevant authorised
requirements and approved procedures.

  -----------------------------------------------------------------------------
  Rule ID        Category         Example        Initial method  Automation
                                  criterion                      potential
  -------------- ---------------- -------------- --------------- --------------
  DOC-001        Document         Drawing number Text extraction High
                 metadata         is present     and field       
                                                 validation      

  DOC-002        Document         Revision       Text extraction High
                 metadata         identifier is  and field       
                                  present        validation      

  DOC-003        Document         Required       Text extraction High
                 metadata         title-block    and field       
                                  fields are     validation      
                                  populated                      

  DIM-001        Dimensions       A specified    Text/geometry   Medium
                                  required       parsing         
                                  dimension is                   
                                  present                        

  DIM-002        Tolerances       A required     Pattern         Medium
                                  tolerance      matching and    
                                  indication is  context checks  
                                  present                        

  GEO-001        Geometric        A required     Symbol/text     Medium
                 tolerancing      geometric      recognition     
                                  tolerance                      
                                  symbol or                      
                                  callout is                     
                                  present                        

  CONS-001       Consistency      Drawing        Rule-based      High
                                  identifier     comparison      
                                  matches a                      
                                  reference                      
                                  record                         

  SEM-001        Engineering      A tolerance or Human review    Low
                 interpretation   note is        initially       
                                  technically                    
                                  appropriate                    
  -----------------------------------------------------------------------------

Automation potential depends on drawing quality, consistency, available
reference data, and the exact inspection criterion. These labels are
hypotheses to validate, not measured performance claims.

### Rule data model

A rule record could contain fields such as:

``` json
{
  "rule_id": "DOC-001",
  "name": "Drawing number is present",
  "category": "Document metadata",
  "description": "Check whether the required drawing-number field is populated.",
  "applicable_profiles": ["sample_mechanical_drawing"],
  "data_source": "Extracted PDF text",
  "check_type": "required_field",
  "severity": "major",
  "automation_feasibility": "high",
  "human_review_required": false,
  "version": "1.0"
}
```

The actual implementation should validate rule definitions against a
schema and handle missing or malformed configuration explicitly.

------------------------------------------------------------------------

## Technology Stack

The stack below is a practical starting point. Optional components
should only be added when the core prototype is working.

  -----------------------------------------------------------------------
  Component               Technology              Purpose
  ----------------------- ----------------------- -----------------------
  Programming language    Python 3.11+            Application logic and
                                                  rule execution

  Web interface           Streamlit               Drawing upload,
                                                  findings, dashboards,
                                                  and reports

  PDF processing          PyMuPDF                 Text extraction and
                                                  page-level document
                                                  handling

  OCR                     Tesseract or EasyOCR    Text extraction from
                                                  scanned drawings

  Image processing        Pillow; OpenCV if       Image preparation and
                          needed                  visual processing

  Rule configuration      JSON                    Human-readable
                                                  inspection-rule
                                                  definitions

  Database                SQLite                  Store rules, inspection
                                                  runs, and results

  Data analysis           pandas                  Summaries, validation
                                                  metrics, and time-study
                                                  data

  Reporting               ReportLab; CSV export   Inspection reports

  Testing                 pytest                  Unit tests and
                                                  end-to-end validation

  Version control         Git and GitHub          Source control, issues,
                                                  and project
                                                  documentation

  Containerisation        Docker (optional)       Reproducible deployment
                                                  environment

  Cloud hosting           Render, Azure, or AWS   Browser-accessible
                          (optional)              deployment

  LLM integration         Optional provider or    Grounded explanations
                          local model             and text categorisation
  -----------------------------------------------------------------------

**Cloud is an optional deployment layer, not a prerequisite for the
first version.** Build and test locally first. Before hosting drawings,
consider data confidentiality, access control, retention, logging, and
the cloud provider's terms. Use synthetic files for public
demonstrations.

------------------------------------------------------------------------

## System Architecture

``` mermaid
flowchart LR
    U["User / Engineer"] --> UI["Streamlit Web UI"]
    UI --> S["Inspection Service"]
    S --> P["PDF Text Extractor"]
    S --> O["OCR Adapter (optional)"]
    P --> R["Rule Engine"]
    O --> R
    R --> DB[("SQLite Rule Catalogue and Results")]
    R --> V["Validation and Result Classifier"]
    V --> UI
    V --> REP["PDF / CSV Report Generator"]
    S -. "Optional, evidence-grounded explanation" .-> LLM["LLM Adapter"]
```

### Architectural principles

-   **Separation of concerns:** extraction, rule execution, result
    classification, storage, and presentation should be separate
    modules.
-   **Traceability:** every finding should identify the rule and
    evidence behind it.
-   **Reproducibility:** inspection runs should record which
    rule-catalogue version was used.
-   **Fail-safe handling:** uncertain extraction should result in
    review, not an unjustified pass or fail.
-   **Privacy by design:** minimise stored drawing content and avoid
    uploading confidential drawings to external services without
    permission.

------------------------------------------------------------------------

## Project Structure

A suggested repository structure:

``` text
typecheck-ai/
├── src/
│   └── typecheck_ai/
│       ├── app.py                  # Streamlit entry point
│       ├── core/
│       │   ├── rule_engine.py      # Rule evaluation
│       │   ├── result_models.py    # Structured inspection results
│       │   └── validation.py       # Result and input validation
│       ├── extractors/
│       │   ├── pdf_extractor.py    # PDF text and metadata
│       │   └── ocr_extractor.py    # Optional OCR pipeline
│       ├── services/
│       │   ├── inspection_service.py
│       │   └── report_service.py
│       ├── storage/
│       │   └── repository.py       # Database access
│       └── utils/
├── config/
│   └── rules.json                  # Example rule catalogue
├── data/
│   └── sample_drawings/            # Synthetic/authorised samples only
├── tests/
│   ├── test_rule_engine.py
│   ├── test_pdf_extractor.py
│   └── test_inspection_workflow.py
├── docs/
│   ├── inspection_criteria.md
│   ├── feasibility_matrix.md
│   ├── validation_report.md
│   └── business_case.md
├── .gitignore
├── requirements.txt
├── Dockerfile                      # Optional
├── README.md
└── LICENSE
```

The exact structure can evolve as the application grows. Keep the first
implementation small and understandable rather than creating empty
modules for every planned feature.

------------------------------------------------------------------------

## Getting Started

### Prerequisites

-   Python 3.11 or newer
-   Git
-   A code editor such as Visual Studio Code
-   Synthetic or authorised sample PDF drawings

OCR is optional for the initial milestone. If you enable Tesseract,
install the Tesseract application separately and make sure it is
available to your Python environment.

### 1. Clone the repository

Replace the example URL with your GitHub repository URL.

``` bash
git clone https://github.com/<your-username>/typecheck-ai.git
cd typecheck-ai
```

### 2. Create a virtual environment

**Windows PowerShell:**

``` powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

If PowerShell prevents activation, use the appropriate execution-policy
guidance for your environment or activate the environment through your
editor. Do not change system security settings unnecessarily.

### 3. Install dependencies

Once `requirements.txt` has been created:

``` bash
pip install -r requirements.txt
```

### 4. Start the application

After implementing the Streamlit entry point:

``` bash
streamlit run src/typecheck_ai/app.py
```

Open the local URL shown in the terminal, typically
`http://localhost:8501`.

> These commands describe the intended setup. They will work once the
> corresponding application files and dependency list have been
> implemented.

------------------------------------------------------------------------

## Validation and Evaluation

Validation is a core deliverable, not an optional final polish.

### Test dataset

Create a labelled set of synthetic drawings containing both correct
examples and controlled defects. Record the expected result for every
rule that applies to each drawing. Include both text-based PDFs and
scanned or degraded examples if OCR is in scope.

### Metrics

-   **Precision:** Of the failures reported by the tool, how many were
    genuine failures?
-   **Recall:** Of the genuine failures in the labelled test set, how
    many did the tool detect?
-   **False-positive rate:** How often did the tool flag a defect when
    the corresponding requirement was actually satisfied?
-   **False-negative count/rate:** How often did the tool miss a genuine
    defect?
-   **Review-required rate:** How often could the tool not reach a
    sufficiently reliable conclusion?
-   **Processing time:** How long did extraction and rule evaluation
    take?
-   **Inspection effort:** How much human time was required before and
    after assistance?

For a rule-based checker, report metrics per rule as well as across the
dataset. Overall averages can conceal a weak or unreliable individual
check.

### Validation procedure

1.  Define each criterion and its expected result before testing.
2.  Label the test drawings independently of the tool's output.
3.  Run the same dataset through the application.
4.  Compare predicted results against the labels.
5.  Investigate false positives and false negatives.
6.  Refine the rule or extraction process and rerun the tests.
7.  Document the test-set size, limitations, and results.

Do not publish performance figures until they have been measured on the
documented test set.

## Business Case: Inspection-Time Savings

The prototype can estimate potential time savings by comparing manual
inspection with assisted inspection.

\[ T\_{`\text{saved}`{=tex}} =
`\frac{N \times (t_{\text{manual}} - t_{\text{assisted}})}{60}`{=tex} \]

Where:

-   \(N\) is the number of drawings inspected in the chosen period.
-   (t\_{`\text{manual}`{=tex}}) is the average manual inspection time
    per drawing in minutes.
-   (t\_{`\text{assisted}`{=tex}}) is the average total human time per
    drawing when using the assistant, including review of uncertain
    findings.

For a meaningful comparison, use the same representative drawings and
inspection scope. Include setup, exception handling, false alarms, and
rule maintenance where relevant. Time saved does not automatically equal
cash saved; the business case should explain how the released capacity
could be used.

------------------------------------------------------------------------

## Cloud Deployment

Once the local prototype and validation suite are stable, the
application can be deployed to a cloud hosting service.

A simple deployment model is:

1.  Package the application and dependencies.
2.  Store source code in GitHub.
3.  Deploy to a supported hosting service, such as Render, Azure, or
    AWS.
4.  Configure secrets through the hosting provider's
    environment-variable mechanism.
5.  Restrict access if drawings or reports are not public.
6.  Test file-size limits, temporary-file handling, error messages, and
    logging.
7.  Define whether uploads and reports are deleted after processing or
    retained under an explicit policy.

### Important deployment considerations

-   A local SQLite database may not be suitable for every multi-user or
    ephemeral hosting setup.
-   Temporary uploads should be removed when no longer needed.
-   Do not commit API keys, credentials, private drawings, or personal
    data to GitHub.
-   Use synthetic sample files for a public demo.
-   Do not send confidential drawings to an external LLM or OCR service
    without appropriate authorisation.
-   Cloud deployment does not itself make the application secure or
    compliant.

A public cloud demo is a useful extension, but a reliable local
prototype with strong tests is a better first milestone than a
prematurely deployed application.

------------------------------------------------------------------------

## Limitations and Responsible Use

-   This is a learning and portfolio project, not a certified
    drawing-inspection system.
-   Example rules do not represent a complete type-approval checklist.
-   Text extraction and OCR can fail on low-resolution scans, unusual
    fonts, symbols, and complex layouts.
-   Correctly detecting a dimension string does not prove that the
    dimension is technically correct.
-   Presence checks are generally easier than interpreting engineering
    intent.
-   Any AI-generated explanation can be incomplete or incorrect and must
    be checked against the source evidence.
-   Human review remains necessary for ambiguous, high-impact, or
    technically complex findings.
-   Real manufacturer drawings and confidential approval documents must
    only be used with explicit authorisation.

## Roadmap

### Phase 1 --- Minimum viable product

-   [ ] Create the repository and Python environment.
-   [ ] Define 10--15 initial inspection rules.
-   [ ] Create synthetic PDF drawings and expected-result labels.
-   [ ] Implement PDF text extraction.
-   [ ] Build the JSON-driven rule engine.
-   [ ] Support Pass, Fail, and Review Required results.
-   [ ] Add unit tests.

### Phase 2 --- Usable inspection application

-   [ ] Build the Streamlit interface.
-   [ ] Add rule catalogue browsing and filtering.
-   [ ] Display evidence and page references.
-   [ ] Export CSV and PDF reports.
-   [ ] Store inspection history and rule versions.

### Phase 3 --- Validation and process analysis

-   [ ] Create a representative labelled test set.
-   [ ] Measure precision, recall, false positives, and false negatives.
-   [ ] Record processing and human review times.
-   [ ] Build an automation-feasibility matrix.
-   [ ] Document technical constraints and the business case.

### Phase 4 --- Advanced capabilities

-   [ ] Add OCR for scanned drawings.
-   [ ] Add drawing-region highlighting where extraction coordinates
    permit.
-   [ ] Explore dimension and tolerance parsing.
-   [ ] Add optional evidence-grounded LLM explanations.
-   [ ] Containerise with Docker.
-   [ ] Deploy a privacy-conscious demo to the cloud.

------------------------------------------------------------------------

## Example Use Case

A user uploads a synthetic mechanical component drawing. TypeCheck AI
extracts the drawing number and revision field, then runs the rules in
the selected inspection profile.

The application finds that the drawing number is present, but the
revision field cannot be located with sufficient confidence. It reports
the first rule as **Pass** and the second as **Review Required**,
displays the supporting extraction evidence, and adds both results to
the inspection report.

This outcome is preferable to automatically marking the revision check
as failed: the tool has not established whether the field is genuinely
missing or merely difficult to extract.

------------------------------------------------------------------------

## Author

Developed as an independent portfolio project exploring the intersection
of mechanical engineering, engineering documentation, software
development, and applied AI.

**Repository:** `typecheck-ai`

**Project status:** Prototype in development

**Note:** Update this README as features are implemented. Clearly
distinguish planned capabilities from completed and validated
functionality.
