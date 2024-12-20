#!/bin/bash
#! Coding By Rasool Vahdati

# Scenario 1: Initializing and Configuring a New Repository
mkdir project6
cd project6
git config --global user.name "<your_username>"
git config --global user.email "<your_email>"
git init
echo "# MLOps Project 6" > README.md
git add README.md
git commit -m "init commit for scenario 1"

# Scenario 2: Creating and Switching to a New Branch
git checkout feature-branch
git branch feature-branch
echo "this is test content for feature.txt" >> touch feature.txt
git add feature.txt
git commit -m "added feature.txt to project"

# Scenario 3: Using git blame to Identify Changes
git blame app.py
git show c4dbe5dc # commit hash

# Scenario 4: Cleaning Up Untracked Files
# Step 1
git clean -n -d
# Step 2
git clean -f -d

# Scenario 5: Setting Up SSH for GitHub
ssh-keygen -t rsa -b 4096 -C "<your_email>"
ssh-add ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub
ssh -T git@github.com

# Scenario 6: Pushing a Branch to a Remote Repository
git branch
git checkout feature-branch
git push origin feature-branch

# Scenario 7: Merging a Branch into Main
git checkout main
git merge feature-branch
git push origin main