# Project Title: Skincare Product Recommender Service

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

This recommender service provides personalized skincare product recommendations based on user-provided skin type information.

## Getting Started <a name = "getting_started"></a>

To set up the project on your local machine for development and testing purposes, follow these steps:

### Prerequisites

Ensure you have the following prerequisites installed:

- Python 3.x
- FastAPI
- Vertex AI

### Installing

Follow these steps to get a development environment running:

1. Clone the repository:
   ```
   git clone https://github.com/seun-beta/skincare-recommender.git
   ```

2. Install dependencies using pip:
   ```
   pip install -r requirements.txt
   ```

3. Set up Google Cloud Platform (GCP) service account credentials:
   - Create a service account in GCP.
   - Generate a key and download the JSON file.
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of the JSON file using `export GOOGLE_APPLICATION_CREDENTIALS="path-to-JSON-file"
`.
 
### Usage <a name = "usage"></a>

Here are instructions on how to use the system:

1. **Determine Skin Type Endpoint:**
   - **Endpoint:** `/determine-skin-type`
   - **Description:** Determines the user's skin type based on provided answers.
   - **Request:** 
       - `oiliness`: How often the skin feels oily.
       - `dryness`: Experience of flakiness or dry patches.
       - `sensitivity`: Reaction of the skin to new products or environmental changes.
       - `hydration`: Frequency of feeling tight or dehydrated skin.
   - **Response:** Returns the determined skin type.

2. **Recommend Products Endpoint:**
   - **Endpoint:** `/recommend`
   - **Description:** Recommends skincare products suitable for a specific skin type.
   - **Request:** 
       - `skin_type`: Skin type determined from previous endpoint.
   - **Response:** Returns a list of recommended skincare products for the given skin type.

3. Ensure the Text Generation Model from Vertex AI is accessible and configured correctly to work with the recommender service.

