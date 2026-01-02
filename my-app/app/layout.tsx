import "./globals.css";
import Link from "next/link";
import { ReactNode } from "react";
import Navbar from "@/components/Navbar";

export const metadata = {
  title: "WorkJournal.ai",
  description: "Think. Journal. Reflect.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-neutral-50 text-neutral-900">
        <Navbar />
        <main className="px-6 py-6">{children}</main>
      </body>
    </html>
  );
}
