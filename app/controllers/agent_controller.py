from app.services.orchestrator import AgentOrchestrator
from flask import request, jsonify

class AgentController:
    def __init__(self, agent_name=None):
        self.agent_name = agent_name
        self.orchestrator = AgentOrchestrator()

    def run_agent(self, agent_type: str, prompt: str, model: str = None):
        """
        Menjalankan agent dari orchestrator berdasarkan agent_type dan prompt.
        """
        return self.orchestrator.run(agent_type, prompt, model=model)

    def agent_endpoint(self):
        """
        Endpoint universal untuk menjalankan agent.
        Expects JSON: { "agent_type": "...", "prompt": "...", "model": "..." }
        """
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"status": "error", "message": "Invalid or missing JSON body"}), 400

        agent_type = data.get("agent_type")
        prompt = data.get("prompt")
        model = data.get("model")  # optional

        if not agent_type or not prompt:
            return jsonify({"status": "error", "message": "agent_type and prompt are required"}), 400

        try:
            result = self.run_agent(agent_type, prompt, model=model)
            return jsonify({"status": "success", "result": result})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
