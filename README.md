# UZBASE Community Portal

UZBASE is a modern, high-end community portal for the Uzbek language community living in Germany. It matches the brand's logo theme colors with an Electric Blue and Emerald Green styling, complete with dark mode and multilingual options.

## Features Included
- **Multilingual Support**: Uzbek (UZ), German (DE), and Russian (RU).
- **Jobs Board**: Filterable job board with post-a-job functionality.
- **Housing Directory**: Accommodation grid (WG, apartment, short-term stays) with details and filters.
- **Interactive Forum**: Topics list categorized with asynchronous upvoting and comments.
- **Info Wiki**: Accordion guides regarding German Bureaucracy.
- **Services Directory**: Verified list of Uzbek-speaking professionals (Translators, Legal Advisors).

---

## Installation & Setup Guide

To install and run this project on another computer:

### 1. Prerequisites
Ensure you have **Python 3.8+** installed. You can download it from [python.org](https://www.python.org/downloads/).

### 2. Copy Project Files
Copy the entire project directory (`UZBASE`) onto the target computer. The structure should look like this:
```text
uzbase.de/
├── app.py
├── requirements.txt
├── README.md
├── static/
│   └── logo.png
└── templates/
    ├── base.html
    ├── index.html
    ├── jobs.html
    ├── housing.html
    ├── community.html
    ├── info.html
    └── services.html
```

### 3. Install Dependencies
Open your terminal (Command Prompt, PowerShell, or Terminal on macOS/Linux) in the project directory and install the requirements:
```bash
pip install -r requirements.txt
```

### 4. Start the Application
Run the Flask server using the following command:
```bash
python app.py
```

### 5. Access the Web Application
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```
