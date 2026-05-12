"use client";

import { useMemo, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jobId, setJobId] = useState<string>("");
  const [status, setStatus] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const downloadUrl = useMemo(() => (jobId ? `${API_BASE}/download/${jobId}` : ""), [jobId]);

  async function handleUpload() {
    if (!file) return;
    setLoading(true);
    setStatus("Uploading...");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(await res.text());
      }

      const data = await res.json();
      setJobId(data.job_id);
      setStatus("Queued");
    } catch (e: any) {
      setStatus(`Error: ${e.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function checkStatus() {
    if (!jobId) return;
    const res = await fetch(`${API_BASE}/status/${jobId}`);
    const data = await res.json();
    setStatus(`${data.status} (${data.progress}%)`);
  }

  return (
    <main style={{ maxWidth: 900, margin: "40px auto", padding: 24, fontFamily: "Arial" }}>
      <h1>PDF to PPTX Converter</h1>
      <p>Upload a PDF and convert it to a PPTX presentation.</p>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <div style={{ marginTop: 16, display: "flex", gap: 12 }}>
        <button onClick={handleUpload} disabled={!file || loading}>
          {loading ? "Working..." : "Upload & Convert"}
        </button>
        <button onClick={checkStatus} disabled={!jobId}>
          Check Status
        </button>
      </div>

      <p style={{ marginTop: 16 }}><strong>Status:</strong> {status}</p>

      {jobId && (
        <p>
          <strong>Job ID:</strong> {jobId}
          <br />
          <a href={downloadUrl} target="_blank" rel="noreferrer">
            Download PPTX
          </a>
        </p>
      )}
    </main>
  );
}
