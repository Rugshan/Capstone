# Here are some instructions for the Git/GitHub repository:

## OS

I'm using Ubuntu as my developmental environment.

## Install Git

You can install Git through the terminal. I personally use the latest version (matching the one I use on Windows)

```sudo add-apt-repository ppa:git-core/ppa```

```sudo apt update```

```sudo apt install git```

## Install Git CLI (For Authentication)

If the command 'curl' is not found, you can install it by using the command the terminal gives you to install it.

```curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg```

```echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null```

```sudo apt update```

```sudo apt install gh```

## Generating a Personal Access Token

1. Go to your GitHub account.
 
2. Settings -> Developer Settings -> Personal Access Tokens

3. Generate New Token

4. Follow the below settings:

    - Note: (Name the token something useful, like Virtual Machine)
    - ``Expiration Date``: I set mine to expire in December, you can set it to the end of this semester.
    - `Enable 'repo'` (and all of the boxes under repo)
    - `Enable 'workflow'`
    - `Enable 'read:org'`
    - `Enable 'gist'`

5. Make sure you `copy the new token` and *put it in a sticky note for now*, otherwise you'll just have to press the regenerate button if you lost the token.

## Authenticating Git

1. Open your terminal on Ubuntu.

2. Enter the command ```gh auth login```

3. Select `HTTPS`

4. Enter `Y` when it asks if you want to authenticate with your GitHub credentials.

5. When it asks for your access token, `paste your personal authentication token`. If it asks for a username, use your GitHub username.

## Clone the GitHub Repository

1. Terminal to a directory you wish to clone the repository too. You could just clone it into the home directory and a folder with the repository will be created.

2. Use ```git clone https://github.com/Rugshan/Capstone.git``` this clones the main branch of the repository.

3. Create a local developer branch with ```git checkout -b developer```. 'checkout' is used to switch between branches, and '-b' is used to create a new branch and switch to it at the same time.

4. Set up tracking for the first time with ```git branch --set-upstream-to=origin/developer``` this tracks the developer branch in the remote (remote is called origin).

5. Use ```git pull``` to make sure all the files are pulled from the repository.

## Visual Studio Code:

Install the `GitLense` extension in the Extensions Tab. Adds some Git-related features. Such as, showing last commits for each line, showing the current branch on the bottom right, etc.

--------------------------------

# Repository Rules and Usage

## Branch Structure

- **main branch** is for working versions of the code
 
- **developer branch** is for development. After a developer branch is confirmed to be working, it can be pushed and merged into main.

- **feature branches** we `do not work on the developer or main branches directly`. When developing, we `create new branches from the developer branch to make changes`.

## Creating and Switching to a Feature Branch

First, switch to the developer branch with ```git checkout developer```

Then, checkout to a new branch named according to what you're currently working on with ```git checkout -b [NEW BRANCH NAME]```. Example, the name could be 'add-turning', 'update-documentation', 'solve-bugX'.

## .gitignore

I'm using Visual Studio Code. If you use other technologies, IDEs or software, make sure to **update the .gitignore** by appending corresponding .gitignore templates.

The current .gitignore contains a Python template and Visual Studio Code template. .gitignores are useful for excluding unnecessary or sensitive files from being pushed to the remote repository.

This site contains some templates: https://www.toptal.com/developers/gitignore

## Committing / Pushing:

Example of adding a feature on a local Git repository:

- ```git checkout developer``` to switch to developer

- ```git checkout -b [NEW FEATURE BRANCH NAME]``` to create and switch to a new feature branch. Mine is called *add-movement-directory* so: ```git checkout -b add-movement-directory```

- ```code .``` to open the current directory in Visual Studio Code (you may or may not have this function, you could just open the folder in Visual Studio Code)

- Now I'll create a folder called '*movement*' in src/ for wheel-motor related functions. I'll also create a *movement_controls.py* file with some comments.

- ```git status``` to see the current branch you are on and the untracked/upstaged files (files which have been modified). Make sure your .gitignore is working as intended and not showing files that you want it to ignore.

- ```git add [FILES]``` to stage specific files. ```git add -A```  to stage all files seen in *git status*

- ```git status``` again to see staged files (now in green)

- ```git commit -m "MESSAGE"``` to commit staged changes. The *-m parameter must be there*, or the terminal will force you to write the commit message some other way. The double quotations must be used. Here, I used ```git commit -m "created movement functions directory"```

- ```git push -u origin [FEATURE BRANCH NAME]``` to push the commit/changes to remote (origin). Here, I used ```git push -u origin add-movement-directory``` for my new feature.

## Merges/Pull Requests

- In GitHub, go to the main page (`<> Code` Button). 

- You can then change the view from (main) to any other branch to see that branch. For merges/pull requests, `press the 'branches' button` beside the view changer.

- Find the branch you just pushed to. Press the create `new pull request` button. (I pushed to add-movement-directory, so I'd create a pull request for that).

- Make sure to `set the base repository as developer` (we want to merge into developer).

- Add an `appropriate title and more context in the comment` if needed. 
    - You `can add the hashtag number of a specific issue` you've addressed in the title to automatically link to it. I.e. my title could be 'Solved #3' to address the issue #3 in the issues tab.
    - You can also `add labels or assignees` on the right side. 

- When done filling out the pull request, `press 'create pull request'`.

- If you forgot to change the base repository like I do all the time, you can edit the pull request. `After review, you can press merge pull request and confirm merge.`

- Since this is just a feature branch, and we have merged into developer, `press delete branch (our feature branch)`.


