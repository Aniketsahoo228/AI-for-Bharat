import { motion } from "framer-motion";

const techStack = [
  "React", "TypeScript", "Tailwind CSS", "Framer Motion",
  "Supabase", "Vite", "Shadcn/UI", "OpenAI",
];

const CreditsSection = () => (
  <section id="credits" className="relative px-6 py-28">
    <div className="mx-auto max-w-4xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="mb-16 text-center"
      >
        <p className="mb-2 font-mono-code text-xs uppercase tracking-[0.3em] text-primary">
          Built With
        </p>
        <h2 className="font-display text-4xl font-bold sm:text-5xl">
          Technologies & <span className="italic text-gradient-red">Credits</span>
        </h2>
      </motion.div>

      <div className="flex flex-wrap justify-center gap-3">
        {techStack.map((tech, i) => (
          <motion.span
            key={tech}
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.3, delay: i * 0.05 }}
            className="rounded-full border border-border bg-secondary/50 px-5 py-2 font-mono-code text-xs uppercase tracking-wider text-muted-foreground transition-colors hover:border-primary hover:text-primary"
          >
            {tech}
          </motion.span>
        ))}
      </div>

      <motion.p
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ delay: 0.4, duration: 0.6 }}
        className="mt-12 text-center text-sm leading-relaxed text-muted-foreground"
      >
        FUSION×MATRIX is an open learning platform built with modern web technologies
        and powered by cutting-edge AI. Crafted with passion for learners worldwide.
      </motion.p>

      <motion.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ delay: 0.5, duration: 0.6 }}
        className="mt-10 text-center"
      >
        <p className="font-mono-code text-xs text-muted-foreground/60">
          © {new Date().getFullYear()} FUSION×MATRIX — All rights reserved
        </p>
      </motion.div>
    </div>
  </section>
);

export default CreditsSection;
