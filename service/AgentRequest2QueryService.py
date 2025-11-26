import boto3
import sys
from pathlib import Path

# Ensure parent path so beans package can be imported when running directly
sys.path.append(str(Path(__file__).parent.parent))

from beans.RequestBean import RequestBean

# Add parent directory to path to import beans module
sys.path.append(str(Path(__file__).parent.parent))

from beans.QueryBean import QueryBean


class AgentRequest2QueryService:
    def __init__(self):
        self.bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
        self.agent_id = "VYJQNG5OJV"
        self.agent_alias_id = "2LALQEPT77"
    
    def call_agent(self, query: QueryBean) -> str:
        # result = f"hello {query.uiFieldName} - {query.policyType}"
        bedrock_result = self.connect_bedrock(query)
        return bedrock_result
    
    def connect_bedrock(self, query: RequestBean) -> str:
        try:
            response = self.bedrock_agent_runtime.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.agent_alias_id,
                sessionId='test-session',
                inputText=f"{query.json_path}"
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

    def extract_sql_query(self, query: str) -> str:
        """
        Calls connect_bedrock and extracts only the SQL query from the agent response.
        - Prefers content inside fenced ```sql ... ``` blocks.
        - Falls back to the first line starting with common SQL keywords.
        - Returns empty string if no query could be found.
        """
        full_text = query

        import re
        # Try fenced code block with language sql
        m = re.search(r"```sql\s*(.*?)\s*```", full_text, flags=re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip()

        # Try any fenced code block
        m2 = re.search(r"```\s*(.*?)\s*```", full_text, flags=re.DOTALL)
        if m2:
            block = m2.group(1).strip()
            # If block looks like SQL, return it
            if re.search(r"\bSELECT\b|\bUPDATE\b|\bDELETE\b|\bINSERT\b", block, flags=re.IGNORECASE):
                return block

        # Fallback: find first line that looks like SQL
        lines = full_text.splitlines()
        sql_lines = []
        capture = False
        for line in lines:
            if re.search(r"\bSELECT\b|\bUPDATE\b|\bDELETE\b|\bINSERT\b", line, flags=re.IGNORECASE):
                capture = True
            if capture:
                sql_lines.append(line)
                # Stop when a blank line after capturing
                if not line.strip():
                    break
        return "\n".join(l.strip() for l in sql_lines).strip()
