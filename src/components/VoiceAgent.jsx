import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast.jsx";
import { useConversation } from "@elevenlabs/react";
import { Phone, X, Activity, Sparkles, Zap } from "lucide-react";
import { cn } from "@/lib/utils";

// --- DEMO PERSONAS (Knowledge Bases) ---
const PERSONAS = {
  GENERAL: `You are the AI concierge for Anaconda Aesthetics. Be professional, high-tech, and concise. Your goal is to book a demo of our AI software.`,

  INJECTOR: `You are the AI Assistant for Cosmetic Injectables Center in Sherman Oaks, working for Dr. Sherly Soleiman. 

             Services: Fillers, Botox, Threads, Kybella. 

             Tone: Luxury, medical, warm.

             Goal: If they mention looking tired or aging, suggest a consultation for Threads or Fillers. 

             Objection: If asked about price, say "Dr. Soleiman requires an in-person assessment for exact pricing."`,

  BODY: `You are the Front Desk AI for Blue Medi Spa. 

         Services: Weight Loss (Semaglutide), CoolSculpting, Botox.

         Tone: Energetic, results-focused.

         Goal: Qualify them for the Weight Loss Program. Ask "Are you looking to slim down for an event?"`,

  ADDA_BROWS: `You are Adda, the friendly AI assistant for Anaconda Brows brow microblading and permanent makeup services.

               Services: Microblading, Powder Brows, Combo Brows, Lip Blush, Eyeliner, Touch-ups.

               Tone: Warm, professional, encouraging, and knowledgeable about permanent makeup.

               Goal: Help visitors understand the benefits of permanent brows, answer questions about the process, and book consultations.

               Key Points:
               - Permanent brows last 2-3 years with proper care
               - Saves 15 minutes every morning - no daily makeup needed
               - Pain is minimal with numbing cream
               - Healing takes about 2 weeks
               - Touch-up sessions available to perfect results

               Objections:
               - Price: "The investment pays for itself - think of all the time and money saved on daily brow products and appointments!"
               - Pain: "Most clients describe it as a light scratching sensation. We use numbing cream to ensure comfort."
               - Permanence: "The pigment fades naturally over 2-3 years, so you can always adjust the style at your touch-up."
               
               Always be encouraging and help them see the value of waking up with perfect brows every day!`
};

