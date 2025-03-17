### Hexlet tests and linter status:
[![Python CI](https://github.com/Mirrasol/python-project-83/actions/workflows/my_pyci.yml/badge.svg)](https://github.com/Mirrasol/python-project-83/actions/workflows/my_pyci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/03255ed191683d44ec3b/maintainability)](https://codeclimate.com/github/Mirrasol/python-project-83/maintainability)

Page Analyzer – a web-service that helps to analyze web-pages and determine their SEO usability. It gathers basic relevant data about a web-page: the response code, headers and short description - and organizes it in the table form.


## 1) Installation

This project is built using Flask as the main framework. Please refer to the pyproject.toml file for the full list of required dependencies.

`git clone git@github.com:Mirrasol/python-project-83.git` - download the package from GitHub

`make install` - install using pip from your console


Don't for get to create the .env file that contains your secret key and information about database!

`SECRET_KEY = enter_your_key`

`DATABASE_URL = {provider}://{user}:{password}@{host}:{port}/{db}`

After that set up your database using the commands from database.sql

Check Makefile for the rest of the available commands.


## 2) Demo Web-page

Check an example web-page screenshots:

![1](https://github.com/user-attachments/assets/6418e73d-34af-4149-9b99-29f432db5ea4)

![2](https://github.com/user-attachments/assets/9be88698-4d67-41e0-8f91-da16acdd8834)

![3](https://github.com/user-attachments/assets/b283cf63-2620-4e57-8ad8-7f80ea313d1e)


