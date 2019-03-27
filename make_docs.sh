#!/bin/bash

set -e
pip install -r requirements.txt
jupyter nbconvert gallery.ipynb --execute --output-dir=docs --output=index --template=docs/nb.tpl
jupyter nbconvert walkthrough.ipynb --execute --output-dir=docs --template=docs/nb.tpl
pdoc plotly_express --html --html-dir=docs --overwrite --template-dir=docs/templates
