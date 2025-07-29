First, configure a .env file with:
'''
# Inflection Pi API Credentials
PI_API_KEY="API_KEY_HERE"

# Self-hosted Qwen vLLM server Credentials
VLLM_URL="http://0.0.0.0:8000/v1/chat/completions"
'''

Install requirements:
'''
uv pip install -r requirements.txt
'''

Then run:
'''
vllm serve Qwen/Qwen3-8B --reasoning-parser qwen3
'''

Chat with Qwen-Pi:
'''
uv run python main.py
'''
