#!/bin/bash

# stop on errors
set -e

# install everything including local version
pip install -r requirements.txt

# reset doc build dir
rm -rf doc_build
mkdir doc_build

# generate HTML reference docs
pdoc plotly_express --html --html-dir=doc_build --overwrite --template-dir=docs/templates

for NB in walkthrough gallery
do
  # make unexecuted IPYNB files from MD files (overwrites)
  jupytext --to notebook $NB.md

  # create executed IPYNB files in the build dir
  jupyter nbconvert --execute --to notebook $NB.ipynb --output doc_build/$NB.ipynb

  # convert executed doc_build/IPYNB files to doc_build/HTML using template
  jupyter nbconvert doc_build/$NB.ipynb --template=docs/nb.tpl
done


cd doc_build
echo www.plotly.express >> CNAME
echo plotly_express >> requirements.txt
mv gallery.html index.html

if [ "$1" == "deploy" ]
then
  # push to gh-pages
  git init
  git add .
  git commit -m doc_build
  git push --force git@github.com:plotly/plotly_express.git master:gh-pages
fi

cd ..

