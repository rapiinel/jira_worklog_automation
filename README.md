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
.\jira_worklogs\Scripts\activate # Windows 
```

Step 4. Install dependencies and add virtual environment to the Python Kernel
```
python -m pip install --upgrade pip
pip install -r requirements.txt 
```
```
# This is only needed if you are using anaconda jupyter notebook
pip install ipykernel
python -m ipykernel install --user --name=jira_worklogs
```

Step 6. Check the source files if they are updated/correct
  1. Credentials
  2. Worklogs Entry Template

Step 7. Run jira worklogs script
```
python LM_worklog_rest_api.py -f "Worklog Entry Template.xlsx" --start_date "YYYY-MM-DD" --end_date "YYYY-MM-DD"
```

> **Note**
> Make sure the jira worklogs entry follow the format we have discussed in the salesops meeting
> If your repository is already in your local system, you can skip to step 3
