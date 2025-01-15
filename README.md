# Auto Review Tool 📝⚙️

Auto Review Tool is an open-source project designed to help automate the review process in software development. It integrates seamlessly with code repositories to provide insights and recommendations for improving code quality.

## Features 🚀

- **Automated Code Review**: Automatically reviews code for potential issues, inconsistencies, and style violations.
- **Customizable Configuration**: Tailor the review criteria to meet specific coding standards or team preferences.
- **Detailed Feedback**: Provides comprehensive feedback on code quality, readability, and best practices.

## Installation 📥

### Prerequisites

- Python 3.x
- pip
  
### Steps to Run Locally 🖥️

1. **Clone the repository**:
   ```bash
   git clone https://github.com/wight0101/Auto-Review-Tool.git
   
Create a virtual environment (recommended for Windows users):
   ```bash
   python -m venv venv
```

Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```
2. **Get ALL API keys(Chathpt API and Github API)**:
   ```bash
   https://platform.openai.com/signup

4 Github API key
   ```bash
    https://github.com/settings/tokens
   ```
3 Then put Chathpt API and Github API in the .env

4 You need to run redis by Docker by this comand:
   ```bash
   docker-compose up -d
   ```
 And the comand to check if redis is going
   ```bash
   docker ps
   ```

5 Finally you run the program by
   ```bash
   uvicorn main:app --reload
   ```
But you need to run it in the directory app or you can provide path in this comand 

