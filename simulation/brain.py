import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load API Keys
load_dotenv()

class NPCBrain:
    def __init__(self, player_name: str):
        self.name = player_name
        
        # 1. Setup the LLM (DeepSeek via OpenRouter)
        self.llm = ChatOpenAI(
            model="tngtech/deepseek-r1t2-chimera:free",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            temperature=0.4 # Slightly creative, but not random
        )
        
        # 2. Define the "Personality" Prompt
        # We force the AI to reply in JSON format ONLY.
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are an AI character named {name} in a 2D survival grid.
            Your goal is to SURVIVE.
            
            RULES:
            - Eating APPLE restores health.
            - WOLF will hurt you.
            - Walls block movement.
            
            You must output your decision in strictly valid JSON format like this:
            {{
                "thought": "I see an apple to the East and I am hungry.",
                "action": "MOVE",
                "dx": 1, 
                "dy": 0
            }}
            
            Possible Moves:
            - North: dx=0, dy=-1
            - South: dx=0, dy=1
            - East: dx=1, dy=0
            - West: dx=-1, dy=0
            """),
            ("user", "My Status: Health={health}. My Vision: {vision}. What do I do?")
        ])

    def decide(self, vision: str, health: int):
        """
        Sends the game state to the AI and gets a move back.
        """
        print(f"🤔 {self.name} is thinking...")
        
        # 1. Format the input
        chain = self.prompt | self.llm
        
        try:
            # 2. Call the AI
            response = chain.invoke({
                "name": self.name,
                "health": health,
                "vision": vision
            })
            
            # 3. Clean the response 
            content = response.content
            
            # Helper to find the JSON bracket {} inside the text
            start = content.find('{')
            end = content.rfind('}') + 1
            if start == -1 or end == 0:
                print(f"❌ Error: AI didn't return JSON. Raw: {content}")
                return None
                
            json_str = content[start:end]
            decision = json.loads(json_str)
            
            return decision

        except Exception as e:
            print(f"💥 Brain Freeze: {str(e)}")
            return None