const VoiceAgent = () => {
  const { toast } = useToast();
  const [isOpen, setIsOpen] = useState(false);
  const [activeMode, setActiveMode] = useState("General");
  
  // Get agent ID from environment variable
  const agentId = import.meta.env.VITE_ELEVENLABS_AGENT_ID;
  
  // Initialize Eleven Labs conversation hook
  const conversation = useConversation({
    onConnect: () => {
      console.log("Eleven Labs connected");
      toast({ 
        title: "AI Agent Online", 
        description: "Listening...", 
        className: "bg-emerald-500 text-white border-none" 
      });
    },
    onDisconnect: () => {
      console.log("Eleven Labs disconnected");
      toast({ 
        title: "Disconnected", 
        description: "Conversation ended.",
        variant: "default"
      });
    },
    onMessage: (message) => {
      console.log("Message:", message);
      // Handle different message types if needed
      if (message.type === 'user_transcript') {
        // User spoke
      } else if (message.type === 'agent_response') {
        // Agent responded
      }
    },
    onError: (error) => {
      console.error("Eleven Labs error:", error);
      toast({ 
        title: "Connection Error", 
        description: error.message || "An error occurred",
        variant: "destructive" 
      });
    },
    // Use conversation overrides for persona switching
    overrides: {
      agent: {
        prompt: {
          prompt: PERSONAS[activeMode.toUpperCase().replace(' ', '_')] || PERSONAS.GENERAL
        }
      }
    }
  });

  // Visualizer State - use Eleven Labs audio data if available
  const [volumeBars, setVolumeBars] = useState([10, 10, 10, 10, 10]);

  // Update visualizer based on speaking state
  useEffect(() => {
    if (conversation.isSpeaking) {
      const interval = setInterval(() => {
        // Get frequency data if available
        try {
          const frequencyData = conversation.getOutputByteFrequencyData?.();
          if (frequencyData && frequencyData.length >= 5) {
            const bars = Array.from({ length: 5 }, (_, i) => {
              const index = Math.floor((i / 5) * frequencyData.length);
              return Math.min(100, (frequencyData[index] / 255) * 100);
            });
            setVolumeBars(bars.map(v => Math.max(15, v)));
          } else {
            // Fallback to random animation
            setVolumeBars(Array.from({ length: 5 }, () => Math.floor(Math.random() * 80) + 15));
          }
        } catch (e) {
          // Fallback to random animation
          setVolumeBars(Array.from({ length: 5 }, () => Math.floor(Math.random() * 80) + 15));
        }
      }, 100);
      return () => clearInterval(interval);
    } else {
      setVolumeBars([10, 10, 10, 10, 10]);
    }
  }, [conversation.isSpeaking]);

  const connect = async () => {
    try {
      // Request microphone permission first
      await navigator.mediaDevices.getUserMedia({ audio: true });

      if (!agentId) {
        toast({
          title: "Configuration Error",
          description: "Eleven Labs Agent ID not configured. Please set VITE_ELEVENLABS_AGENT_ID in your environment variables.",
          variant: "destructive"
        });
        return;
      }

      // Start the conversation with Eleven Labs
      await conversation.startSession({
        agentId: agentId,
        connectionType: 'webrtc', // or 'websocket' - WebRTC typically has lower latency
        userId: `user_${Date.now()}` // Optional: track user sessions
      });
    } catch (error) {
      console.error("Connection failed:", error);
      if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
        toast({ 
          title: "Microphone Permission Denied", 
          description: "Please allow microphone access to use the voice agent.",
          variant: "destructive" 
        });
      } else {
        toast({ 
          title: "Connection Failed", 
          description: error.message || "Could not connect to voice agent.",
          variant: "destructive" 
        });
      }
    }
  };

  const disconnect = async () => {
    try {
      await conversation.endSession();
    } catch (error) {
      console.error("Disconnect error:", error);
    }
  };

  // Switch persona using conversation overrides
  const switchPersona = async (mode, instructions) => {
    setActiveMode(mode);
    
    if (conversation.status === 'connected') {
      // Update the conversation with new prompt
      // Note: Eleven Labs SDK handles this through the overrides prop,
      // but we may need to reconnect to apply new prompts in some cases
      toast({ 
        title: `Switched to ${mode} Mode`, 
        description: "AI context updated.",
        className: "bg-slate-800 text-emerald-400 border-emerald-500/20" 
      });
    } else {
      toast({ title: "Connect first", description: "Start the call to switch modes." });
    }
  };

  const isConnected = conversation.status === 'connected';
  const isListening = conversation.isSpeaking || isConnected;

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end font-sans">
      
      {/* Floating Action Button */}
      {!isOpen && (
        <div className="relative group">
           <div className="absolute -top-12 right-0 bg-white text-slate-900 px-4 py-2 rounded-lg shadow-xl text-sm font-bold animate-bounce whitespace-nowrap">
            Try the Live Demo 💬
            <div className="absolute bottom-[-6px] right-6 w-3 h-3 bg-white rotate-45"></div>
          </div>
          <Button
            onClick={() => setIsOpen(true)}
            className="h-16 w-16 rounded-full bg-emerald-500 hover:bg-emerald-400 shadow-lg shadow-emerald-500/40 flex items-center justify-center transition-all duration-300 hover:scale-110"
          >
            <Phone className="h-8 w-8 text-slate-900 animate-pulse" />
          </Button>
        </div>
      )}

      {/* Main Widget Interface */}
      <div className={cn("transition-all duration-500 ease-out transform origin-bottom-right", isOpen ? "scale-100 opacity-100" : "scale-95 opacity-0 pointer-events-none absolute")}>
        <Card className="w-[360px] bg-slate-950 border border-slate-800 shadow-2xl overflow-hidden flex flex-col relative rounded-3xl glow-emerald">
          
          {/* HIDDEN CONTEXT SWITCHER (Click top bar) */}
          <div className="absolute top-0 left-0 w-full h-4 z-20 flex opacity-0 hover:opacity-100 transition-opacity cursor-pointer bg-slate-900/80 backdrop-blur-sm">
            <div onClick={() => switchPersona("General", PERSONAS.GENERAL)} className="flex-1 hover:bg-emerald-500/50" title="General Mode" />
            <div onClick={() => switchPersona("Injector", PERSONAS.INJECTOR)} className="flex-1 hover:bg-pink-500/50" title="Injector (Dr. Soleiman)" />
            <div onClick={() => switchPersona("Body", PERSONAS.BODY)} className="flex-1 hover:bg-cyan-500/50" title="Body (Blue Spa)" />
            <div onClick={() => switchPersona("Adda Brows", PERSONAS.ADDA_BROWS)} className="flex-1 hover:bg-purple-500/50" title="Adda Brows" />
          </div>

          {/* Header */}
          <div className="p-6 bg-gradient-to-b from-slate-900 to-slate-950 flex flex-col items-center pt-10 pb-8 border-b border-slate-800/50">
            <div className="relative mb-4">
              <div className={cn("h-20 w-20 rounded-full flex items-center justify-center border-2 shadow-[0_0_30px_rgba(16,185,129,0.3)] transition-colors duration-500", 
                activeMode === 'Injector' ? "border-pink-500/50 bg-pink-900/20" : 
                activeMode === 'Body' ? "border-cyan-500/50 bg-cyan-900/20" :
                activeMode === 'Adda Brows' ? "border-purple-500/50 bg-purple-900/20" :
                "border-emerald-500/30 bg-emerald-900/20"
              )}>
                 {activeMode === 'Injector' ? <Sparkles className="h-8 w-8 text-pink-400"/> : 
                  activeMode === 'Body' ? <Zap className="h-8 w-8 text-cyan-400"/> : 
                  activeMode === 'Adda Brows' ? <Sparkles className="h-8 w-8 text-purple-400"/> :
                  <Activity className="h-8 w-8 text-emerald-400" />}
              </div>
              {isConnected && (
                <div className="absolute bottom-0 right-0 h-5 w-5 rounded-full bg-emerald-500 border-4 border-slate-950 flex items-center justify-center animate-pulse">
                  <div className="h-1.5 w-1.5 rounded-full bg-white" />
                </div>
              )}
            </div>
            
            <h3 className="text-xl font-bold text-white tracking-tight">
              {activeMode === 'Adda Brows' ? 'Adda' : 'Anaconda AI'}
            </h3>
            <p className="text-xs font-medium text-slate-500 uppercase tracking-widest mt-1 flex items-center gap-2">
              <span className={cn("w-2 h-2 rounded-full", isConnected ? "bg-emerald-500" : "bg-slate-600")}></span>
              {activeMode} Concierge
            </p>
          </div>

          {/* Waveform Visualizer */}
          <div className="h-32 flex items-center justify-center gap-1.5 bg-slate-950 relative overflow-hidden">
            {/* Dynamic Background Glow */}
            <div className={cn("absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-40 h-40 blur-[60px] rounded-full transition-colors duration-700",
               activeMode === 'Injector' ? "bg-pink-500/20" : 
               activeMode === 'Body' ? "bg-cyan-500/20" :
               activeMode === 'Adda Brows' ? "bg-purple-500/20" :
               "bg-emerald-500/20"
            )} />
            
            {volumeBars.map((h, i) => (
              <div 
                key={i}
                className={cn("w-2 rounded-full transition-all duration-100 ease-in-out", 
                  activeMode === 'Injector' ? "bg-pink-400" : 
                  activeMode === 'Body' ? "bg-cyan-400" :
                  activeMode === 'Adda Brows' ? "bg-purple-400" :
                  "bg-emerald-400"
                )}
                style={{ 
                  height: isListening ? `${Math.max(15, h)}%` : '4px', 
                  opacity: isListening ? 1 : 0.3 
                }}
              />
            ))}
            {!isConnected && <p className="absolute text-slate-600 text-sm">Ready to Connect</p>}
          </div>

          {/* Controls */}
          <div className="p-6 bg-slate-900 flex justify-center items-center gap-6 z-10 relative">
             <Button 
                onClick={() => setIsOpen(false)}
                variant="ghost" size="icon" className="text-slate-500 hover:text-white"
             >
               <X className="h-5 w-5" />
             </Button>

             {!isConnected ? (
               <Button 
                 onClick={connect}
                 className="h-14 px-8 rounded-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold shadow-lg shadow-emerald-500/20"
               >
                 Start Call
               </Button>
             ) : (
               <Button 
                 onClick={disconnect}
                 className="h-14 w-14 rounded-full bg-red-500/10 text-red-500 hover:bg-red-500 hover:text-white border border-red-500/20"
               >
                 <Phone className="h-6 w-6 rotate-[135deg]" />
               </Button>
             )}

             <div className="w-10" /> {/* Spacer for centering */}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default VoiceAgent;
