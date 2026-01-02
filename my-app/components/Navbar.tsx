"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { name: "Chat", href: "/" },
  { name: "Journal", href: "/journal" },
  { name: "Reflect", href: "/reflect" },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="w-full border-b bg-white">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        
        {/* Logo – extreme left */}
        <Link
          href="/"
          className="text-xl font-semibold tracking-tight text-neutral-900"
        >
          WorkJournal<span className="text-neutral-500">.ai</span>
        </Link>

        {/* Nav items – extreme right */}
        <div className="flex items-center gap-8">
          {navItems.map((item) => {
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.name}
                href={item.href}
                className={`text-sm font-medium transition-colors ${
                  isActive
                    ? "text-neutral-900 border-b-2 border-neutral-900 pb-1"
                    : "text-neutral-500 hover:text-neutral-900"
                }`}
              >
                {item.name}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
