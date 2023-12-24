# Dienstplan App

## Overview
Dienstplan App is a Python-based application designed to find the optimal worker allocation given the requirements
1. the processes which need to be executed
2. the number of workers needed for each process
3. the availabilities of the workers
4. the processes each worker is able to execute
for each day of the week.

Built with Kivy, it offers a user-friendly interface for uploading an Excel file with the requirements and downloading the corresponding optimal worker allocation as a csv.

### Input Excel
The input Excel must have format .xlsx and following worksheets. Naming and capitalization of letters must be identical, otherwise the code won't work.

1. "Qualifikationen"

The column Mitarbeiter contains the workers to be allocated. The column process_n determines whether the respective worker is able to execute process_n ("Ja") or not ("Nein").

| Nr. | Mitarbeiter | process1 | process2 | process2 | ... | 
| --- | ----------- | -------- | -------- | -------- | --- |
| 1   | worker1     | Ja/Nein  | Ja/Nein  | Ja/Nein  | ... |
| 2   | worker2     | Ja/Nein  | Ja/Nein  | Ja/Nein  | ... |
| 3   | ...         | ...      | ...      | ...      | ... |

2. "Arbeitstage"

The column Mitarbeiter contains the workers to be allocated. The column day_n determines whether the respective worker will be working on day_n ("Ja") or not ("Nein"). It is assumed that each worker has the capacity to perform exactly one process in one day.

| Nr. | Mitarbeiter | day1     | day2     | day3     | ... | 
| --- | ----------- | -------- | -------- | -------- | --- |
| 1   | worker1     | Ja/Nein  | Ja/Nein  | Ja/Nein  | ... |
| 2   | worker2     | Ja/Nein  | Ja/Nein  | Ja/Nein  | ... |
| 3   | ...         | ...      | ...      | ...      | ... |

3. "Benötigtes Personal"

The column Prozesse contains the processes to be executed. The column day_n determines how many workers (n_ij) are needed to execute the process on day_n.

| Prozesse | day1 | day2 | day3 | ... | 
| -------- | ---- | ---- | ---- | --- |
| process1 | n11  | n12  | n13  | ... |
| process1 | n11  | n12  | n13  | ... |
| ...      | ...  | ...  | ...  | ... |

### Output csv

The output csv contains the optimal shift such that the number of allocated workers and executed processes is maximised. Column Tag specifies the day on which the worker from column Mitarbeiter executes the process from column Prozess.

If column Mitarbeiter has entry N/A it means that there all workers who are able to execute the respective process are already busy that day. If column Prozess has an entry N/A it means that the respective worker is not assigned to any process that day.

| Tag  | Mitarbeiter | Prozess  | 
| ---- | ----------- | -------_ |
| day1 | worker1     | process1 |
| day1 | worker2     | process3 |
| day2 | N/A         | process1 |
| day2 | worker1     | N/A      |
| ...  | ...         | ...      |

## Features
- Upload Excel Files: Easily upload data from Excel files.
- Data Processing: The data is processed using graph algorithms to find the perfect worker process allocation.
- Save Functionality: Save the processed data in a csv file.

## Getting Started

### Prerequisites
- Python 3.x
- pip (Python package manager)
- [Any other prerequisites...]
