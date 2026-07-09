"""
Data Helper (Pandas)
====================
WHY THIS FILE EXISTS:
    Pandas is the industry standard for data analysis in Python.
    In automation, we use it to:
      - Read test data from CSV/Excel files (data-driven testing)
      - Analyze test results (pass/fail trends, durations)
      - Query and filter data like SQL but in Python

WHAT YOU LEARN HERE:
    - pd.DataFrame       : Create a table of data
    - pd.read_csv        : Load test data from a CSV file
    - df.to_csv          : Save data to CSV
    - df[condition]      : Filter rows (like SQL WHERE)
    - df.groupby()       : Group data (like SQL GROUP BY)
    - df.merge()         : Join two tables (like SQL JOIN)
    - df.apply(lambda)   : Transform data row by row
"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)


def load_test_data_from_csv(file_path):
    """
    Read test data from a CSV file and return it as a list of tuples.
    This is perfect for feeding into @pytest.mark.parametrize!

    Example CSV (test_data/users.csv):
        first_name,last_name,role
        Alice,Smith,admin
        Bob,Johnson,user

    Usage:
        data = load_test_data_from_csv("test_data/users.csv")
        @pytest.mark.parametrize("first_name,last_name,role", data)
    """
    df = pd.read_csv(file_path)
    logger.info(f"Loaded {len(df)} rows from {file_path}")
    # Convert DataFrame rows to a list of tuples for parametrize
    return list(df.itertuples(index=False, name=None))


def analyze_test_results(db_helper):
    """
    Query the test_results table and return a Pandas DataFrame.
    This bridges SQL and Pandas — query with SQL, analyze with Pandas.
    """
    rows = db_helper.fetch_all("SELECT * FROM test_results")
    df = pd.DataFrame(rows, columns=["id", "test_name", "status", "duration", "executed_by", "executed_on"])
    logger.info(f"Loaded {len(df)} test results into DataFrame")
    return df


def get_summary_report(df):
    """
    Generate a summary report from test results DataFrame.
    Returns a dictionary with key metrics.
    """
    summary = {
        "total_tests": len(df),
        "passed": len(df[df["status"] == "PASSED"]),
        "failed": len(df[df["status"] == "FAILED"]),
        "skipped": len(df[df["status"] == "SKIPPED"]),
        "avg_duration": round(df["duration"].mean(), 2),
        "slowest_test": df.loc[df["duration"].idxmax(), "test_name"],
        "fastest_test": df.loc[df["duration"].idxmin(), "test_name"],
    }
    logger.info(f"Summary: {summary}")
    return summary


def get_results_by_tester(df):
    """
    GROUP BY example — count how many tests each tester ran.
    This is the Pandas equivalent of:
        SELECT executed_by, COUNT(*) FROM test_results GROUP BY executed_by
    """
    grouped = df.groupby("executed_by")["test_name"].count()
    logger.info(f"Results by tester:\n{grouped}")
    return grouped


def filter_failed_tests(df):
    """
    WHERE clause equivalent — filter only failed tests.
    This is the Pandas equivalent of:
        SELECT * FROM test_results WHERE status = 'FAILED'
    """
    failed = df[df["status"] == "FAILED"]
    logger.info(f"Failed tests:\n{failed[['test_name', 'executed_by']]}")
    return failed
