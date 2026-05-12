import "./globals.css";
import React from "react";

export const metadata = {
  title: "PDF to PPTX Converter",
  description: "Enterprise PDF to PPTX AI converter",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
