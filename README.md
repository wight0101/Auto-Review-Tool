# Auto Review Tool 📝⚙️

Auto Review Tool is a project that analyzes all the code in the repository behind the github trap.

### Steps to Run Locally 🖥️

1. **Clone the repository**:
   ```bash
   git clone https://github.com/wight0101/Auto-Review-Tool.git
   
2.Create a virtual environment (recommended for Windows users):
   ```bash
   python -m venv venv
```

3. ## Installation 📥, required libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. **Get ALL API keys(Chathpt API and Github API)**:
   ```bash
   https://platform.openai.com/signup

5. Github API key
   ```bash
    https://github.com/settings/tokens
   ```
6. Then put Chathpt API and Github API in the .env

7. You need to run redis by Docker by this comand:
   ```bash
   docker-compose up -d
   ```
8. And the comand to check if redis is going
   ```bash
   docker ps
   ```

9. Finally you run the program by
   ```bash
   uvicorn main:app --reload
   ```
But you need to run it in the directory app or you can provide path in this comand 

Part 2:
Answer 
To scale the automatic code review tool to handle 100+ requests per minute and large repositories, you can do the following:

Servers: I would use cloud services that scale automatically, such as the same AWS or Google Cloud. If the number of requests increases, new servers are added.

Then I would store the data in databases and do caching, which is already implemented in my code, I would use the same one: PostgreSQL.

Large repositories could be divided into small groups and processed in parallel. I think this would speed up the work

I would optimize OpenAI and GitHub API calls using a cache of already repeated requests. When the number of requests exceeds, add a queue of requests with retries.

This would make the system more stable, fast and ready for high loads.
