interface Props {
  status: string;
}

export default function ProgressCard({ status }: Props) {
  return (
    <div
      style={{
        marginTop: 20,
        padding: 20,
        borderRadius: 12,
        background: "#1e293b",
      }}
    >
      <strong>Status:</strong> {status}
    </div>
  );
}
