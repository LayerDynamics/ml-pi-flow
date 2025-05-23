# Copilot Instructions
# This file contains instructions for Copilot to follow when generating code.
# It is important to keep this file up to date with the latest instructions and guidelines.


## REQUIRED FOR CONSIDERATION WITH EVERY PROMPT

- **Remote Development** The code is not running here, its running on a raspberry pi 5 8gb with a 512gb nvme m key storage.

## Project Overview
The project consists of several components, each serving a specific purpose. The architecture is designed to be modular and scalable, allowing for easy integration and management of various services. Below is a high-level overview of the components involved:
* **MLflow**: A lightweight, headless MLflow tracking server for managing experiments, models, and datasets.
* **TensorBoard**: A centralized headless TensorBoard server for automatically syncing training runs and visualization logs.
* **Vector Database**: A local embedding store (Qdrant or ChromaDB) for semantic searches, used for datasets or codebases.
* **Data Labeling Interface**: A self-hosted labeling system (e.g., Label Studio) for annotating datasets.
* **Continuous Dataset Validation & Versioning**: A server for automating data validation, profiling, and management (e.g., Great Expectations) integrated into ML pipelines.
* **Dashboard**: A display for metrics and information from all projects, separate from the individual components.
* **Web Portal**: An interactive interface for managing and viewing the projects, accessible locally on the same network.
* **Folder Structure**: A comprehensive folder structure for organizing the various components and their respective files.
* **Architecture Visuals**: Diagrams illustrating the architecture and interactions between components.
* **Documentation**: Detailed documentation for each component, including setup instructions, usage guidelines, and interaction details.
* **Metrics and Info**: Information on how to access and utilize the metrics and data from each component.





## Demeanor and Style
The following are the general guidelines that should be followed when generating code:

----
# 1. **Be concise**: Provide clear and direct instructions to avoid unnecessary verbosity.
# 2. **Be specific**: Clearly define the task and expected output to ensure accurate results.
# 3. **Be consistent**: Maintain a uniform style and structure throughout the code to enhance readability.
# 4. **Be modular**: Write code in a way that allows for easy reuse and modification.
# 5. **Be informative**: Include comments and documentation to explain the purpose and functionality of the code.
# 6. **Be adaptable**: Ensure the code can be easily modified to accommodate future changes or enhancements.
# 7. **Be efficient**: Optimize the code for performance and resource usage.