 wrong access methon and Cross-site Request Forgery:
<form action="add/" method = "get">
templates/cyber/index.html line 20
Fix: line 21 
also in cyber/views.py line 33 wrong method is used. 
fix: line 34


Broken access control: 
cyber/views.py line 17 user is able to delete any note, even not being the creatore of it. 
Fix: line 22, only the user that created the note can delete it 


Injection: 
cyber/views.py line 43 
fix: line 44 

Security misconfiguration: project/settings.py line 50 
missing CsrfViewMiddleware that is responsible for checking scrf token for all post requests. 
also the security key is stored in settings.py and not in env file project/settings.py line 23

Vulnerable and Outdated Components: 
used vulnerable compnent project/settings.py line 41 djangoo
has a critical vulnerability. 
fix: the same line, commented it out. Since it is not even a package that is used 