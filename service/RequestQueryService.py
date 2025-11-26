import boto3
from typing import Optional
import sys
from pathlib import Path
import json

# Ensure parent path so beans package can be imported when running directly
sys.path.append(str(Path(__file__).parent.parent))

from beans.RequestBean import RequestBean


class RequestQueryService:
    def __init__(self, region_name: str = "us-east-1"):
        self.bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name=region_name)
        self.agent_id = "VYJQNG5OJV"
        self.agent_alias_id = "2LALQEPT77"

    def run_request(self, request: Optional[RequestBean] = None) -> str:
        """
        Invoke the Bedrock Agent with provided RequestBean. If no bean is provided,
        uses the default values specified in the task.
        """
        if request is None:
            request = RequestBean(
                table_name="policy.tbl_server_policy",
                json_column="server_policy",
                json_path="EndpointSignIn.OfflineTOTP",
                natural_language_query=(
                    "get me a list of all sets which are using provided policy "
                    "and setting provided json path parameter to 'false'"
                ),
                policy_types=["48", "52"],
            )

        try:
            # Build prompt with all parameters as JSON
            prompt_data = {
                "table_name": request.table_name,
                "json_column": request.json_column,
                "json_path": request.json_path,
                "natural_language_query": request.natural_language_query,
                "policy_types": request.policy_types,
            }
            prompt = json.dumps(prompt_data, ensure_ascii=False)


            response = self.bedrock_agent_runtime.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.agent_alias_id,
                sessionId="request-query-session",
                inputText=prompt,
            )

            result = ""
            for event in response.get("completion", []):
                if "chunk" in event:
                    chunk = event["chunk"]
                    if "bytes" in chunk:
                        result += chunk["bytes"].decode("utf-8")

            return result or ""
        except Exception as e:
            return f"Error connecting to Bedrock agent: {str(e)}"
