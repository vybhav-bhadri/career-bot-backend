# Career Counsellor Agent

This project implements an intelligent Career Counsellor system using a multi-agent architecture. It is designed to provide interactive career guidance by leveraging advanced AI agents and real-time web research capabilities.

## Implementation Details

The system is built using a modern AI stack:

1.  **Google ADK (Agent Development Kit)**: utilized for building and managing the AI agents.
2.  **MCP (Model Context Protocol) & A2A (Agent-to-Agent)**:
    *   **MCP**: Leveraged for standardized tool interfaces, allowing the Researcher agent to perform actions like web searches.
    *   **A2A**: Enables seamless communication between the different agents in the system.
3.  **Counsellor Agent**: This is the primary agent exposed to the user interface. It is served via a **FastAPI** backend, handling user interactions and orchestrating the session.
4.  **Researcher Agent**: A specialized agent responsible for fetching up-to-date information. It uses MCP tools to perform web searches and gather the latest career-related data.
5.  **Agent Collaboration**: The Counsellor agent delegates specific information-gathering tasks to the Researcher agent using the A2A protocol, ensuring accurate and grounded advice.

## Future Improvements

To further enhance the capabilities and user experience, the following improvements are planned:

1.  **Enhanced Tooling for Researcher**:
    *   Give the Researcher agent access to specialized career databases (e.g., job market trends, salary data) using **MCP resource tools**. This will provide more granular and authoritative data sources beyond general web search.
2.  **Real-Time Streaming**:
    *   Implement streaming responses to the UI. This will keep the interface interactive and responsive, allowing users to see the agent's "thought process" and receive partial answers as they are generated.

## Running Locally

To run the project locally, you will need to start the backend agents and the frontend interface.

1.  **Backend**: Open two terminal tabs in the `backend` directory.
    *   **Tab 1**: Start the Researcher Agent (exposes via A2A).
        ```bash
        python run_researcher.py
        ```
    *   **Tab 2**: Start the Counsellor Agent (exposes via API).
        ```bash
        python main.py
        ```

2.  **Frontend**: Open a new terminal tab in the `frontend` directory.
    *   Start the UI development server.
        ```bash
        npm run dev
        ```

## Deployment & Live Project

This project is designed to be cloud-agnostic and can be deployed to various platforms.

### Deploying to Production

You can deploy this application to improved infrastructure for production use-cases:

1.  **Railway**:
    *   Connect your GitHub repository to Railway.
    *   Railway can automatically detect the `Dockerfile` or `Procfile` (if present) or you can configure the build command.
    *   Set up the necessary environment variables (API keys, etc.) in the Railway dashboard.
2.  **AWS (Amazon Web Services)**:
    *   For more control, you can deploy to services like AWS App Runner or ECS (Elastic Container Service).
    *   Containerize the application using Docker.
    *   Push the image to ECR (Elastic Container Registry).
    *   Configure the service to run your container, ensuring environment variables are securely managed via AWS Systems Manager Parameter Store or Secrets Manager.
