import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global constants from environment variables
VLLM_API_KEY = os.getenv("VLLM_API_KEY")
VLLM_URL = os.getenv("VLLM_URL")
VLLM_MODEL_NAME = os.getenv("VLLM_MODEL_NAME")
PI_API_KEY = os.getenv("PI_API_KEY")
PI_VERSION = os.getenv("PI_VERSION", "Pi-3.1")  # Default to justpi

def get_factual_answer_from_qwen(user_query):
    """
    Get a factual answer from Qwen model via VLLM API.
    
    Args:
        user_query (str): The user's query string
        
    Returns:
        str or None: The AI's response content, or None if request fails
    """
    # Construct messages payload
    messages = [
        {
            "role": "system",
            "content": "You are Qwen, the analytical reasoning engine powering Pi's responses. Pi excels at friendly conversation but relies on you for deep analysis, complex reasoning, technical knowledge, and factual accuracy. Your role: provide concise yet complete analytical answers that cover the essential facts, key concepts, and logical reasoning. Be precise and well-structured, but avoid unnecessary verbosity. Focus on the core information Pi needs to give an excellent answer. You handle the 'thinking' - Pi handles the 'talking'. Prioritize accuracy, relevance, and analytical depth over length."
        },
        {
            "role": "user", 
            "content": user_query
        }
    ]
    
    # Construct full payload
    payload = {
        "model": VLLM_MODEL_NAME,
        "messages": messages,
        "max_tokens": 32768,
        "temperature": 0.0
    }
    
    # Set up headers with authorization
    headers = {
        "Authorization": f"Bearer {VLLM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Make POST request to VLLM API
        response = requests.post(VLLM_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        # Parse JSON response and extract content
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
        
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request error occurred: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing response: missing key {e}")
        return None
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return None

def restyle_text_with_pi(text_to_restyle, original_query, pi_version):
    """
    Restyle factual text using Pi's conversational tone while retaining all facts.
    
    Args:
        text_to_restyle (str): The factual text to restyle
        original_query (str): The original user query for context
        
    Returns:
        str or None: The restyled text, or None if request fails
    """

    if pi_version == "inflection_3_pi":
        pi_url = "https://api.inflection.ai/external/api/inference/openai/v1/chat/completions"
    elif pi_version == "Pi-3.1":
        pi_url = "https://api.inflection.ai/v1/chat/completions"
    else:
        raise ValueError(f"Invalid Pi version: {pi_version}")


    # Construct messages payload
    messages = [
        {
            "role": "system",
            "content": "You are Pi, an AI assistant known for your friendly, supportive, and conversational tone. A user asked a question, and another AI (Qwen) provided a detailed, factual response. Your task is to rewrite Qwen's response using your signature style and personality while keeping it as a direct answer to the original user question. It is CRITICAL that you retain ALL original facts, data, and key details from Qwen's text. DO NOT add new facts. Remember your backstory and personality at all times."
        },
        {
            "role": "user",
            "content": f"Original user question: {original_query}\n\nQwen's factual response to restyle:\n{text_to_restyle}"
        }
    ]
    
    model = pi_version

    # Construct full payload
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.7
    }
    
    # Set up headers with authorization
    headers = {
        "Authorization": f"Bearer {PI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Make POST request to Pi API
        response = requests.post(pi_url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        # Parse JSON response and extract content
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
        
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request error occurred: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing response: missing key {e}")
        return None
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return None

if __name__ == "__main__":

    if PI_VERSION != "Pi-3.1" and PI_VERSION != "inflection_3_pi":
        raise ValueError(f"Invalid Pi version: {PI_VERSION}, must be 'Pi-3.1' or 'inflection_3_pi'")
    
    print(f"Qwen-Pi CLI Chat. Using {PI_VERSION} as Pi. Type 'exit' to quit.")
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check for exit condition
        if user_input.lower() == 'exit':
            break
        
        # Get factual answer from Qwen
        print("\n🧠 Thinking with Qwen's brain...")
        qwen_response = get_factual_answer_from_qwen(user_input)
        
        if qwen_response is not None:
            # Print Qwen's response for comparison
            print("\nQwen Response:")
            print(qwen_response)
            
            # Restyle with Pi's friendly voice
            print("\n🎨 Adding Pi's friendly voice...")
            pi_response = restyle_text_with_pi(qwen_response, user_input, PI_VERSION)
            
            if pi_response is not None:
                print("\nPi-Style Response:")
                print(pi_response)
            # If Pi call failed, error messages are already printed by the function
        # If Qwen call failed, error messages are already printed by the function
