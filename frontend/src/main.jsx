import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Bot,
  Braces,
  CheckCircle2,
  Clock3,
  Download,
  FileCode2,
  GitBranch,
  Layers3,
  Loader2,
  Play,
  ServerCog,
  ShieldCheck,
  Sparkles,
  TerminalSquare
} from "lucide-react";
import { generateProject, listProjects, manifestUrl } from "./lib/api";
import "./styles.css";

const starterPrompt =
  "Build a SaaS CRM with authentication, dashboard analytics, billing, team roles, audit logs, API docs, and automated tests. Use React for the frontend and FastAPI for the backend.";

const examples = [
  "Create an AI support desk with ticket triage, knowledge base search, team inboxes, SLAs, analytics, and audit logs.",
  "Build an education marketplace with courses, instructors, quizzes, payments, certificates, communities, and admin moderation.",
  "Generate a project management workspace with kanban boards, comments, notifications, file attachments, reports, and API docs."
];

function App() {
  const [prompt, setPrompt] = useState(starterPrompt);
  const [targetStack, setTargetStack] = useState("react-fastapi");
  const [projectType, setProjectType] = useState("saas");
  const [qualityProfile, setQualityProfile] = useState("production");
  const [includeTests, setIncludeTests] = useState(true);
  const [includeDocker, setIncludeDocker] = useState(true);
  const [project, setProject] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    refreshHistory();
  }, []);

  const fileCounts = useMemo(() => {
    if (!project) return {};
    return project.files.reduce((acc, file) => {
      acc[file.role] = (acc[file.role] || 0) + 1;
      return acc;
    }, {});
  }, [project]);

  const totalLines = useMemo(() => {
    if (!project) return 0;
    return project.files.reduce((total, file) => total + file.content.split("\n").length, 0);
  }, [project]);

  async function refreshHistory() {
    setHistoryLoading(true);
    try {
      const projects = await listProjects();
      setHistory(projects);
    } catch {
      setHistory([]);
    } finally {
      setHistoryLoading(false);
    }
  }

  async function onGenerate() {
    setLoading(true);
    setError("");
    try {
      const result = await generateProject({
        prompt,
        target_stack: targetStack,
        project_type: projectType,
        quality_profile: qualityProfile,
        include_tests: includeTests,
        include_docker: includeDocker
      });
      setProject(result);
      await refreshHistory();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function loadExample(index) {
    setPrompt(examples[index]);
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
        <div className="sidebar-card">
          <p>Session projects</p>
          <strong>{history.length}</strong>
          <span>{historyLoading ? "Loading" : "Stored in backend memory"}</span>
        </div>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Generative AI | LangChain | LangGraph | Pydantic</p>
            <h2>Design, validate, and export structured app codebases</h2>
          </div>
          <div className="top-actions">
            {project && (
              <a className="secondary" href={manifestUrl(project.id)}>
                <Download size={18} />
                Export JSON
              </a>
            )}
            <button className="primary" onClick={onGenerate} disabled={loading || prompt.length < 20}>
              {loading ? <Loader2 className="spin" size={18} /> : <Play size={18} />}
              {loading ? "Generating" : "Generate"}
            </button>
          </div>
        </header>

        <section className="builder-grid">
          <div className="panel prompt-panel">
            <div className="section-title split">
              <div>
                <h3>Prompt studio</h3>
                <p>Describe the product, users, workflows, integrations, and constraints.</p>
              </div>
              <Sparkles size={22} />
            </div>
            <label htmlFor="prompt">Product prompt</label>
            <textarea id="prompt" value={prompt} onChange={(event) => setPrompt(event.target.value)} />
            <div className="example-row">
              {examples.map((example, index) => (
                <button key={example} type="button" onClick={() => loadExample(index)}>
                  Example {index + 1}
                </button>
              ))}
            </div>
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
              <label>
                Project type
                <select value={projectType} onChange={(event) => setProjectType(event.target.value)}>
                  <option value="saas">SaaS</option>
                  <option value="marketplace">Marketplace</option>
                  <option value="internal-tool">Internal tool</option>
                  <option value="ai-agent">AI agent</option>
                  <option value="education">Education</option>
                </select>
              </label>
              <label>
                Quality
                <select value={qualityProfile} onChange={(event) => setQualityProfile(event.target.value)}>
                  <option value="prototype">Prototype</option>
                  <option value="production">Production</option>
                  <option value="enterprise">Enterprise</option>
                </select>
              </label>
              <label className="check"><input type="checkbox" checked={includeTests} onChange={(event) => setIncludeTests(event.target.checked)} /> Tests</label>
              <label className="check"><input type="checkbox" checked={includeDocker} onChange={(event) => setIncludeDocker(event.target.checked)} /> Docker</label>
            </div>
            {error && <p className="error">{error}</p>}
          </div>

          <div className="panel">
            <h3>Workflow trace</h3>
            <div className="steps">
              {(project?.workflow_trace || [
                { name: "Prompt intake", detail: "Waiting for a generation request." },
                { name: "Architecture", detail: "Blueprint will appear here." },
                { name: "Tool validation", detail: "Pydantic checks protect tool calls." },
                { name: "Code generation", detail: "Files are emitted as a manifest." },
                { name: "Quality review", detail: "Readiness score closes the loop." }
              ]).map((step, index) => (
                <div className="step" key={`${step.name}-${index}`}>
                  <span>{project ? <CheckCircle2 size={17} /> : index + 1}</span>
                  <div>
                    <p>{step.name}</p>
                    <small>{step.detail}</small>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {!project && (
          <section className="empty-state">
            <Layers3 size={34} />
            <h3>Ready to generate a validated app blueprint</h3>
            <p>Use the default prompt or choose an example, then run the agent workflow.</p>
          </section>
        )}

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

            <div className="metric-grid">
              <div className="panel metric-card">
                <CheckCircle2 size={24} />
                <strong>{project.review.score}</strong>
                <p>Review score</p>
              </div>
              <div className="panel metric-card">
                <FileCode2 size={24} />
                <strong>{project.files.length}</strong>
                <p>Files</p>
              </div>
              <div className="panel metric-card">
                <TerminalSquare size={24} />
                <strong>{totalLines}</strong>
                <p>Lines</p>
              </div>
            </div>

            <InfoPanel icon={<ServerCog size={20} />} title="Architecture" items={project.blueprint.architecture} />
            <InfoPanel icon={<Layers3 size={20} />} title="Data entities" items={project.blueprint.data_entities} />
            <InfoPanel icon={<TerminalSquare size={20} />} title="Run commands" items={project.blueprint.run_commands} code />
            <InfoPanel icon={<ShieldCheck size={20} />} title="Review recommendations" items={project.review.recommendations} />

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

            <div className="panel history-panel">
              <div className="section-title">
                <Clock3 size={20} />
                <h3>Project history</h3>
              </div>
              <div className="history-list">
                {history.map((item) => (
                  <button key={item.id} type="button" onClick={() => setProject(item)}>
                    <strong>{item.blueprint.name}</strong>
                    <span>{new Date(item.created_at).toLocaleString()}</span>
                  </button>
                ))}
              </div>
            </div>
          </section>
        )}
      </section>
    </main>
  );
}

function InfoPanel({ icon, title, items, code = false }) {
  return (
    <div className="panel info-panel">
      <div className="section-title">
        {icon}
        <h3>{title}</h3>
      </div>
      <ul>
        {items.map((item) => (
          <li key={item}>{code ? <code>{item}</code> : item}</li>
        ))}
      </ul>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
