"use client";

interface Props {
  onFileSelect: (file: File) => void;
}

export default function UploadZone({ onFileSelect }: Props) {
  return (
    <div
      style={{
        border: "2px dashed #64748b",
        padding: 40,
        borderRadius: 16,
        textAlign: "center",
      }}
    >
      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) onFileSelect(file);
        }}
      />
    </div>
  );
}
