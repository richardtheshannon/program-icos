# MAIN PROMPTS

Please read CLAUDE.md for project context. Development principles: Make minimal, surgical edits—use existing systems and avoid new dependencies unless absolutely necessary. Warn me before any changes that could break functionality or layouts. Don't create user guides unless I ask. If our conversation becomes very long or you notice degraded recall of earlier context, let me know so we can start a fresh session. Our dev server is already running. 

Also, Review _TEMP\v2-frame-studio-implementation.md we will be continuing development of this one phase at a time. Keep the document updated with our progress as we go, so we can pick up from where we left off. Verify documentation is updated and complete. This should be the last thing that you say. 


> Update _TEMP/CLAUDE.md for project status and context regarding our developments. Revise the markdown file to include only essential development specifications, information, and development guidelines. Keep the file under 1000 lines.

> We will be deploying the changes we have made. Review the files for deployment. Let me know if: - we have database migrations - if we need to restart any services on the server. I will be pushing to github for cpanel deployment. 

> Ask me any questions you may have, strictly one question at a time so we can develop this accurately and efficiently the first time.  

https://program.icos.dev/

new git repository: https://github.com/richardtheshannon/program-icos.git

Subdomain created: /public_html/program.icos.dev

FTP ACCOUNT:
FTP Username: program@program.icos.dev
FTP Password: Superculture1@
FTP server: ftp.icos.dev
FTP & explicit FTPS port:  21
This account is restricted to /home/icos/public_html/program.icos.dev so lets just publish to "/" lets not duplicate the path since its already set. 

Database Created (Postgre)
User: program-user
Database: program
Password: Superculture1@

<X  
<X 
<X 


# LOCAL DEV: PROGRAM
C:\Users\ic0s\Downloads\_obsd\RJS\RJS_icos-ritual\_icos-dev\program-icos-dev

cd C:\Users\ic0s\Downloads\_obsd\RJS\RJS_icos-ritual\_icos-dev\program-icos-dev
py manage.py runserver


# LOCAL DEV: RITUAl
>Open a new PowerShell window and run:
cd C:\Users\ic0s\Downloads\_obsd\RJS\RJS_icos-ritual\_icos-dev\
C:\php\php.exe -S localhost:8081 -t ritual-icos-dev\public\

_icos-dev\ritual-icos-dev
# DEPLOY
cd _icos-dev/ritual-icos-dev && git add -A && git commit -m "V003.0" && git push origin main

<x Review:
_TEMP\00_Research\ActiveCampaign.md


# SETUP DETAILS
https://github.com/richardtheshannon/ritual-icos.git

FTP Username: ritual@icos.dev
FTP Password: Superculture1@
FTP server: ftp.icos.dev
FTP & explicit FTPS port:  21
FTP account is set to " /public_html/ritual.icos.dev" so just deploy to "/"

Database:
User: ritual-user
Database: ritual-dev
Password: Superculture1@


# DATABASE
User: hs1-user
Database: hs1
Password: Superculture1@

FTP_SERVER	ftp.salesfield.net
FTP_USERNAME	hs1@salesfield.net
FTP_PASSWORD	Superculture1@
