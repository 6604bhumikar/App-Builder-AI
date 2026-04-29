const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8100";

export async function generateProject(payload) {
  const response = await fetch(`${API_BASE_URL}/api/projects/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Project generation failed");
  }

  return response.json();
}

export async function listProjects() {
  const response = await fetch(`${API_BASE_URL}/api/projects`);

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Could not load project history");
  }

  return response.json();
}

export function manifestUrl(projectId) {
  return `${API_BASE_URL}/api/projects/${projectId}/manifest`;
}
