veryacademy-sql-tools
==================
A simple middleware tool for analyzing Django ORM SQL execution. You can learn how to build this middleware package on our course at Udemy. 

# Usage
Add the follow line of code to your middleware in your project settings.py file.
```
veryacademy-sql-tools.middleware.new_middleware
```

# How it works
The tool uses Django built in features to inspect the SQL genrated from queries executed by the application. 3rd party tools are used to format and highlight the SQL presented in the terminal window.