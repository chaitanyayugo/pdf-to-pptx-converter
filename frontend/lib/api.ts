export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export async function uploadPDF(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await response.text());
  }

  return response.json();
}

export async function getStatus(jobId: string) {
  const response = await fetch(`${API_BASE}/status/${jobId}`);
  return response.json();
}
