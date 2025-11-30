import { Bot, Zap, Database, Globe, Sparkles } from "lucide-react";
import { Card } from "@/components/ui/card";

const Services = () => {
  const services = [
    {
      icon: Bot,
      title: "AI Voice Concierge",
      description: "Books appointments 24/7 with warmth, clarity, and professionalism.",
      color: "text-emerald-400"
    },
    {
      icon: Zap,
      title: "Smart Lead Automation",
      description: "Text, email, and multi-channel sequences that convert interest into booked treatments.",
      color: "text-cyan-400"
    },
    {
      icon: Database,
      title: "Unified CRM Systems",
      description: "Every message, lead, and client touchpoint centralized for efficiency.",
      color: "text-purple-400"
    },
    {
      icon: Globe,
      title: "Website & SEO Optimization",
      description: "A refined digital presence with local search dominance.",
      color: "text-blue-400"
    },
    {
      icon: Sparkles,
      title: "LLM-Ready Content",
      description: "AI agents trained to speak in high-end aesthetic language across your channels.",
      color: "text-pink-400"
    },
  ];

  return (
    <section id="services" className="py-32 bg-slate-950 relative overflow-hidden">
      {/* Background Grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#8080800a_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:40px_40px] opacity-20"></div>

      <div className="container mx-auto px-6 relative z-10">
        <div className="max-w-3xl mx-auto text-center space-y-6 mb-20">
          <h2 className="text-4xl md:text-5xl font-bold text-white text-balance">
            The Aesthetic Intelligence Advantage
          </h2>
          <p className="text-xl text-slate-400 leading-relaxed">
            A complete AI-powered growth framework built and installed for premium clinics.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-7xl mx-auto">
          {services.map((service, index) => (
            <Card key={index} className="group relative overflow-hidden border-slate-800 bg-slate-900/50 p-8 hover:border-emerald-500/50 transition-all duration-300 hover:shadow-[0_0_30px_-10px_rgba(16,185,129,0.2)]">
              <div className="absolute inset-0 bg-gradient-to-b from-emerald-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              
              <div className="relative z-10">
                <div className={`w-14 h-14 rounded-xl bg-slate-800 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 border border-slate-700 group-hover:border-emerald-500/30`}>
                  <service.icon className={`w-7 h-7 ${service.color}`} />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  {service.title}
                </h3>
                <p className="text-slate-400 leading-relaxed">
                  {service.description}
                </p>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Services;

