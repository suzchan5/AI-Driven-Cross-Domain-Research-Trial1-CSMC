[**🇯🇵 日本語**](README.md)

# Research Project: AI-Driven Cross-Domain Research (Trial 1)

## "Can an AI agent transcend the boundaries of human expertise?"

### This project is an experimental attempt where a human engineer specializing in autonomous driving and control engineering collaborates with an AI agent (Antigravity / Gemini / NotebookLM) to conduct high-quality research in a completely different field (Cognitive Science), completing everything from theoretical construction to paper writing and numerical verification.

### The most distinctive feature is the quality assurance process built upon a complete research ecosystem, ranging from "Human-AI Co-Creation" to "The Hell of Peer Review (Adversarial Review)."

### 🤝 Respect for Expertise
The question "Can we transcend the boundaries of expertise?" is not a claim that human experts are becoming unnecessary. On the contrary, deep respect for the vast knowledge accumulated by experts in each field lies at the foundation of this project.
AI can serve as a "ladder" to democratize access to expert knowledge, but climbing that ladder to discover new truths and take responsibility remains a uniquely human role. This research explores not the conflict between experts and AI, but the new "intellectual horizons" reachable only through their collaboration.

## 🚀 AI-Driven Research Workflow (The Core Innovation)

The core value of this project lies in the "AI-Human-AI Loop" shown in the diagram below. It ensures academic robustness by incorporating not just **Generation**, but also **"Strict Auditing"** and **"Adversarial Review"** into the process.

A key innovation is the introduction of **Strict Source Grounding using NotebookLM**. By cross-referencing every statement in the paper against PDF files of real existing literature (primary sources), we successfully established a mechanism to instantly detect and eliminate AI-specific "Hallucinations" (fabrication of non-existent research or data).

![Project Workflow](docs/images/workflow_comic.png)
*Fig: The 3-Stage Process of AI-Driven Research*

### Phase 1: Co-Creation
Starting from the engineer's fragmented idea ("Can human panic be prevented using control engineering?"), the AI partner (Antigravity) constructs the logical structure and mathematical models. Through high-speed self-consistency check loops, a cohesive draft paper is generated.

### Phase 2: Grounding Verification
Google NotebookLM is deployed as a "Strict Gatekeeper." Using only the actual PDF literature (cited sources) as its knowledge base, it inspects whether the descriptions in the paper are perfectly consistent with the sources. If any hallucination (citation of non-existent research or misinterpretation of data) is found, the paper is immediately remanded to the writing phase.

### Phase 3: The Hell of Peer Review
As the final barrier, the AI enacts multiple adversarial reviewer personas (an authoritative professor, a critical young researcher, and a conservative critic) to thoroughly attack the completed draft from diverse perspectives. This cycle of criticism and defense is repeated over **100 loops**, eliminating logical vulnerabilities and refining the paper to a "Diamond Master" level of robustness.

#### 🛡️ The Gritty Reality: A Record of Struggle
While the concept is ideal, the actual process was far from smooth. This quality is underpinned by the accumulation of "gritty" work, where AI hallucinations and logical contradictions were detected time and again, requiring repeated corrections.

*   **[NotebookLM Validation Report](docs/reviews/notebooklm_validation_report_en.md)**: 
    *   Record of detecting citations of non-existent datasets (Gjoreski et al.) and correcting them to WESAD.
*   **[Initial Hell Review Archive](docs/reviews/review_history_archive_en.md)**: 
    *   The record of the "Gate of Hell" phase at the beginning of the project. It all started with the ruthless abuse from AI to AI: "Did you forget the basics of control engineering?"
*   **[Hell Review 100-Loop Report](docs/reviews/hell_review_rev9_en.md)**: 
    *   Full record of thorough attacks by "The Destroyer" persona and the corresponding defense (mathematical rebuttals).
*   **[International Hell Review (English)](docs/reviews/hell_review_en_final.md)**: 
    *   **New!** The English draft was audited by the "International Committee" (Oxford / MIT / Silicon Valley personas) to ensure global academic standards.
*   **[Process Log](docs/process_log_en.md)**: 
    *   The story of how humans and AI collaborated to overcome barriers, from conception to completion.

---

## 🧠 Case Study: C-SMC (Cognitive Sliding Mode Control)

The research theme constructed and verified using the above workflow is as follows:

### Theme Overview
We redefined the panic phenomenon of "mind going blank" as a "fall of a bistable system" in control engineering terms, and established a theory for a "mental airbag" to prevent this using robust control (Sliding Mode Control).

### 🏆 Final Artifact
# [📄 Read the Paper: C-SMC Final Version (English)](paper/draft_en_rev9.md)
**[📄 Read in Japanese (Original)](paper/draft_jp_rev9.md)**
*(Verified by NotebookLM & 100-Loop Hell Review)*

- **Paper Title:** Preventing "Blanking Out" with Mathematics: A Theory of Cognitive Sliding Mode Control (C-SMC) for Stabilizing Recall Processes and Suppressing Panic
- **Key Achievements:**
    - Modeling Cognitive Processes using Double-Well Potential
    - Engineering implementation of "Cognitive Flexibility" using Boundary Layer
    - Confirmation of Panic Cancellation (Compliance Rate 99.9%) via Simulation
    - **Deliverable:** [draft_jp_rev9.md](paper/draft_jp_rev9.md) (Final Diamond Master)

## 📁 Structure
- `paper/`: Draft papers (Japanese/English) and PDFs
    - `draft_jp_rev9.md`: **Latest Version (Rev9: Final Diamond Master)**
- `simulation/`: Verification code for control algorithms (Python)
- `docs/`: Thought processes, review reports, concept diagrams
    - `docs/reviews/`: Full texts of "Hell of Peer Review" reports by AI
        - `review_history_archive.md`: Archive of review history from start to completion
        - `peer_review_report_final.md`: Final Peer Review Report
        - `notebooklm_validation_report.md`: Logic Verification Report by NotebookLM
        - `hell_review_rev9.md`: Results of the 100-Loop Hell Review (Rev9)
    - `docs/process_log.md`: Record of AI-Human collaboration process
    - `docs/notebooklm_source_links.md`: Source guide for validation
- `docs/images/`: Workflow diagrams and conceptual images

## 🛠 Technologies Used
- **Control Theory:** Sliding Mode Control (SMC), Lyapunov Stability (Concept)
- **Cognitive Science:** Drift Diffusion Model (DDM), Bistable Potential Model
- **Tools:** Python (NumPy, Matplotlib), LaTeX, Gemini (Writing Partner), NotebookLM (Grounding)

---

## 👤 Author
**Yasuhiro Suzuki**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/%E5%BA%B7%E5%95%93-%E9%88%B4%E6%9C%A8-a61107279/)

---
*Disclaimer: This project contains hypotheses generated through dialogue with AI and is not based on actual clinical data. It is a "logical experiment" to explore the applicability of engineering methods to cognitive science.*
