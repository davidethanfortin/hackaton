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

    # Build a RequestBean using the result as json_path and call second agent
    requestBean2 = RequestBean(
        table_name="sample_table",
        json_column="EndpointSignIn.OfflineTOTP",
        json_path=result,
        natural_language_query="Find all records where age is greater than 30",
        policy_types=["type1", "type2"],
    )

    bedrock_result2 = agentrequest2_service.run_request(requestBean2)

    # Return combined result
    return {"agentResult": result, "requestAgentResult": bedrock_result2}


@app.get("/")
async def root():
    return {"message": "Query Generator API", "docs": "/docs"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
