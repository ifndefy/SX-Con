<!--
SX-Con - Vendor Management System
A comprehensive application for managing vendor records, products, and revenue sharing.
-->

<div align="center">

  <img src="src/imgs/logo.jpg" width="400" height="auto" />
  
  <h1>SX-Con</h1>
  
  <p>
    Content Management System to streamline and automate our client's Consignment process.
  </p>
  
<!-- Badges -->
<p>
  <a href="https://github.com/ifndefy/SX-Con/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/ifndefy/SX-Con" alt="contributors" />
  </a>
  <a href="">
    <img src="https://img.shields.io/github/last-commit/ifndefy/SX-Con" alt="last update" />
  </a>
  <a href="https://github.com/ifndefy/SX-Con/network/members">
    <img src="https://img.shields.io/github/forks/ifndefy/SX-Con" alt="forks" />
  </a>
  <a href="https://github.com/ifndefy/SX-Con/stargazers">
    <img src="https://img.shields.io/github/stars/ifndefy/SX-Con" alt="stars" />
  </a>
  <a href="https://github.com/ifndefy/SX-Con/issues/">
    <img src="https://img.shields.io/github/issues/ifndefy/SX-Con" alt="open issues" />
  </a>
  <a href="https://github.com/ifndefy/SX-Con/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/ifndefy/SX-Con.svg" alt="license" />
  </a>
</p>
   
<h4>
    <a href="https://github.com/ifndefy/SX-Con/">View Demo</a>
  <span> · </span>
    <a href="https://github.com/ifndefy/SX-Con/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/ifndefy/SX-Con/issues/">Request Feature</a>
  </h4>
</div>

<br />

<!-- Table of Contents -->
# Table of Contents

- [About the Project](#about-the-project)
  * [Screenshots](#screenshots)
  * [Tech Stack](#tech-stack)
  * [Features](#features)
  * [Configs](#configs)
- [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [License](#license)
- [Contact](#contact)

<!-- About the Project -->
## About the Project

SX-Con is a desktop application built with PyQt6 for managing Consignment data.
The application provides a user-friendly interface for creating, viewing, and managing consignment records with robust input validation and Azure Cosmos database integration.

<!-- Screenshots -->
<div align="center">

# Screenshots

## Create New Ticket
![Create New Ticket](src/imgs/create_new.PNG)

## Vendor Tickets
![Vendor Tickets](src/imgs/vendor_tickets.PNG)

## Open Tickets  
![Open Tickets](src/imgs/open_tickets.PNG)

## Settings
![Settings](src/imgs/settings.PNG)

## Admin
![Admin](src/imgs/admin.PNG)

</div>
<!-- TechStack -->

### Tech Stack

<!-- Update the tech stack, it should list what's on the slideshow -->

<details>
  <summary>Client</summary><! -- REMOVE THIS COMMENT || The info in the following block is not correct -->
  <ul>
    <li><a href="https://www.python.org/">Python</a></li>
    <li><a href="https://www.riverbankcomputing.com/software/pyqt/">PyQt6</a></li>
    <li><a href="https://code.visualstudio.com/">VSCode</a></li>
  </ul>
</details>

<details>
  <summary>Backend</summary><! -- REMOVE THIS COMMENT || The info in the following block is not correct -->
  <ul>
    <li><a href="https://docs.python.org/3/library/sqlite3.html">SQLite</a> (Local Development)</li>
    <li><a href="https://azure.microsoft.com/en-us/products/azure-sql/database">Azure SQL</a> (Production)</li>
  </ul>
</details>

<details>
<summary>Database</summary><! -- REMOVE THIS COMMENT || The info in the following block is not correct -->
  <ul>
    <li><a href="https://azure.microsoft.com/en-us/products/azure-sql/database">Azure SQL Database</a></li>
    <li><a href="https://learn.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server">ODBC Driver 18 for SQL Server</a></li>
  </ul>
</details>

<details>
<summary>Authentication</summary>
  <ul>
    <li><a href="https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview">Azure Identity</a></li>
    <li><a href="https://learn.microsoft.com/en-us/azure/active-directory/develop/access-tokens">Azure Access Tokens</a></li>
  </ul>
</details>

<!-- Features -->
### Features

- **Multi-tab Interface**: Separate tabs for Create New, Vendor Tickets, Open Tickets, Settings, and Admin Settings\ 
User Interface is reduced, cleaned, and modernized using tabs to quickly move through options
- **Login Authentication**: login credentials are hashed and stored
<!-- Add feature description for hashing (Colin Henderson) -->
- **Content Management**: Create and manage records with comprehensive information
- User input data is stored in Azure Cosmos NoSQL Database. Additional features such as Cosmos actions, autogeneration, and validation are combined to manage the content.
- **Input Validation**: Robust input restrictions matching database constraints
<!-- Add feature description for validation (Alexander Bubienko) -->
- **Revenue Sharing**: Calculate and manage revenue distribution
<!-- Add feature description for calculation (Kyle Valdez) -->
- **Azure Cosmos NoSQL Integration**: Secure cloud database connectivity
<!-- Add feature description for DB Connection (Maksym Komarov) -->
- **Azure Cosmos NoSQL Actions**: 
<!-- Add feature description for DB interactions (Tim Liu) -->
- **Auto-generated Fields**: Automatic ticket numbers and timestamps
<!-- Add feature description for autopopulations (Tyler Slagboom) -->
- **Printing**: Ticket/Traveler printing
<!-- Add feature description for ptinting (Colin Heinselman) -->

<!-- Config Files -->
### Configs

The connection method will look for the config.ini in services directory
Create `services/config.ini` with the following structure:

"""\
[Cosmos Connection Parameters]\
endpoint = your-cosmos-endpoint\
key = your-cosmos-key\
database_name = your-database\
container_name = your-container\
"""

<!-- Usage -->

### Usage
<!-- explain how to use this step by step -->

<!-- Roadmap -->
### Roadmap
<!-- Insert the flow chart from the slide here -->

<!-- Contact -->

### Contact

Joe Lee, joeslee@csus.edu
<!-- Put your name and email here -->