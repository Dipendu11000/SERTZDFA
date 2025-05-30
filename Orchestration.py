from typing import List, Dict

class AgentStatus:
    def __init__(self, name):
        self.name = name
        self.status = "Pending"
        self.message = ""

    def update(self, status, message=""):
        self.status = status
        self.message = message

    def __repr__(self):
        return f"{self.name}: {self.status} {self.message}"

# --- Agent Stubs (hardcoded logic) ---

class GovernanceAgent:
    def run(self, query):
        return "Governance check complete. Guardrails in place."

class AuthorizationAgent:
    def run(self, query):
        return "Authorization successful. Access granted."

class ResearchAgent:
    def run(self, query):
        if "treatment space" in query:
            return "Latest trends: AI-driven diagnostics, personalized medicine, telehealth expansion."
        elif "marketing campaigns" in query:
            return "Latest campaigns: 'HealthFirst 2024', 'Wellness for All', 'CareConnect'."
        else:
            return "Research completed."

class RiskAssessmentAgent:
    def run(self, query):
        return "Risk assessment: Moderate risk identified for this healthcare treatment."

class LegalAgent:
    def run(self, query):
        return "Legal review: No regulatory or compliance issues found."

class RevenueProfitAgent:
    def run(self, query):
        return "Projected revenue: $2.5M, Projected profit: $800K for the first year."

class MarketingAnalyticsAgent:
    def run(self, query):
        return "ROI Analysis: Campaigns yielded 150% ROI, with a 30% increase in engagement."

class DocumentingAgent:
    def run(self, query, results):
        doc = "Documentation Summary:\n"
        for agent, result in results.items():
            doc += f"- {agent}: {result}\n"
        doc += "Final answer ready for download."
        return doc

# --- Orchestration Logic ---

class OrchestrationAgent:
    def __init__(self):
        self.agents = {
            "Governance": GovernanceAgent(),
            "Authorization": AuthorizationAgent(),
            "Research": ResearchAgent(),
            "RiskAssessment": RiskAssessmentAgent(),
            "Legal": LegalAgent(),
            "RevenueProfit": RevenueProfitAgent(),
            "MarketingAnalytics": MarketingAnalyticsAgent(),
            "Documenting": DocumentingAgent(),
        }

    def get_pipeline(self, query_type):
        pipelines = {
            "treatment_trends": ["Governance", "Authorization", "Research", "Documenting"],
            "treatment_risk": ["Governance", "Authorization", "RiskAssessment", "Legal", "Documenting"],
            "revenue_projection": ["Governance", "Authorization", "RevenueProfit", "Documenting"],
            "marketing_campaigns": ["Governance", "Authorization", "Research", "Documenting"],
            "roi_analysis": ["Governance", "Authorization", "MarketingAnalytics", "Documenting"],
        }
        return pipelines[query_type]

    def run_pipeline(self, query_type, query):
        pipeline = self.get_pipeline(query_type)
        statuses: List[AgentStatus] = []
        results = {}
        for agent_name in pipeline:
            status = AgentStatus(agent_name)
            statuses.append(status)
            status.update("Running", f"Calling {agent_name} Agent...")
            print(status)
            # Simulate agent call
            if agent_name == "Documenting":
                result = self.agents[agent_name].run(query, results)
            else:
                result = self.agents[agent_name].run(query)
                results[agent_name] = result
            status.update("Done", f"{result} ✓")
            print(status)
        print("\n--- Final Documentation ---")
        print(results.get("Documenting", ""))
        print("-" * 40)
        return statuses, results

# --- Example Usage ---

if __name__ == "__main__":
    orchestrator = OrchestrationAgent()

    # 1. What are latest trends in the healthcare treatment space?
    print("\n--- Treatment Trends Query ---")
    orchestrator.run_pipeline(
        "treatment_trends",
        "What are latest trends in the healthcare treatment space?"
    )

    # 2. Is implementing this particular healthcare treatment risky?
    print("\n--- Treatment Risk Query ---")
    orchestrator.run_pipeline(
        "treatment_risk",
        "Is implementing this particular healthcare treatment risky?"
    )

    # 3. What is the revenue and profit projection if we implement this healthcare treatment?
    print("\n--- Revenue Projection Query ---")
    orchestrator.run_pipeline(
        "revenue_projection",
        "What is the revenue and profit projection if we implement this healthcare treatment?"
    )

    # 4. What are the latest marketing campaigns?
    print("\n--- Marketing Campaigns Query ---")
    orchestrator.run_pipeline(
        "marketing_campaigns",
        "What are the latest marketing campaigns?"
    )

    # 5. Give some analysis of the ROI of these campaigns.
    print("\n--- ROI Analysis Query ---")
    orchestrator.run_pipeline(
        "roi_analysis",
        "Give some analysis of the ROI of these campaigns."
    ) 
