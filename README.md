# jira_worklog_automation
Jira ticket task tracker



Step 1. Clone repository 
```
https://github.com/rapiinel/jira_worklog_automation.git
```

Step 2. Create a new virtual environment
```
python -m venv jira_worklogs
```

Step 3. Activate your virtual environment
```
source jira_worklogs/bin/activate # Linux
.\jira_worklogs\Scripts\activate # Windows 
```

Step 4. Install dependencies and add virtual environment to the Python Kernel
```
python -m pip install --upgrade pip

# This is only needed if you are using anaconda jupyter notebook
pip install ipykernel
python -m ipykernel install --user --name=jira_worklogs
```

Step 5. Check the source files
  1. Jira Links
  2. Worklogs entry 


> **Note**
> Make sure the jira worklogs entry follow the format we have discussed in the salesops meeting
