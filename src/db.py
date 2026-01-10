import base64
import json
import requests
import streamlit as st
from typing import Dict
from dataclasses import dataclass

@dataclass
class GithubClient:
    token: str = st.secrets["GITHUB_TOKEN"]
    repo: str = "RobboTurner/merlin"
    file: str = "data/state.json"
    branch: str = "data"

    def __post_init__(self):
        self.url = f"https://api.github.com/repos/{self.repo}/contents/{self.file}?ref={self.branch}"
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.refresh_metadata()

    def refresh_metadata(self):
        """Fetch latest SHA + content metadata."""
        self.current_data = requests.get(self.url, headers=self.headers).json()
        self.sha = self.current_data.get("sha")

    def read_github_json(self) -> Dict:
        """Download and decode JSON file."""
        self.refresh_metadata()
        encoded = self.current_data["content"]
        decoded = base64.b64decode(encoded).decode()
        return json.loads(decoded)

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