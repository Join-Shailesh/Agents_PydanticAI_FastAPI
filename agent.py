import os
from dotenv import load_dotenv
from colorama import Fore
from dataclasses import dataclass
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider 

# Initialize model
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@dataclass
class Movie:
    title: str
    year: str
    rating: float
    gener: str  # NOTE: Should likely be "genre"
    cast: list[str]

if not GROQ_API_KEY:
    raise ValueError(Fore.RED + "Groq key not Found")

def get_model(model_name: str):
    try:
        provider = GroqProvider(api_key=GROQ_API_KEY)  # Create provider first
        model = GroqModel(
            model_name=model_name,
            provider=provider  # Pass provider instead of api_key
        )
    except Exception as e:
        print(Fore.RED + "Error initializing model", e)
        model = None
    return model

def main_loop():
    system_prompt = "You are a movie critic and expert"
    agent = Agent(
        model=get_model("llama-3.3-70b-versatile"),
        result_type=Movie,
        system_prompt=system_prompt
    )
    
    while True:
        user_input = input("==>>> Enter a movie query (q, quit, exit to exit): ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        result = agent.run_sync(user_input)
        print(Fore.BLUE, result.data)

if __name__ == '__main__':
    main_loop()


async def getMovieDetails(q:str, model:str) -> Movie:
    model_name = model if model is not None else "llama-3.3-70b-versatile"
    system_prompt = "You are a movie critic and expert. you are expert of web series"
    agent = Agent(
        model=get_model(model_name),
        result_type=Movie,
        system_prompt=system_prompt 
    )
    try:
        result = await agent.run(q)
        return result.data
    except Exception as e:
        error_msg = f"Error: {type(e).__name__} - {str(e)}"
        print(Fore.RED + error_msg)
        return error_msg

    
