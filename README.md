<!--
SX-Con - Vendor Management System
A comprehensive application for managing vendor records, products, and revenue sharing.
-->

<div align="center">

  <img src="src/imgs/logo.jpg" width="200" height="auto" />
  
  <h1>SX-Con</h1>
  
  <p>
    Vendor Management System for tracking products and revenue sharing with Azure SQL integration
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
  * [Environment Variables](#environment-variables)
- [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Run Locally](#run-locally)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

<!-- About the Project -->
## About the Project

SX-Con is a desktop application built with PyQt6 for managing vendor information, product inventory, and revenue sharing calculations. The application provides a user-friendly interface for creating, viewing, and managing vendor records with robust input validation and Azure SQL database integration.

<!-- Screenshots -->
### Screenshots

<div align="center"> 
  <h4>Create New Ticket</h4>
  <img src="src/imgs/create-new.png" width="600" />
  
  <h4>Open Tickets</h4>
  <img src="src/imgs/open-tickets.png" width="600" />
  
  <h4>Settings</h4>
  <img src="src/imgs/settings.png" width="400" />

  <h4>Vendor Tickets</h4>
  <img src="src/imgs/vendor-tickets.png" width="400" />
</div>

<!-- TechStack -->
### Tech Stack

<details>
  <summary>Client</summary>
  <ul>
    <li><a href="https://www.python.org/">Python</a></li>
    <li><a href="https://www.riverbankcomputing.com/software/pyqt/">PyQt6</a></li>
    <li><a href="https://code.visualstudio.com/">VSCode</a></li>
  </ul>
</details>

<details>
  <summary>Backend</summary>
  <ul>
    <li><a href="https://docs.python.org/3/library/sqlite3.html">SQLite</a> (Local Development)</li>
    <li><a href="https://azure.microsoft.com/en-us/products/azure-sql/database">Azure SQL</a> (Production)</li>
  </ul>
</details>

<details>
<summary>Database</summary>
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

- **Vendor Management**: Create and manage vendor records with comprehensive information
- **Product Tracking**: Track product inventory with quantity and pricing
- **Input Validation**: Robust input restrictions matching database constraints
- **Revenue Sharing**: Calculate and manage revenue distribution
- **Azure SQL Integration**: Secure cloud database connectivity
- **Auto-generated Fields**: Automatic ticket numbers and timestamps
- **Multi-tab Interface**: Separate tabs for Create, View, Get, Delete, and Admin operations

<!-- Env Variables -->
### Environment Variables

Create `services/config.ini` with the following structure:

```ini
[SQL Connection Parameters]
odbc_driver = {ODBC Driver 18 for SQL Server}
server_addr = your-server.database.windows.net
server_port = 1433
db_name = your-database-name
sql_access_token = 1256

[Cosmos Connection Parameters]
endpoint = your-cosmos-endpoint
key = your-cosmos-key
database_name = your-database
container_name = your-container