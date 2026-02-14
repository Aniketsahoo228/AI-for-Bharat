import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";

const navLinks = [
  { label: "Intro", href: "#hero" },
  { label: "Services", href: "#how-it-works" },
  { label: "Project", href: "#features" },
  { label: "Credits", href: "#credits" },
];

interface NavbarProps {
  onLaunchClick: () => void;
}

const Navbar = ({ onLaunchClick }: NavbarProps) => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <nav
      className={cn(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-300",
        scrolled ? "bg-background/90 backdrop-blur-md border-b border-border" : "bg-transparent"
      )}
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <a href="#hero" className="font-display text-xl font-bold tracking-wider">
          <span className="text-gradient-red">FUSION</span>
          <span className="text-muted-foreground">×</span>
          <span className="text-foreground">MATRIX</span>
        </a>
        <div className="hidden items-center gap-8 md:flex">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="text-sm font-medium uppercase tracking-widest text-muted-foreground transition-colors hover:text-primary"
            >
              {link.label}
            </a>
          ))}
        </div>
        <button
          onClick={onLaunchClick}
          className="rounded-md border border-primary/50 bg-primary px-4 py-2 text-xs font-semibold uppercase tracking-widest text-white transition-all hover:bg-primary/90 hover:shadow-[0_0_30px_hsl(0_85%_45%/0.4)]"
        >
          Launch
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
