import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { Bot, Braces, CheckCircle2, FileCode2, GitBranch, Play, ShieldCheck } from "lucide-react";
import { generateProject } from "./lib/api";
import "./styles.css";

const starterPrompt =
  "Build a SaaS CRM with authentication, dashboard analytics, billing, team roles, audit logs, API docs, and automated tests. Use React for the frontend and FastAPI for the backend.";

function App() {
  const [prompt, setPrompt] = useState(starterPrompt);
  const [targetStack, setTargetStack] = useState("react-fastapi");
  const [includeTests, setIncludeTests] = useState(true);
  const [includeDocker, setIncludeDocker] = useState(true);
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fileCounts = useMemo(() => {
    if (!project) return {};
    return project.files.reduce((acc, file) => {
      acc[file.role] = (acc[file.role] || 0) + 1;
      return acc;
    }, {});
  }, [project]);

  async function onGenerate() {
    setLoading(true);
    setError("");
    try {
      const result = await generateProject({ prompt, target_stack: targetStack, include_tests: includeTests, include_docker: includeDocker });
      setProject(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <Bot size={28} />
          <div>
            <h1>App-Builder AI</h1>
            <p>Agentic codebase generation</p>
          </div>
        </div>
        <nav>
          <a className="active"><Play size={16} /> Builder</a>
          <a><GitBranch size={16} /> Workflow</a>
          <a><ShieldCheck size={16} /> Review</a>
        </nav>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Generative AI | LangChain | LangGraph | Pydantic</p>
            <h2>Convert prompts into structured codebase manifests</h2>
          </div>
          <button className="primary" onClick={onGenerate} disabled={loading || prompt.length < 20}>
            <Play size={18} />
            {loading ? "Generating" : "Generate"}
          </button>
        </header>

        <section className="builder-grid">
          <div className="panel prompt-panel">
            <label htmlFor="prompt">Product prompt</label>
            <textarea id="prompt" value={prompt} onChange={(event) => setPrompt(event.target.value)} />
            <div className="controls">
              <label>
                Stack
                <select value={targetStack} onChange={(event) => setTargetStack(event.target.value)}>
                  <option value="react-fastapi">React + FastAPI</option>
                  <option value="nextjs-fastapi">Next.js + FastAPI</option>
                  <option value="mern">MERN</option>
                  <option value="python-cli">Python CLI</option>
                </select>
              </label>
              <label className="check"><input type="checkbox" checked={includeTests} onChange={(event) => setIncludeTests(event.target.checked)} /> Tests</label>
              <label className="check"><input type="checkbox" checked={includeDocker} onChange={(event) => setIncludeDocker(event.target.checked)} /> Docker</label>
            </div>
            {error && <p className="error">{error}</p>}
          </div>

          <div className="panel">
            <h3>Workflow</h3>
            <div className="steps">
              {["Plan", "Architect", "Validate tools", "Generate", "Review"].map((step, index) => (
                <div className="step" key={step}>
                  <span>{index + 1}</span>
                  <p>{step}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {project && (
          <section className="result-grid">
            <div className="panel result-main">
              <div className="section-title">
                <Braces size={20} />
                <h3>{project.blueprint.name}</h3>
              </div>
              <p>{project.blueprint.summary}</p>
              <div className="chips">
                {project.blueprint.core_features.map((feature) => <span key={feature}>{feature}</span>)}
              </div>
            </div>

            <div className="panel score-card">
              <CheckCircle2 size={28} />
              <strong>{project.review.score}</strong>
              <p>Review score</p>
            </div>

            <div className="panel files-panel">
              <div className="section-title">
                <FileCode2 size={20} />
                <h3>Generated files</h3>
              </div>
              <div className="file-counts">
                {Object.entries(fileCounts).map(([role, count]) => <span key={role}>{role}: {count}</span>)}
              </div>
              <div className="file-list">
                {project.files.map((file) => (
                  <details key={file.path}>
                    <summary>{file.path}</summary>
                    <pre>{file.content}</pre>
                  </details>
                ))}
              </div>
            </div>

            <div className="panel">
              <h3>Validated tool calls</h3>
              <ul className="tool-list">
                {project.tool_calls.map((call, index) => <li key={`${call.name}-${index}`}>{call.name}</li>)}
              </ul>
            </div>
          </section>
        )}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
