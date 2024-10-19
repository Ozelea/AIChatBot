from typing import List
import requests
from langchain_community.document_loaders import WebBaseLoader
from services.groq_llm import llm
from services.prompts import prompt_template
import re
from dotenv import load_dotenv
load_dotenv()


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
                try:
                    loader = WebBaseLoader(url)
                    documents = loader.load()
                    page_data = "".join(
                        [docs.page_content for docs in documents])
                    combined_page_data += page_data + "\n"
                except Exception as e:
                    print(f"Error loading URL {url}: {e}")
                    continue  # Skip this URL and proceed with the next

            # If no content was loaded, inform the LLM to use its general knowledge
            if not combined_page_data.strip():
                combined_page_data = "The content provided from URLs does not contain relevant information about crypto."

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
            print("An unexpected error occurred: ", e)  # Log the error
            return str(e)  # Return the error message


if __name__ == '__main__':
    pass
