% Git Tutorial
% Rami Sayar [@ramisayar](http://twitter/ramisayar)
% May 1st, 2013

## What is git?

Version Control Systems are tools for software engineers to manage their source code over time. They are frequently used to manage different revisions of software projects, to help engineers collaborate and to work together. There has been many systems designed for this tasks, perhaps you may have used one previously such as SVN or CVS. This class will use Git which a recent development and differs significantly from previous VCS you may have used. Git is a Distributed Version Control System (DVCS). It is an evolution from local and central version control systems. Central version control systems such as SVN and CVS maintained a single authoritative copy of your project and it's history in one central location that was accessible to everybody on the project. However, this approach does not scale for large scale development efforts with 10s of concurrent branching efforts. New approaches using distributed version control where developed such as Git and Mercurial. Git was created and designed by Linus Torvalds to handle the incredible quickly paced, highly branched development of the Linux kernel. 

With Git, project members don't get just the latest version of a code base, instead they checkout a full mirror copy of the repository. As a result, you can do local VCS work and still be able to push out the changes in your code base to a central VCS or directly to your peers. Git is designed around the notion of content as opposed to changesets, branching and merging is thus significantly more powerful and easier to use than previous systems. Git is a powerful source code management system in use throughout industry and has led to many startups such as GitHub and BitBucket which expose a Git repository.

## Where do I get git?

You can download git for your operating system using your system's package manager or by downloading an installer from [http://git-scm.com](http://git-scm.com).

If you are on a mac and have either Ports or Brew installed, you can use the terminal to install git via the following commands. 

```
$ sudo ports install git
```

or

```
$ brew install git
```

## How do I use git?
The general preferred method of using git is through a terminal. Git comes with an wealth of command line tools. However, it is possible to use git through a graphical interface but you will be limited to what the tool provides you.

If you are a Windows users, you may be uncomfortable using the terminal. Instead, you can use the [GitHub for Windows Client](http://windows.github.com/). If you are a Mac user, you also have a similar option, [GitHub for Mac](http://mac.github.com/). These tools allow you to do the most of what will be described in the rest of this tutorial however it is recommended you use git through a terminal. It's great practice for future work on the terminal as well (such as your Operating Systems class).

## How does Git Work? 

Historically, source control management software would work by tracking the changes to a base file over time.

![image](http://www.git-scm.com/figures/18333fig0104-tn.png)
[REFERENCE](http://www.git-scm.com/book/en/Getting-Started-Git-Basics#Snapshots,-Not-Differences)

Your local repository consists of snapshots of your files. Git treat your repository as if it were a mini-filesystem and will store references to the current state.

![image](http://www.git-scm.com/figures/18333fig0105-tn.png)
[REFERENCE](http://www.git-scm.com/book/en/Getting-Started-Git-Basics#Snapshots,-Not-Differences)

Everything is local and, as a result, very fast. Your repository can exist entirely within your computer, or be accessible within a LAN, you do not need to get on the Internet. You can literally have git work over network shares (DO NOT DO THIS.)

Everything in git is check-summed and referred to by checksums. You will not be able to hack git to ignore changes in your files. Git will detect every change and it will use hashes everywhere. Git will then refer to files using a hash as opposed to the file name.

Git almost always simply adds data, so it is very hard to mess up your version control system or be unable to recover data or go back in time.

![image](http://www.git-scm.com/figures/18333fig0106-tn.png)
[REFERENCE](http://www.git-scm.com/book/en/Getting-Started-Git-Basics#The-Three-States)

## Creating a new repository

The first step in any project is to create a directory to hold your code and documentation. 

Create a directory:

```
$ mkdir sample-project
```

Change into the directory:

```
$ cd sample-project
```

The next command will tell git to create a hidden folder `.git` in your directory and to start tracking changes to your code. 

```
$ git init

Initialized empty Git repository in /path/to/sample-project/.git/
```

git init comes with some useful extras such as --template which will allow you to use a template repository and add initial files. 

git init --shared allows you to specify repository information if you are sharing a repository with several users. 

You can run the following for more information.

```
git init -h
```

## Adding, Removing and Committing

Assuming you have started writing some code in the directory you created. When you feel your code has reached a useful state, your next step is to add the code to the repository. Let's say you created a README file about your project.

You can run `git status` to see the current status of your repository. 

```
$ git status

# On branch master
#
# Initial commit
#
# Untracked files:
#	README
nothing added to commit but untracked files present
```

You will notice that git is informing you of untracked files. These are the files you just created. To add them to your repository, you have several options using the `git add` command. You don't only add new files, you also add changed files.

```
$ git add path/to/file
$ git add *
```

You can run the following for more information. 

```
git add -h
```

After adding all the files, if you run `git status` again, you will notice that all the files you added are now staged for commit. You will commit this changeset to the repository using the git commit command.

```
$ git commit
```

or

```
$ git commit -m "Commit my file."
[master (root-commit) 47d6aa5] Commit my file.
 0 files changed
 create mode 100644 README

```

The first command will open your default text editor which tends to be either `vi` or `nano`. Refer to online tutorials for how to use `vi`.

After committing your first commit, git has recorded the first content state in the local repository and it refers to this state as the HEAD.

Removing files is simple 

```
$ git rm path/to/file
```

For further reference, if you need to refer to the latest change you can use `HEAD`, the second to last change `HEAD^`, a certain number of changes back `HEAD~n`.


## Branching
The true power in the git approach to version control is branching. Branches are simply diversions in your code changesets. You branch off a certain point in history and add more revision of your code from there. You can revert to another branch that may have gone a completely different direction. You can switch between different branches and take the same code base in other ways. As a note, you will always start on a "master" branch. Creating a branch will not 

```
$ git branch [branch_name]
```

To list all the branches:

```
$ git branch -l

* master
  [branch_name]

```

To delete a branch:

```
$ git branch -d [branch_name]

Deleted branch [branch_name] (was 47d6aa5).

```

To switch from one branch to another, you can use the checkout tool. 

```
$ git checkout [branch_name]

Switched to branch '[branch_name]'
```

If you want to checkout and create a branch in one shot, you can use: 

```
$ git checkout -b [branch_name]

Switched to a new branch '[branch_name]'
```

## Branch Management

Branch management is an important task, as typically the number of branches will increase quickly on an project. The most typical information you will need to know is which branch have been merged or not merged with the current branch that you are in. The following commands can help you get that information, we will discuss merging next.

```
$ git branch -v
  master 47d6aa5 Commit my file
* [branch_name]  47d6aa5 Commit my file


$ git branch --merged
$ git branch --no-merged
```

## Merging

Merging essentially incorporate the development history from another branch into your current branch. To merge a branch into the current branch, you can simply run:

```
$ git merge [branch_name]

```

Git tries to auto-merge changes. Unfortunately, conflicts arise, so you will have to manually edit the files shown by git. After fixing the file, you add them to the staging area.

```
$ git add [filename]
$ git commit -m "Merge commit."

```

You can also preview changes using the git diff command.

```
$ git diff [source_branch] [target_branch]
$ git diff [filename]
```

## Tagging

To keep track of your software releases, you can use a the tagging feature.

```
$ git tag
```

Tags exist in two forms, lightweight and annotated. Lightweight tags can not be changed, but annotated tags are full objects that can have messages, be updated, etc… 

Lightweight tag:

```
$ git tag first-version [COMMIT_ID]
$ git tag 1.0.0 [COMMIT_ID]
```

You can get the commit id by using the log.

Annotated tag:

```
$ git tag -a 1.0.0 -m "Here is my first version"
```

## Using the Log
The log is an extremely powerful tool and will tell you about the development history of the current branch. You can use to figure out what changes have taken place and who committed these changes. 
The following is a list of variations on the git log command to achieve different objectives.

```
$ git log 
$ git log --stat
$ git log --author=sayar
$ git log --stat [subdirectory]
$ git log --grep='.*foo.*'
$ git log --since="1 week ago" --until="2 weeks ago"
$ git shortlog -sn
```

[REFERENCE](http://blog.mixu.net/2012/04/06/git-tips-and-tricks/)

## Replacing local changes

To replace changes in the working tree to whatever is in HEAD a.k.a. the latest change.

```
$ git checkout -- [filename]
``` 

HOWEVER, changes in the staging area and new files are kept. To drop all changes you have to reset your repository.

```
$ git reset
$ git reset --soft HEAD^
$ git reset --hard
```

Undo a commit and redo

```
$ git commit ...
$ git reset --soft HEAD^
$ edit
$ git commit -a -c ORIG_HEAD
```

Undo a commit, making it a topic branch

```
$ git branch topic/wip
$ git reset --hard HEAD~3
$ git checkout topic/wip
```

This will still not delete new files you added, so you can recommit them if necessary.

## Branching Workflows

Long-Running Branches - As branches are simply pointers to commits, you can keep running many branches without a great difficulty in merging back. 

Topic Branches - Branches can be short-lived. You can create and use a branch for implementing a single feature or topic. As it is fairly straightforward to merge back, I highly recommend you do so as it allows you segment your work into manageable chunks.

![image](http://nvie.com/img/2009/12/Screen-shot-2009-12-24-at-11.32.03.png) [REFERENCE](http://nvie.com/posts/a-successful-git-branching-model/)

## Getting an existing repository

All the work we have done above was entirely local to our machine. The first step in communicating with the outside world is to get an external repository. We can do this with the clone tool and we can retrieve repositories on a specific path or on a user@host.

```
$ git clone /path/to/repo
$ git clone username@host:/path/to/repo
```

## Cloning from GitHub

Most of the open source repositories are now hosted on GitHub. GitHub at its most basic level provides you with a platform to host your git repositories and to be able to collaborate on the code within without needing a direct connection to somebody else's machine. 

GitHub Example using HTTPS: 

```
$ git clone https://github.com/username/repo.git
```

If you have your SSH keys setup with your GitHub account, you can use the SSH transport. Benefits are that you will not have to constantly sign in with your GitHub account. See Setting up SSH Keys with GitHub.

GitHub Example: 

```
$ git clone git@github.com:username/repo.git
```

## Pushing changes to remote repository

If we already have created a repository on our local machine and we can add a remote repository by using the git-remote tool.

```
$ git remote add origin /path/to/repo
$ git remote add origin username@host:/path/to/repo
```

The remote repository can be empty or contain the same history (which it will if you cloned it in the first place). To push your local history to the remote repository, you can use the git-push tool. You can use this tool to push to different branches from your local branch. If you do not specify a remote branch name, git will assume the remote branch has the same name as the local branch. 

```
$ git push [remotename] [localbranch]:[remotebranch]
```

The following is a simple example of pushing your local master branch to the master branch on the remote repository.

```
$ git push origin master
```

## Fetching

To synchronize repositories with a remote repository you can use fetch to get the latest histories. 

```
$ git fetch origin 
```

## Merging Remote Branches

To merge remote repositories, you can specify the repository name and branch name with the slash separator. 

```
$ git merge origin/master
```

If you want to create a branch from the remote repository, check out into it and inform git to track the branch, you can use the following. Tracking a repository simply tells git to set the upstream direction so that you don't have to specify the full details of your push/pull each time (e.g. the remotename is set for you).

```
$ git checkout -t origin/[branch]
```

## Deleting Remote Branches

To delete a remote branch, you simply push nothing into a remote branch.

```
$ git push [remotename] :[remotebranch]
```

## Using Pull

If you already have an upstream setting, you can use git pull to do a fetch and merge.

```
$ git pull [remote] [branch]
$ git pull origin master
```

## GitHub Pull Request
Pull requests let you notify a repository owner that you've offered a set of changes for a merge. If a pull request is sent, the owner can review, discuss changes, add commits and then merge your set of changes into a branch.

#### Fork & Pull
Allows you to clone a repository and then notify the owner of changes you've made in your own fork.

#### Shared Repository Model
If you are sharing a repository, you can still use pull requests to discuss and notify each other about changes taking place in your branch before you merge.

[GitHub Using Pull Requests](https://help.github.com/articles/using-pull-requests)

To use pull requests, you must go on the GitHub project page (of your clone or the page itself) and press the pull request button. For open source projects, unless you were listed as a collaborator, you will not be able to use the shared repository model, you must fork the project, push your code and then send your pull request back to the original repository.

## Git Config

```
$ git config --global -e

$ git config --global user.name "Rami Sayar"

$ git config color.ui true
$ git config format.pretty oneline

$ git config --global alias.co checkout
$ git config --global alias.br branch
$ git config --global alias.lg log
$ git config --global alias.st status
```

## Git Ignore
.gitignore is a file in your repository which informs git to ignore certain files and directories.

Sample for Java

```
*.class

# Package Files #
*.jar
*.war
*.ear
```

[GitHub GitIgnore Repository](https://github.com/github/gitignore)

## Setting up SSH Keys with GitHub

The authoritative documentation is on [GitHub](https://help.github.com/articles/generating-ssh-keys). You will mostly have to generate an ssh key if you do not have one and upload the public key to GitHub.

## Advanced Topics
* [Git Branch Rebasing](http://www.git-scm.com/book/en/Git-Branching-Rebasing)
* [Git Tools - Revision Selection](http://www.git-scm.com/book/en/Git-Tools-Revision-Selection)
* [Git Tools - Rewriting History](http://www.git-scm.com/book/en/Git-Tools-Rewriting-History)
* [Git Tools - Submodules](http://www.git-scm.com/book/en/Git-Tools-Submodules)
* [Git Tools - Subtree Merging](http://www.git-scm.com/book/en/Git-Tools-Subtree-Merging)

## References

* [git - the simple guide by Roger Dudler](http://rogerdudler.github.com/git-guide/)
* [Pro Git by Scott Chacon](http://www.git-scm.com/book)
* [github:help](https://help.github.com/)
