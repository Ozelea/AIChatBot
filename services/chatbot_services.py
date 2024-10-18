from typing import List
import requests
from langchain_community.document_loaders import WebBaseLoader
from services.groq_llm import llm
from services.prompts import prompt_template
import re
from langchain_core.tools import tool
from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import HTTPException,status
ETHERSCAN_API_KEY=os.getenv('ETHERSCAN_API_KEY')
WALLET_ADDRESS=os.getenv('WALLET_ADDRESS')
API_URL = f"https://api-sepolia.etherscan.io/api?module=account&action=balance&address={WALLET_ADDRESS}&tag=latest&apikey={ETHERSCAN_API_KEY}"


class Application:
    def __init__(self, urls: List[str]):
        self.urls = urls

    def process_and_respond(self, query):
        """
        Loads documents from each URL, combines the content, and generates a response 
        based on the combined data and the user query.
        """
        try:
            # Combine page data from all URLs
            combined_page_data = ""
            for url in self.urls:
                loader = WebBaseLoader(url)
                documents = loader.load()
                page_data = "".join([docs.page_content for docs in documents])
                combined_page_data += page_data + "\n"

            # Save the combined content to a file
            with open('combined_file.txt', 'w', encoding='UTF-8') as file:
                file.write(combined_page_data.strip())

            # Prepare the prompt and generate a response
            prompt = prompt_template.format(
                page_data=combined_page_data.strip(), question=query)
            response = llm.invoke(prompt)
            clean_response = re.sub(r'\n+', ' ', response.content)

            return clean_response

        except Exception as e:
            return str(e)  # Return the error message

    def __str__(self):
        """Override the string representation of the application."""
        return f"Application to scrape URLs: {', '.join(self.urls)}"
if __name__ == '__main__':
    pass