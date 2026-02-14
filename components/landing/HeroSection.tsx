import { motion } from "framer-motion";

const HeroSection = () => (
  <section
    id="hero"
    className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-6 pt-20"
  >
    {/* Watermark */}
    <div className="watermark-text left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 whitespace-nowrap">
      FUSION-MATRIX
    </div>

    {/* Radial glow */}
    <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_center,_hsl(0_85%_20%/0.15)_0%,_transparent_70%)]" />

    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.9, ease: "easeOut" }}
      className="relative z-10 text-center"
    >
      <p className="mb-4 font-mono-code text-xs uppercase tracking-[0.3em] text-muted-foreground">
        Next-Generation Learning
      </p>
      <h1 className="font-display text-5xl font-black leading-tight tracking-tight sm:text-7xl lg:text-8xl">
        <span className="text-gradient-red">AI-Guided</span>
        <br />
        <span className="text-foreground">Learning Workflow</span>
        <br />
        <span className="italic text-foreground/80">Platform</span>
      </h1>
      <p className="mx-auto mt-6 max-w-xl text-base text-muted-foreground sm:text-lg">
        Master any technology through structured, AI-driven learning paths —
        from plan to mastery, guided every step of the way.
      </p>

      <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
        <a
          href="#how-it-works"
          className="rounded-lg bg-primary px-8 py-3 text-sm font-bold uppercase tracking-widest text-primary-foreground transition-all hover:bg-accent hover:shadow-[0_0_30px_hsl(0_85%_45%/0.4)]"
        >
          Get Started
        </a>
        <a
          href="#features"
          className="rounded-lg border border-border px-8 py-3 text-sm font-bold uppercase tracking-widest text-foreground transition-colors hover:border-primary hover:text-primary"
        >
          Deep Dive
        </a>
      </div>
    </motion.div>

    {/* Social links */}
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.6, duration: 0.8 }}
      className="absolute bottom-10 z-10 flex gap-6"
    >
      {["Slack", "CodeCanyon", "Discord"].map((name) => (
        <span
          key={name}
          className="cursor-pointer font-mono-code text-xs uppercase tracking-widest text-muted-foreground transition-colors hover:text-primary"
        >
          {name}
        </span>
      ))}
    </motion.div>
  </section>
);

export default HeroSection;
