# A script for find the labels with specific keywords from JIRA
## Requirement:
### Pyton 3.x
https://www.python.org/downloads/

## Usage:
### 1. Save the account info into the file named "account.json".
This file will be created automatically after first run.
Please modify it after it appeared.

### 2. Build a filter to find all of the labels in JIRA.
Example,
https://idarttest.mot.com/issues/?filter=136250

### 3. Change the filter_id in the file named "find_labels.py" to the real value of the filter build on 2#.
e.g. The filter_id of the example on 2# is 136250.

### 4. Run the script with the keywords you would find as arguments
labels.py <string1> [<string2>,...]
e.g. "labels.py top block" will find all of the labels including "top" or "block".

### 5. The result will be stored in the file named "labels.txt" and "labels_list.txt" with different format.
