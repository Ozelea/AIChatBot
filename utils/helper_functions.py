import requests
import os
from fastapi import HTTPException, status
from typing import List, Dict, Any
from dotenv import load_dotenv
load_dotenv()

# Load API key from environment
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')


def multiple_address_balance():
    API_URL = f"https://api-sepolia.etherscan.io/api?module=account&action=balancemulti&address=0x382b4ca2c4a7cd28c1c400c69d81ec2b2637f7dd, 0x8a5847fd0e592b058c026c5fdc322aee834b87f5, 0x63a9dbCe75413036B2B778E670aaBd4493aAF9F3, 0xd82b6aB1f20A21484fA5E28221B95425dddC5E8E&tag=latest&apikey=JBHG98JSJI7CRDSECQ6BPQHZHW3A38FPMD"

    response = requests.get(API_URL)
    if response.status_code == 200:
        result = response.json()
        if result.get("status") == "1":  # API call was successful
            return result
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "Error fetching balances.",
                    "message": result.get("message", "Unknown error"),
                    "data": result.get("result", [])
                }
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": f"Unexpected status code {response.status_code}: {response.content}"
            }
        )
