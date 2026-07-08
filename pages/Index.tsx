import { useState } from "react";
import Navbar from "@/components/landing/Navbar";
import HeroSection from "@/components/landing/HeroSection";
import HowItWorksSection from "@/components/landing/HowItWorksSection";
import FeaturesSection from "@/components/landing/FeaturesSection";
import CreditsSection from "@/components/landing/CreditsSection";
import Workspace from "@/components/Workspace";

const Index = () => {
  const [showWorkspace, setShowWorkspace] = useState(false);

  const handleLaunch = () => {
    setShowWorkspace(true);
    window.scrollTo(0, 0); // NEW: reset scroll when entering workspace
  };

  const handleBack = () => {
    setShowWorkspace(false); // NEW: return to landing page
    window.scrollTo(0, 0);
  };

  if (showWorkspace) {
    return <Workspace onBack={handleBack} />; // CHANGED: pass onBack prop
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar onLaunchClick={handleLaunch} /> {/* CHANGED: use handleLaunch */}
      <HeroSection />
      <HowItWorksSection />
      <FeaturesSection />
      <CreditsSection />
    </div>
  );
};

export default Index;
