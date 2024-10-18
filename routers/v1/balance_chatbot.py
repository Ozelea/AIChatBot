from schema.balace_chatbot_schema import ChatRequest, ChatResponse
from services.prompts import prompt
from services.api_chatbot import llm_with_tools, tools
from langchain.agents import AgentExecutor, create_tool_calling_agent
from fastapi import APIRouter, HTTPException, status
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key='chat_history')


# Initialize the agents
agents = create_tool_calling_agent(llm_with_tools, tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agents, tools=tools, verbose=True)

router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
)


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Use agent_executor to get a response, using "input" as the key
        ai_message = agent_executor.invoke(
            {"input": request.message}
        )

        # Check if the response is in the correct format
        if isinstance(ai_message, dict) and 'output' in ai_message:
            response_str = ai_message['output']
        elif isinstance(ai_message, str):
            response_str = ai_message
        else:
            raise ValueError("Unexpected response format from agent_executor")
        memory.chat_memory.add_user_message(request.message)
        memory.chat_memory.add_ai_message(response_str)
        print(memory.load_memory_variables({}))

        # Return the response in the correct format
        return ChatResponse(response=response_str)

    except Exception as e:
        # Raise an HTTP exception with a proper error message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
