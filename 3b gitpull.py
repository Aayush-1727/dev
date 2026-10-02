"A" should already be performed b4 "B"
Open VS Code> File > Open Folder >Git_Practical

New Terminal
git branch
git checkout -b feature-login

Open:
hello.py
print("Login Feature Added")
print("Feature Branch Example")
Save the file (Ctrl + S).
git add hello.py
git commit -m "added"
git log --oneline
'''
1.Open GitHub.
2. Click New Repository.
3. Repository name: Git_Practical
4. Create Repository.

git remote add origin "Copy your GitHub repository URL"
git remote -v
git checkout main
git push -u origin main
git checkout feature-login
git push -u origin feature-login

Go to GitHub.
You will see:
Compare & Pull Request
Click it.
then on git only Click:
Merge Pull Request

In VS Code:
git checkout main
git pull origin main
'''