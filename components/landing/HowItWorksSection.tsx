import { motion } from "framer-motion";

const steps = [
  {
    num: "01",
    title: "Plan",
    desc: "Define your learning objectives and let the AI craft a personalized curriculum tailored to your goals.",
  },
  {
    num: "02",
    title: "Learn",
    desc: "Follow structured modules with interactive exercises, real-time feedback, and AI-powered explanations.",
  },
  {
    num: "03",
    title: "Build",
    desc: "Apply your knowledge through hands-on projects guided by intelligent code assistance.",
  },
  {
    num: "04",
    title: "Master",
    desc: "Track your progress, fill knowledge gaps, and achieve true mastery with adaptive review.",
  },
];

const HowItWorksSection = () => (
  <section id="how-it-works" className="relative px-6 py-28">
    <div className="mx-auto max-w-6xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="mb-16 text-center"
      >
        <p className="mb-2 font-mono-code text-xs uppercase tracking-[0.3em] text-primary">
          How It Works
        </p>
        <h2 className="font-display text-4xl font-bold sm:text-5xl">
          From <span className="italic text-gradient-red">Plan</span> to{" "}
          <span className="italic text-gradient-red">Mastery</span>
        </h2>
      </motion.div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {steps.map((step, i) => (
          <motion.div
            key={step.num}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: i * 0.1 }}
            className="glass-card p-6"
          >
            <span className="font-mono-code text-3xl font-bold text-primary/40">
              {step.num}
            </span>
            <h3 className="mt-3 font-display text-xl font-bold">{step.title}</h3>
            <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
              {step.desc}
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default HowItWorksSection;
