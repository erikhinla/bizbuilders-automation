/**
 * AudioRecorder - Records audio from microphone and provides chunks via callback
 */
export class AudioRecorder {
  constructor(onAudioData) {
    this.onAudioData = onAudioData;
    this.mediaStream = null;
    this.audioContext = null;
    this.processor = null;
    this.source = null;
    this.isRecording = false;
  }

  async start() {
    try {
      // Request microphone access
      this.mediaStream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          channelCount: 1,
          sampleRate: 24000,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        }
      });

      // Create audio context with 24kHz sample rate (matching backend)
      this.audioContext = new AudioContext({ sampleRate: 24000 });

      // Create source from media stream
      this.source = this.audioContext.createMediaStreamSource(this.mediaStream);

      // Create script processor for audio chunks (4096 buffer size)
      this.processor = this.audioContext.createScriptProcessor(4096, 1, 1);

      // Process audio chunks
      this.processor.onaudioprocess = (event) => {
        if (this.isRecording) {
          const inputBuffer = event.inputBuffer;
          const inputData = inputBuffer.getChannelData(0);
          
          // Convert Float32Array to Int16Array (PCM format)
          const int16Data = new Int16Array(inputData.length);
          for (let i = 0; i < inputData.length; i++) {
            // Clamp to [-1, 1] and convert to 16-bit integer
            const s = Math.max(-1, Math.min(1, inputData[i]));
            int16Data[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
          }
          
          // Send audio data to callback
          if (this.onAudioData) {
            this.onAudioData(int16Data);
          }
        }
      };

      // Connect processor
      this.source.connect(this.processor);
      this.processor.connect(this.audioContext.destination);

      this.isRecording = true;
      return true;
    } catch (error) {
      console.error('AudioRecorder start error:', error);
      throw error;
    }
  }

  stop() {
    this.isRecording = false;

    if (this.processor) {
      this.processor.disconnect();
      this.processor = null;
    }

    if (this.source) {
      this.source.disconnect();
      this.source = null;
    }

    if (this.audioContext && this.audioContext.state !== 'closed') {
      this.audioContext.close();
      this.audioContext = null;
    }

    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach(track => track.stop());
      this.mediaStream = null;
    }
  }
}

/**
 * Encode audio data as base64 for API transmission
 */
export function encodeAudioForAPI(audioData) {
  // Convert Int16Array to base64
  const bytes = new Uint8Array(audioData.buffer);
  let binary = '';
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

