### Hexlet tests and linter status:
[![Actions Status](https://github.com/Mirrasol/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Mirrasol/python-project-83/actions)
[![Python CI](https://github.com/Mirrasol/python-project-83/actions/workflows/my_pyci.yml/badge.svg)](https://github.com/Mirrasol/python-project-83/actions/workflows/my_pyci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/03255ed191683d44ec3b/maintainability)](https://codeclimate.com/github/Mirrasol/python-project-83/maintainability)

Page Analyzer – a web-service that helps to analyze web-pages and determine their SEO usability.


## 1) Installation

This project is built using Flask as the main framework. Please refer to the pyproject.toml file for the full list of required dependencies.

`git clone git@github.com:Mirrasol/python-project-83.git` - download the package from GitHub

`make install` - install using pip from your console


Don't for get to create the .env file that contains your secret key and information about database!

`SECRET_KEY = enter_your_key`

`DATABASE_URL = {provider}://{user}:{password}@{host}:{port}/{db}`

After that create your database using the commands from database.sql

Check Makefile for the rest of the available commands.


## 2) Demo Web-page

Check an example web-page (hosted on Render.com):

https://python-project-83-20ew.onrender.com
