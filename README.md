
# Cyber Security Base 2024: Project 1


## Installation: 
1.	Install the required dependencies as outlined in the course [installation guide](https://cybersecuritybase.mooc.fi/installation-guide): 
2.	Clone the repository

3.	Run: `python3 manage.py runserver` to start the server 

4.	Access the website by typing `localhost:8000` in your browser

5.	Log in with the default accounts:


    | Username | Password |    
    |:--------:|:--------:|
    | alice    | redqueen |
    | bob    | squarepants |




If the login fails, you can initialize the database with this command:

```
python3 manage.py migrate
```

Then you can create a new user through the registration form provided in the application interface.



Project contains a number of cybersecurity vulnerabilities from the [OWASP Top 10](https://owasp.org/www-project-top-ten/ ) 2021 list. 



## Flaws:


### Flaw 1: SQL Injection

#### Location: [cyber/views.py line 39](https://github.com/linaova/cyberproject/blob/474eb190fce1b5394946d40ffe7bf14db081ea35/cyber/views.py#L42)




#### Description: 
This vulnerability occurs, when variables are directly used in SQL statements, without proper validation. This allows attackers to alter the queries to access database entities they are not authorized to access. In this application, this is shown with `user_id` variable, that is just passed to the query. Attacker could have used Union operator and accessed all notes in database.

#### Fix: [cyber/views.py line 40](https://github.com/linaova/cyberproject/blob/474eb190fce1b5394946d40ffe7bf14db081ea35/cyber/views.py#L43)



Instead of using raw SQL query, I implemented Django’s own Object-Relational Mapping (ORM) system. It was useful, because Django abstracts SQl commands into python code and automatically handles input sanitization. It does that by escaping dangerous characters, that could be interpreted as code.



### Flaw 2: Broken Access Control

#### Location: [cyber/views.py line 14](https://github.com/linaova/cyberproject/blob/9689c8553839cab16a3453d8fdb12b1e9a50b183/cyber/views.py#L14 )


#### Description:
Broken Access Control vulnerability occurs, when users can access things, they are not supposed to be able to, for example add or remove or do other things they are not authorized to. In this application deleteView function: 
`Note.objects.get(pk=request.POST.get('id'))` does not take into account who is the owner of the note, it only needs to know the id of the note. This means, that user could potentially delete any note just by guessing its’ id. 

#### Fix: [cyber/views.py line 19](https://github.com/linaova/cyberproject/blob/9689c8553839cab16a3453d8fdb12b1e9a50b183/cyber/views.py#L19)


The implemented fix `Note.objects.get(pk=request.POST.get('id'), user = request.user)` on the other hand checks if the logged in user is the owner of the note, they are trying to delete. This ensures, that users can perform this action strictly on the notes they own. 



### Flaw 3: Cross-site Request Forgery (CSRF)

#### Location: [cyber/templetes/cyber/index.html line 20](https://github.com/linaova/cyberproject/blob/9689c8553839cab16a3453d8fdb12b1e9a50b183/cyber/templates/cyber/index.html#L20)


#### Description: 
With Cross-site Request Forgery (CSRF) vulnerability, it is possible to send request from another source to the application without proper authentication. This makes it possible to access data or services unauthenticated. For instance, in this application form for adding notes, does not have any csrf protection, making it easy to corrupt database for example. 


#### Fixes: 
[cyber/templetes/cyber/index.html line 20](https://github.com/linaova/cyberproject/blob/9689c8553839cab16a3453d8fdb12b1e9a50b183/cyber/templates/cyber/index.html#L21)

[project/settings.py line 50](https://github.com/linaova/cyberproject/blob/9689c8553839cab16a3453d8fdb12b1e9a50b183/project/settings.py#L50)



Integrating `csrf token` to all form is an easy method to mitigate csrf-attacks. So I added the `csrf token`, as you can see in delete- and logout-forms as well. Now Server verifies each post request with the token to ensure that it is the same user making a request. Additionally, in application settings middleware I added `CsrfViewMiddleware`, that automatically checks if sent post request has a token and cancels the request if it does not. With it, even if the developer forgets to add the token to the form, it will quickly be noticed. 



### Flaw 4: Security Misconfiguration 

#### Locations:
[project/settings.py line 23](https://github.com/linaova/cyberproject/blob/9689c8553839cab16a3453d8fdb12b1e9a50b183/project/settings.py#L23 )

[project/settings.py line 26](https://github.com/linaova/cyberproject/blob/9689c8553839cab16a3453d8fdb12b1e9a50b183/project/settings.py#L26)






#### Description: 
Security misconfiguration gives attackers and easy target to access private data in the application. For instance, Debug = true in the production provides they with detailed error messages, when they are trying to break our application so accessing stack traces or database dumps is the same as giving strait forward clues, that will exploit further attacks. 
 The same goes with secret key stored in public. It is responsible for cryptographic signing, creating hashes and csrf_tockens, and storing it in document that is easily accessed makes tokens and passwords easily guessable. 


#### Fix: [project/settings.py line 27](https://github.com/linaova/cyberproject/blob/d18a2914fa90a2038a08aab55155f0c2c2c1bc53/project/settings.py#L27)


By setting DEBUG = False and ensuring sensitive settings are not exposed, the application reduces the risk of such informational leakage. Furthermore, storing sensitive configuration details like the security key outside of the public codebase, in an environment file that is added to .gitignore, helps in securing access credentials and other critical settings from being exposed in version control.

### Flaw 5: Identification and Authentication Failures

#### Description:
Effective authentication systems are important so that attackers could not impersonate the user. This vulnerability includes using basic passwords or storing them as a plain text. In this application currently when registering the user there are not many requirements for the password, meaning user may use as simple password as they wish, meaning hackers could easily guess it. Also, session does not have any time out. Meaning unless user intentionally log out, they will stay logged in even after closing the browser. This is a critical security risk especially, when application is used on public computers. 

#### Fixes:
[project/settings.py line 90](https://github.com/linaova/cyberproject/blob/9689c8553839cab16a3453d8fdb12b1e9a50b183/project/settings.py#L90)

[project/settings.py line 128](https://github.com/linaova/cyberproject/blob/9689c8553839cab16a3453d8fdb12b1e9a50b183/project/settings.py#L128)




More strict password policies and managing session lifetimes rapidly enhances the security. Django's AUTH_PASSWORD_VALIDATORS allow you to enforce complex passwords that resist common attacks such as brute-force. The session management settings secures session cookies and ensures, that sessions expire when the browser is closed.
