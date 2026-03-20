# How to Run Locally and Deploy to Vercel

This project is a multi-agent AI bug detection application using FastAPI, python orchestrators, and a modern Vanilla HTML frontend. It's fully optimized for local development and serverless deployment to Vercel.

## 🚀 1. Running Locally

### Prerequisites
* Python 3.9+
* Create a virtual environment (`python -m venv venv`) and activate it.
* Install dependencies:
  ```bash
  cd "A-12"
  pip install -r requirements.txt
  ```

### Configuration
1. Be sure your `GROQ_API_KEY` is present in `code/config.py`.
2. Be sure the `MCP_SERVER_URL` is correct and the server is running on `http://localhost:8003/sse` (this part is needed for the validator agent, per your pre-existing code).

### Start the Server
Run the FastAPI developer server with `uvicorn`:

```bash
uvicorn api.index:app --reload
```

* Once it's running, open your web browser and go to `http://localhost:8000/`.
* You will see the stunning glassmorphism dashboard where you can paste your code and context!


## 🌐 2. Deploying on Vercel

This application relies on the `@vercel/python` builder. It will seamlessly deploy your FastAPI application serverless while serving your `/public/index.html` file staticly.

### Approach 1: Deploy using Vercel CLI (Recommended)

1. **Install the Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**: Navigate to the `A-12` root folder and run:
   ```bash
   vercel
   ```
   Follow the prompts. Vercel will auto-detect the configuration from the `vercel.json`.

### Approach 2: Deploy using GitHub Integration

1. Push your `A-12` folder to a GitHub repository.
2. Go to the [Vercel Dashboard](https://vercel.com/dashboard).
3. Click "Add New..." -> "Project".
4. Import your newly created GitHub repository.
5. In the "Environment Variables" section, you might want to configure environment variables for the MCP connection or Groq API (if you decide to update `config.py` to use `os.environ` later, this is best practice to hide the key from source control!).
6. Click **Deploy**.

## Troubleshooting
* **`ModuleNotFoundError` on Vercel**: The `api/index.py` correctly appends the `code/` directory to `sys.path`. This ensures `@vercel/python` can find `orchestrator` during cold starts.
* **`MCP Server Unavailable`**: Reminder that MCP Servers locally running at `localhost:8000` will *not* be reachable from Vercel unless it's a publicly accessible URL, or if you bundle the MCP server directly in Vercel. You may need to expose your MCP server via ngrok so Vercel can fetch the docs during agent operation.
