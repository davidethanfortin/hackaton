from fastapi import FastAPI
import uvicorn
from beans import QueryBean, RequestBean
from service import AgentQueryService, RequestQueryService

app = FastAPI(title="Query Generator API", version="1.0.0")
agent_service = AgentQueryService()
agentrequest2_service = RequestQueryService()


@app.post("/generate")
async def generate_query(request: QueryBean):
    """
    Generate a greeting message.
    
    - **uiFieldName**: UI field name
    - **policyType**: Policy type
    """
    # Call first agent and get a result string
    result = agent_service.call_agent(request)

    # Extract only the JSON path token from the agent result (e.g., LoginDesktopIdentityProvider.IdentityProviderName)
    import re
    match = re.search(r"^[A-Za-z0-9_.]+$", result.strip(), flags=re.MULTILINE)
    resultQuery1 = match.group(0) if match else result.strip()
    
    


    # Build a RequestBean using the result as json_path and call second agent
    requestBean2 = RequestBean(
        table_name="policy.tbl_server_policy",
        json_column="server_policy",
        json_path=resultQuery1,
        natural_language_query=request.naturalLanguageQuery,
        policy_types=["48", "52"],
    )

    bedrock_result2 = agentrequest2_service.run_request(requestBean2)

    # Return combined result
    return {"agentResult": result, "jsonPath": resultQuery1, "requestAgentResult": bedrock_result2}


@app.get("/")
async def root():
    return {"message": "Query Generator API", "docs": "/docs"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
