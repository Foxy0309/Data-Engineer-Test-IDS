# Solution to Data Analysis Challenge

## Summary
This program processes the given JSON event logs by merging these logs based on timestamps. It then identifies transactions, and summarizes these transactions, which are changes in the balance of savings accounts or credit used of cards.

## Thinking Behind the Implemented Solution

I first had to decide that the `ts` (timestamp) field is the key for aligning records across the different tables, as by doing so, I would be able to list down each data point accurately and align them chronologically. After this realization, all I had to do was to implement it.

## Implementation
The solution is implemented in Python using the pandas library for data manipulation and analysis. The main steps of the solution are as follows:

1. **Load JSON Files**: The program loads JSON files from three directories (`data/accounts`, `data/cards`, `data/savings_accounts`) and normalizes them into pandas DataFrames.

2. **Add Timestamp Columns**: Each DataFrame is augmented with a `timestamp` column derived from its respective timestamp field.

3. **Merge Tables**: The DataFrames are merged on their unique timestamps to create a denormalized view of all tables.

4. **Identify Transactions**: Transactions are identified based on changes in the `set_balance` and `set_credit_used` fields.

5. **Print Results**: The main() fucntion then prints the complete historical views of each table, the denormalized table, and the identified transactions.

## How to Run the Solution in a Docker Container

- Docker must be installed on the system the program is run.
- The JSON files must be present in the respective directories within the `data` directory.

1. **Build the Docker Image**

    Navigate to the `DWH-CODING-CHALLENGE` directory and run the following command:

    docker build -t data-challenge-solution solution


2. **Run the Docker Container**

    docker run -v `the absolute path to the JSON data directory` data-challenge-solution

    For example: `C:/Users/natse/Documents/dwh-coding-challenge/data:/app/data`


