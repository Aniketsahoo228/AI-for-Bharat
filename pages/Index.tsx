import { useState } from "react";
import Navbar from "@/components/landing/Navbar";
import HeroSection from "@/components/landing/HeroSection";
import HowItWorksSection from "@/components/landing/HowItWorksSection";
import FeaturesSection from "@/components/landing/FeaturesSection";
import CreditsSection from "@/components/landing/CreditsSection";
import Workspace from "@/components/Workspace";

const Index = () => {
  const [showWorkspace, setShowWorkspace] = useState(false);

  if (showWorkspace) {
    return <Workspace />;
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar onLaunchClick={() => setShowWorkspace(true)} />
      <HeroSection />
      <HowItWorksSection />
      <FeaturesSection />
      <CreditsSection />
    </div>
  );
};

export default Index;
