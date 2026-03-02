# 02\_PROMPTING [​](#_02-prompting)

  

## INIT [​](#init)

`Read _TEMP/CLAUDE.md for project context. Development principles: Make minimal, surgical edits—use existing systems and avoid new dependencies unless absolutely necessary. Warn me before any changes that could break functionality or layouts. Don't create user guides unless I ask. If our conversation becomes very long or you notice degraded recall of earlier context, let me know so we can start a fresh session. Our dev server is already running.`

```
<X Read 00_research\12steppers-analysis.md and 00_research\PS01-Implementation-Guide.md we will be developing this as an application in this root directory. For the application development we will be using _TEMP\AUTO-CREATE.md Lets walk though this one phase at a time and make appropriate updates so our development comes together correctly and without issues. Ask me any questions you may have so we can develop this correctly and efficiently. Strictly ask me one question at a time so we can update the documents for development. 

<X
```
Email: admin@powerfulsilence.com
Password: devpassword123

> Ask me any questions you may have so we can develop this correctly and efficiently. Strictly ask me one question at a time so we can create this as a markdown file. Break it up into bite sized development phases. Create it in the \_TEMP directory as \_\_\_.md

CURRENT DIRECTORY: cd /home/highlineadventur/public\_html/`[PATH]`

` Update _TEMP/CLAUDE.md for project status and context regarding our developments. Revise the markdown file to include only essential development specifications, information, and development guidelines. Keep the file under 1000 lines. `

## LOCAL DEV [​](#local-dev)

Terminal 1 - Backend: `venv\Scripts\activate && venv\Scripts\uvicorn main:app --reload --host 127.0.0.1 --port 8001`

Terminal 2 - Frontend: `cd c:\Users\icos\00_DEPLOY\[PATH] && python -m http.server 3020`

## GIT [​](#git)

git pull

git add . && git commit -m "general commit" && git push

## PRODUCTION DEPLOYMENT [​](#production-deployment)

*   \[x\] cd c:\\Users\\icos\\00\_DEPLOY\\`[PATH]` && deploy-dataspur.bat

## Deploy and restart the server: [​](#deploy-and-restart-the-server)

## CLAUDE FLOW "claude-flow v2.5.0-alpha.141" [​](#claude-flow-claude-flow-v2-5-0-alpha-141)

TERMINAL 1 # Terminal 2 (Docker/Swarm):

\[DIRECTORY\] - cd /mnt/c/Users/icos/00\_DEPLOY/highlineadventures.co/ops

\[BUILD-DOCKER\] - docker build -t claude-flow-env .

\[RUN-DOCKER\] - docker run -it --rm -v $(pwd):/home/claude/workspace claude-flow-env

\[MCP-AGENTS\] - claude mcp add claude-flow -- npx claude-flow@alpha mcp start

\[HIVE-MIND-WIZARD\] claude-flow hive-mind wizard

:: - \`PROMPT \`

> > You can run the regular instance of Claude code in parallel with this. Use the hive for large complicated tasks, use Claude code for specific singular tasks

## CLEANING UP SESSIONS [​](#cleaning-up-sessions)

claude-flow hive-mind sessions claude-flow hive-mind stop

## REMOVE ALL SESSION FILES [​](#remove-all-session-files)

rm -rf .hive-mind/sessions/\*

## RESUME SESSION (IF LOST) [​](#resume-session-if-lost)

claude-flow hive-mind sessions claude-flow hive-mind resume --claude claude-flow hive-mind resume session-1767902482678-ggqsu1y8t --claude

*   \[O\] `Review _TEMP/___.md we will be deploying these developments to cpanel for production using the deploy-all.bat script. Walk me though any database migrations that need to be performed. I prefer to upload a .sql file in myphpadmin, or run a query.`

* * *

* * *

## TEMPLATE: [​](#template)

Create this as a markdown file. Break it up into bite sized development phases. Create it in the \_TEMP directory as \_\_\_.md

`Please read _TEMP/CLAUDE.md for project context. Development principles: Make minimal, surgical edits—use existing systems and avoid new dependencies unless absolutely necessary. Warn me before any changes that could break functionality or layouts. Don't create user guides unless I ask. If our conversation becomes very long or you notice degraded recall of earlier context, let me know so we can start a fresh session. Our dev server is already running. Also, Review _TEMP/___.md we will be continuing development of this one phase at a time. Keep the document updated with our progress as we go, so we can pick up from where we left off. Verify documentation is updated and complete. This should be the last thing that you say.`

Review _TEMP/_\_\_.md we will be continuing development of this one phase at a time. Keep the document updated with our progress as we go, so we can pick up from where we left off.

Update _TEMP/_\_\_.md with our current development progress so that we can pick up from exactly where we left off. Include any helpful development notes, information, specification, of findings that will assist us as we continue development at another time.

Review \*TEMP/\_\_\_.md we will be deploying these developments and updates. For database migrations, if there are any, I would prefer to upload a .sql file to myphpadmin. The rest should be deployed via "deploy-all.bat" Please review the developments for deployment, let me know if you foresee any issues, what migrations may or need to be uploaded, and if "deploy-all.bat" will upload all necessary files.

I would like to add a new page and navigation link for a sub-navigation under "System Info" Lets call this page, "\*\*" on that page I want to publish the content we have for TEMP/_**.md so that we can refer back to it, and update it accordingly if new developments are made.I would like update TEMP/**_.md with our current development and progress. Please include all information from the file.

* * *

## DB/API/DEV-SPECS [​](#db-api-dev-specs)

*   12steps.powerfulsilence.com

FTP Username: 12steps@powerfulsilence.com
FTP Password: Superculture1@
FTP server: ftp.powerfulsilence.com
FTP & explicit FTPS port:  21
FTP server: /home/powerfulsilence/public_html/12steps.powerfulsilence.com
FTPS port: 21
Explicit path (This has already been set in the credentials the path is already fixed, simply deploy to /)

User: 12steps-user
Database: 12setps
Password: Superculture1@

*   \[API\]

*   * * *
    

* * *

## STYLE GUIDE [​](#style-guide)

*   \[o\] Color Pallet: --deep-mocha: #402B2Aff; --grey: #7F7A7Dff; --taupe-grey: #705D5Fff; --taupe: #A38C85ff; --dusty-taupe: #9F7768ff; --clay-soil: #6F3826ff; --rosy-taupe: #C59B87ff; --toffee-brown: #9B654Eff; --blue-slate: #54687Aff; --smoky-rose: #83645Fff;

* * *