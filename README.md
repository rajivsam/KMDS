<p align="center">
  <a href="https://kmds.readthedocs.io/en/latest/">
    <img width="460" height="300" src="https://raw.githubusercontent.com/rajivsam/KMDS/main/images/kmds_logo_resized.jpg" alt="KMDS Logo">
  </a>
</p>

<h1 align="center">Knowledge Management for Data Science (KMDS)</h1>

<p align="center">
  <strong>Capture, organize, and reuse knowledge from your data science experiments.</strong>
</p>

<p align="center">
  <a href="https://zenodo.org/doi/10.5281/zenodo.10695270"><img src="https://zenodo.org/badge/753950832.svg" alt="DOI"></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License"></a>
  <a href="https://kmds.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/kmds/badge/?version=latest" alt="Documentation Status"></a>
</p>

---

## 🌟 What is KMDS?

KMDS is a Python-based tool designed for systematic knowledge management in data science projects. It helps you document the incremental process of experimentation, including context, decisions, and rationale, ensuring that valuable insights are not lost over time.

### The Problem It Solves

Data scientists live by experimentation. However, the context and rationale behind each experiment are often documented in an ad-hoc manner. When it's time to revisit a question or build upon previous work, it's difficult to piece together the research and its results. KMDS addresses this by providing a structured way to log your findings.

🎥 **Watch a quick overview of KMDS:** [YouTube Video](https://www.youtube.com/watch?v=n7gE6bfLWtI)

---

## ✨ Key Features

- **Structured Logging:** Log findings from your exploratory data analysis, data representation, and modeling phases.
- **Knowledge Base Export:** Export your knowledge base to communicate your findings to your team or management.
- **Integration with Generative AI:** Use generative AI tools like NotebookLM to create reports, videos, and other documentation artifacts from your exported knowledge base.
- **Process Agnostic:** Complements process guidelines like CRISP-DM and semantic vocabularies like OpenML by capturing the "why" behind your data science tasks.

---

## 🚀 Getting Started

### 1. Installation

Install KMDS in your Python environment:

```bash
pip install kmds
```

### 2. Usage

As you work through your analysis, log your findings to `kmds`. Here's a basic workflow:

1.  **Import KMDS:**
    ```python
    from kmds import KnowledgeManagement
    ```

2.  **Initialize the Knowledge Base:**
    ```python
    km = KnowledgeManagement()
    ```

3.  **Log Your Findings:**
    ```python
    km.log_finding("My observation during EDA", "This is what I found...")
    ```

4.  **Export Your Knowledge Base:**
    ```python
    km.export("my_project_knowledge_base.txt")
    ```

5.  **Generate Reports:**
    Point a generative AI tool to your exported knowledge base to create reports, presentations, and other documentation.

---

## 📚 Examples of Use

This repository includes two detailed examples:

-   **Analytics Example:** Evaluates the effectiveness of a ticket resolution help desk.
    -   [Notebooks](examples_of_use/analytics)
    -   [Video Summary](https://www.youtube.com/watch?v=zmm0O4_fK_c)
    -   [Infographic](examples_of_use/analytics/usecase_overview_mindmap.png)

-   **Machine Learning Example:** Uses Principal Component Analysis (PCA) to summarize online store sales activity.
    -   [Notebooks](examples_of_use/machine_learning)
    -   [Infographic](examples_of_use/machine_learning/ml_infographic_kmds.png)

---

## 🤝 Contributing

We welcome contributions! If you have an idea for a new feature or would like to report a bug, please open an issue. If you'd like to contribute code, please fork the repository and submit a pull request.

---

## 📄 License

This project is licensed under the Apache 2.0 License. See the [LICENSE](https://www.apache.org/licenses/LICENSE-2.0.txt) file for details.

---

## 📞 Contact

If you have questions or are interested in the following, please [schedule a meeting](https://calendly.com/rajiv-sambasivan/help-with-kmds-feature):

-   Help with a data analysis task for your use case.
-   Developing a custom ontology-based solution.
-   Integrating KMDS with other tools in your data science stack.