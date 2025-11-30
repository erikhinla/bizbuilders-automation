# Eleven Labs Voice Agent Setup Guide

## ✅ Implementation Complete!

The Voice Agent has been successfully integrated with Eleven Labs Conversational AI. The component now uses the `@elevenlabs/react` SDK for real-time voice conversations.

## 🚀 Quick Setup

### 1. Get Your Eleven Labs Agent ID

1. Go to [Eleven Labs Agents Dashboard](https://elevenlabs.io/app/agents)
2. Create a new agent or select an existing one
3. Copy the **Agent ID** (format: `agent_xxxxxxxxxxxxx`)

### 2. Configure Environment Variables

Create a `.env.local` file in the project root (if it doesn't exist) and add:

```env
VITE_ELEVENLABS_AGENT_ID=your_agent_id_here
```

**Important:** 
- The `.env.local` file is already in `.gitignore` and won't be committed
- Restart your dev server after adding environment variables

### 3. (Optional) Configure Voice Settings

If you want to use a specific voice for your agent:

1. Go to your agent settings in the Eleven Labs dashboard
2. Select your desired voice from your voice library
3. Configure the agent's personality and instructions
4. Save the agent

### 4. Test the Integration

1. Start your dev server: `npm run dev`
2. Navigate to your app
3. Click the floating phone button in the bottom-right corner
4. Click "Start Call" to begin a voice conversation

## 🎯 Features

- ✅ Real-time voice conversations using WebRTC (low latency)
- ✅ Multiple persona modes (General, Injector, Body, Adda Brows)
- ✅ Automatic audio visualization
- ✅ Microphone permission handling
- ✅ Connection status indicators
- ✅ Error handling and user feedback

## 📝 Agent Configuration

The VoiceAgent component supports persona switching. Each persona has custom instructions:

- **General**: Anaconda Aesthetics concierge
- **Injector**: Cosmetic Injectables Center assistant
- **Body**: Blue Medi Spa front desk
- **Adda Brows**: Anaconda Brows assistant (NEW!)

To update persona instructions, edit the `PERSONAS` object in `src/components/VoiceAgent.jsx`.

## 🔒 Security Notes

- The Agent ID is safe to expose on the client side for public agents
- For private agents, you'll need to implement a backend endpoint to generate signed URLs
- Never expose your Eleven Labs API key on the client side

## 🐛 Troubleshooting

### "Eleven Labs Agent ID not configured"
- Make sure `VITE_ELEVENLABS_AGENT_ID` is set in `.env.local`
- Restart your dev server after adding the variable

### "Microphone Permission Denied"
- The browser requires explicit permission to use the microphone
- Make sure you've allowed microphone access when prompted
- Check browser settings if issues persist

### Connection Issues
- Check your internet connection
- Verify the Agent ID is correct
- Check browser console for detailed error messages

## 📚 Resources

- [Eleven Labs React SDK Documentation](https://elevenlabs.io/docs/agents-platform/libraries/react)
- [Eleven Labs Agents Dashboard](https://elevenlabs.io/app/agents)
- [Eleven Labs WebSocket API Docs](https://elevenlabs.io/docs/agents-platform/libraries/web-sockets)

## 🎉 Next Steps

1. Customize the agent's voice and personality in the Eleven Labs dashboard
2. Add more personas or update existing ones
3. Integrate with your booking system (if needed)
4. Test on different devices and browsers

