# Financial Data Analysis API
## Table of Contents
- [Project Description](#project-description)
- [Tech Stack](#tech-stack)
- [Running the Code Locally](#running-the-code-locally)
  - [Prerequisites](#prerequisites)
  - [Steps to Run](#steps-to-run)
- [API Endpoints](#api-endpoints)
  - [`/financial_data`](#financial_data)
  - [`/statistics`](#statistics)
- [Testing](#testing)
  - [Unit Tests](#unit-tests)
- [Future work](#future-work)
    
## Project Description
This Python-based project, covered by comprehensive unit test cases, fetches and analyzes financial stock data from AlphaVantage over specified periods. It enables users to retrieve average daily open prices, closing prices, and volumes for selected stocks.

Some future work is listed at the end of the README section, which can be undertaken to improve scalability, robustness, and quality.

## Tech Stack
- **Programming Language**: Python 3
- **Web Framework**: Flask
- **Database**: SQLite
- **External API**: AlphaVantage

## Running the Code Locally

### Prerequisites
- Python 3.12.2_1

### Steps to Run
1. Clone the repository to your local machine.
2. Navigate to the project directory using Pycharm IDE.
3. Set the AlphaVantage API key as an environment variable:
   1. Open PyCharm and navigate to the project where you need the environment variable.
   2. Go to "Run" -> "Edit Configurations".
   3. Find the script or configuration you're running.
   4. In the "Environment variables" field, click the browse button (three dots).
   5. Click the "+" icon to add a new environment variable.
   6. Enter **`ALPHAVANTAGE_API_KEY`** as the name and your actual API key as the value.
   7. Apply the changes and close the dialog.
4. Run `python get_raw_data.py` to get the financial data from AlphaVantage, and insert the data to local SQLite db.
5. Spin up the API by runnig `app.py`, and you can use curl command in the below `API Endpoints` section to retrieve data.
  
## API Endpoints

### `/financial_data`
- **Method**: GET
- **Description**: Fetches historical financial data including open, close prices, and volume for specified stock symbols over a given date range.
- **Parameters**:
  - start_date (required): The starting date for fetching the financial data (format: YYYY-MM-DD).
  - end_date (required): The ending date for fetching the financial data (format: YYYY-MM-DD).
  - symbols (required): A comma-separated list of stock symbols for which financial data is to be fetched (e.g., AAPL,IBM).
- **Example Request**:
  ```sh
  curl -G "http://127.0.0.1:5000/financial_data" \
    --data-urlencode "start_date=2023-01-01" \
    --data-urlencode "end_date=2023-01-31" \
    --data-urlencode "symbols=IBM,AAPL"

### `/statistics`
- **Method**: GET
- **Description**: Calculates and returns the average daily open price, closing price, and volume for the specified stock symbols within a given date range.
- **Parameters**:
  - `start_date` (required): Start date of the period (format: YYYY-MM-DD).
  - `end_date` (required): End date of the period (format: YYYY-MM-DD).
  - `symbols` (required): Comma-separated list of stock symbols (e.g., AAPL,IBM).
- **Example Request**:
  ```sh
  curl -G "http://127.0.0.1:5000/statistics" \
  --data-urlencode "start_date=2023-01-01" \
  --data-urlencode "end_date=2023-01-31" \
  --data-urlencode "symbols=IBM,AAPL"

## Testing
### Unit Tests
- To ensure API functionality, including optional and required parameters handling, unit tests are implemented. You can find the unit tests in the `test_financial_data_api.py`. Run them using:
  ```sh
  python3 -m unittest

## Future work
1. In the development and production environment we will need to store API Keys more securely. Below are some best practices for securely storing API keys:
   - Local Environment:
     - Set the AlphaVantage API key as an environment variable
   - Production Environment:
     - **Cloud Provider Key Management Services (KMS):** Services like AWS KMS, Azure Key Vault, and Google Cloud KMS allow creation and management of cryptographic keys for application security.
     - **Secret Management Services:** AWS Secrets Manager, for instance, enables rotation, management, and retrieval of secrets, with applications advised to dynamically fetch these at runtime.
     - **CI/CD Pipeline:** Securely store API keys as variables in Git repositories with restricted access, and inject these secrets into applications (e.g., `get_raw_data.py`) via CI/CD pipelines like GitLab.
3. Implement robust error handling and data validation to ensure data integrity and data quality.
4. Use caching and request batching to optimize API calls and reduce load on the database.





