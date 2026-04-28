import { useEffect, useState } from "react";
import "./App.css";

export default function App() {
  const [projects, setProjects] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  const API = "https://ai-project-generator-ppa5.onrender.com";

  const fetchProjects = () => {
    fetch(`${API}/projects`)
      .then(res => res.json())
      .then(data => setProjects(data));
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const generateProject = async () => {
    if (!prompt.trim()) return;

    setLoading(true);

    await fetch(`${API}/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt })
    });

    setPrompt("");
    setLoading(false);
    fetchProjects();
  };

  return (
    <div className="container">
      <h1 className="title"> AI Project Generator</h1>

      {/* 🔹 Generate Section */}
      <div className="input-section">
        <input
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your idea..."
          className="input"
        />

        <button onClick={generateProject} disabled={loading}>
          {loading ? "Generating..." : "Generate"}
        </button>
      </div>

      {/* 🔹 Project List */}
      <h2 className="subtitle">📁 Previous Projects</h2>

      {projects.length === 0 && <p>No projects yet</p>}

      <div className="projects-grid">
        {projects.map((p) => (
          <div key={p.id} className="card">
            <h3>{p.name}</h3>
            <p>{p.prompt}</p>

            <p>
              <strong>Tech:</strong> {p.tech_stack.join(", ")}
            </p>

            <p>
              <strong>Created:</strong>{" "}
              {new Date(p.created_at).toLocaleString()}
            </p>

            <div className="buttons">
              <button
                onClick={() =>
                  window.open(`${API}/preview/${p.id}/index.html`, "_blank")
                }
              >
                👀 Preview
              </button>

              <button
                onClick={() =>
                  window.open(`${API}/download/${p.id}`)
                }
              >
                ⬇ Download
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}