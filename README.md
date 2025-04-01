# X-Twitter-Data-Pipeline

## Description
This project is a data engineering pipeline that extracts tweets from X (Twitter), saves them as CSV files using Apache Airflow, and loads the data into AWS for storage and further processing. Built with Python, this pipeline automates the process of collecting and managing social media data efficiently.

## Required Tools and Libraries
- **Python 3.9+** - Core programming language for scripting and pipeline logic
- **Apache Airflow 2.5+** - Workflow orchestration for scheduling and managing the pipeline
- **AWS SDK (boto3)** - Python library for interacting with AWS services (e.g., S3)
- **Tweepy** - Python library for accessing the X (Twitter) API to extract tweets
- **Pandas** - Data manipulation and CSV file handling

## Features
- Automated tweet extraction from X (Twitter) using the Twitter API
- Scheduled workflows with Apache Airflow to run extraction and loading tasks
- Storage of tweet data in CSV format for easy access and analysis
- Seamless integration with AWS (e.g., S3) for scalable data storage

## Installation
1. Clone the repository: `git clone https://github.com/Ashutosh-Jarag/X-Twitter-Data-pipeline.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Airflow:
   - Initialize the Airflow database: `airflow db init`
   - Start the Airflow webserver: `airflow webserver --port 8080`
   - Start the Airflow scheduler: `airflow scheduler`
4. Configure AWS credentials (e.g., via `aws configure` or environment variables)
5. Update the `dags/x-dag.py` file with your Twitter API keys and AWS bucket details

## Usage
1. Place the DAG file (`x-dag.py`) in your Airflow `dags` folder
2. Access the Airflow UI at `http://localhost:8080` to trigger or schedule the pipeline
3. Monitor the pipeline execution and check the CSV output in your specified AWS S3 bucket

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
MIT License
