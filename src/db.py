import base64
import json
import requests
import streamlit as st
from typing import Dict
from dataclasses import dataclass

@dataclass
class GithubClient:
    token: str = st.secrets["GITHUB_TOKEN"]
    repo: str = "RobboTurner/merlindata"
    branch: str = "main"
    game_id: int = 1

    def __post_init__(self) -> None:
        self.url = f"https://api.github.com/repos/{self.repo}/contents/data/game_{self.game_id}.json?ref={self.branch}"
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.refresh_metadata()

    def refresh_metadata(self) -> None:
        """Fetch latest SHA + content metadata."""
        response = requests.get(self.url, headers=self.headers)

        if response.status_code == 404:
            # File does not exist so create an empty json
            self.current_data = None
            self.sha = None
        else:
            self.current_data = response.json()
            self.sha = self.current_data.get("sha")

    def read_github_json(self) -> Dict:
        """Download and decode JSON file."""
        self.refresh_metadata()

        if self.current_data is not None:
            encoded = self.current_data["content"]
            decoded = base64.b64decode(encoded).decode()
            return json.loads(decoded)
        
        else:
            return {}
        

    def write_github_json(self, new_data: Dict) -> None:
        """Upload updated JSON to GitHub."""
        content = json.dumps(new_data)
        encoded = base64.b64encode(content.encode()).decode()

        payload = {
            "message": "Update JSON",
            "content": encoded,
            "sha": self.sha,
            "branch":self.branch
        }

        response = requests.put(self.url, headers=self.headers, json=payload).json()
        print(response)

        
    def update_github_json(self, new_data: Dict) -> None:
        """Append or merge new data into existing JSON."""
        data = self.read_github_json()
        data.update(new_data)
        self.write_github_json(data)