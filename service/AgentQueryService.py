import boto3
import sys
from pathlib import Path

# Add parent directory to path to import beans module
sys.path.append(str(Path(__file__).parent.parent))

from beans.QueryBean import QueryBean


class AgentQueryService:
    def __init__(self):
        self.bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
        self.agent_id = "RY4TK2YGH9"
        self.agent_alias_id = "TSTALIASID"
    
    def call_agent(self, query: QueryBean) -> str:
        # result = f"hello {query.uiFieldName} - {query.policyType}"
        bedrock_result = self.connect_bedrock(query)
        return bedrock_result
    
    def connect_bedrock(self, query: QueryBean) -> str:
        try:
            response = self.bedrock_agent_runtime.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.agent_alias_id,
                sessionId='test-session',
                inputText=f"give me json path for screen field {query.uiFieldName}"
            )
            
            result = ""
            for event in response['completion']:
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        result += chunk['bytes'].decode('utf-8')
            
            return result
        except Exception as e:
            return f"Error connecting to Bedrock agent: {str(e)}"
