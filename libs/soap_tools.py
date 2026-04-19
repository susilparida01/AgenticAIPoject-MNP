import httpx
from autogen_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Type
import logging

logger = logging.getLogger(__name__)

class SoapGetInput(BaseModel):
    url: str = Field(description="The URL of the WSDL or SOAP service to fetch.")

class SoapGetTool(BaseTool[SoapGetInput, str]):
    def __init__(self):
        super().__init__(
            args_type=SoapGetInput,
            return_type=str,
            name="soap_get",
            description="Fetches a WSDL or SOAP-related resource using a GET request."
        )

    async def run(self, input_data: SoapGetInput, cancellation_token) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(input_data.url, timeout=30.0)
                return f"Status Code: {response.status_code}\n\nResponse Body:\n{response.text}"
        except Exception as e:
            return f"Error fetching WSDL: {str(e)}"

class SoapPostInput(BaseModel):
    url: str = Field(description="The SOAP service endpoint URL.")
    envelope: str = Field(description="The full XML SOAP envelope to send.")
    headers: Optional[Dict[str, str]] = Field(default=None, description="Optional HTTP headers.")

class SoapPostTool(BaseTool[SoapPostInput, str]):
    def __init__(self):
        super().__init__(
            args_type=SoapPostInput,
            return_type=str,
            name="soap_post",
            description="Sends a SOAP request using a POST method with a provided XML envelope."
        )

    async def run(self, input_data: SoapPostInput, cancellation_token) -> str:
        try:
            headers = input_data.headers or {"Content-Type": "text/xml; charset=utf-8"}
            if "Content-Type" not in headers:
                headers["Content-Type"] = "text/xml; charset=utf-8"
                
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    input_data.url, 
                    content=input_data.envelope, 
                    headers=headers,
                    timeout=30.0
                )
                return f"Status Code: {response.status_code}\n\nResponse Body:\n{response.text}"
        except Exception as e:
            return f"Error performing SOAP POST: {str(e)}"
