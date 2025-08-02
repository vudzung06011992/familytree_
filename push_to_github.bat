@echo off
echo Pushing code to GitHub...

echo Initializing git repository...
git init

echo Setting up git config...
git config user.name "vudzung06011992"
git config user.email "vudung.vvd@gmail.com"

echo Adding remote repository...
git remote add origin https://github.com/vudzung06011992/familytree_.git

echo Adding files to staging...
git add .

echo Creating commit...
git commit -m "Improved family tree card display: centered text, line wrapping for long names, and better spacing between name and birth year"

echo Setting main branch...
git branch -M main

echo Pushing to GitHub...
git push -u origin main

echo.
echo Done! Check if push was successful above.
pause
