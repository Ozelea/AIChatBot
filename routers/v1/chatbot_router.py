"""
from fastapi import APIRouter, HTTPException, status
from services.chatbot_services import Application
from schema.chatbot_schema import ChatbotRequest

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"],
)


@router.post("/generate_response", status_code=status.HTTP_200_OK)
async def generate_response(request: ChatbotRequest):
    try:
        # Validate URLs and query inputs before processing
        if not request.urls or not request.query:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid input: URLs and query are required."
            )

        # Initialize the Application class with the given list of URLs
        app = Application(request.urls)

        # Generate the response using the query
        response = app.process_and_respond(request.query)

        # If response is empty or invalid, return an appropriate status
        if not response:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="No response generated from the LLM."
            )

        # Return the response with a 200 status code
        return {"response": response}

    except HTTPException as e:
        # Let HTTPExceptions pass through to be handled by FastAPI
        raise e

    except Exception as e:
        # Catch any unexpected errors and return a 500 status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
"""



from fastapi import APIRouter, HTTPException, status
from schema.chatbot_schema import ChatbotRequest,ChatbotResponse
from services.prompts import prompt
from services.api_chatbot import llm_with_tools, tools
from services.chatbot_services import Application  # Your web-scraping logic here
from langchain.agents import AgentExecutor, create_tool_calling_agent
agents = create_tool_calling_agent(llm_with_tools, tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agents, tools=tools, verbose=True)

# Create a single router for both chatbots
router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot"],
)


@router.post("/", response_model=ChatbotResponse)
async def chat(request: ChatbotRequest):
    try:
        # Determine the type of request based on the query
        if hasattr(request, 'message'):
            if request.query == "Web-Scraping":
                # Handle web-scraping request
                if not request.urls:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid input: URLs are required for web scraping."
                    )

                # Initialize the Application class with the given list of URLs
                app = Application(request.urls)

                # Generate the response using the query
                response = app.process_and_respond(request.message)

                # If response is empty or invalid, return an appropriate status
                if not response:
                    raise HTTPException(
                        status_code=status.HTTP_204_NO_CONTENT,
                        detail="No response generated from the LLM."
                    )

                return ChatbotResponse(response=response)

            elif request.query == "Check Balance":
                # Handle Ethereum balance check request
                ai_message = agent_executor.invoke({"input": request.message})

                # Check if the response is in the correct format
                if isinstance(ai_message, dict) and 'output' in ai_message:
                    response_str = ai_message['output']
                elif isinstance(ai_message, str):
                    response_str = ai_message
                else:
                    raise ValueError(
                        "Unexpected response format from agent_executor")

                return ChatbotResponse(response=response_str)

            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid query: Expected 'Web-Scraping' or 'Check Balance'."
                )

        # Raise an error if request structure is not as expected
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request: 'query' field is required."
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )