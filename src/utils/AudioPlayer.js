/**
 * AudioQueue - Manages playback of audio chunks from the API
 */
export class AudioQueue {
  constructor(audioContext) {
    this.audioContext = audioContext;
    this.queue = [];
    this.isPlaying = false;
    this.currentSource = null;
    this.startTime = null;
    this.nextStartTime = 0;
  }

  async addToQueue(audioData) {
    try {
      // Assume audioData is Uint8Array PCM data (24kHz, mono, 16-bit)
      // Decode PCM to AudioBuffer
      const audioBuffer = await this.decodePCM(audioData);
      
      if (audioBuffer) {
        this.queue.push(audioBuffer);
        if (!this.isPlaying) {
          this.playQueue();
        }
      }
    } catch (error) {
      console.error('AudioQueue addToQueue error:', error);
    }
  }

  async decodePCM(pcmData) {
    try {
      // PCM 16-bit, mono, 24kHz
      const sampleRate = 24000;
      const numChannels = 1;
      const length = pcmData.length / 2; // 2 bytes per sample (16-bit)
      
      const audioBuffer = this.audioContext.createBuffer(numChannels, length, sampleRate);
      const channelData = audioBuffer.getChannelData(0);
      
      // Convert Int16 PCM to Float32 (-1 to 1)
      const view = new DataView(pcmData.buffer);
      for (let i = 0; i < length; i++) {
        const int16 = view.getInt16(i * 2, true); // little-endian
        channelData[i] = int16 / 0x8000; // Normalize to [-1, 1]
      }
      
      return audioBuffer;
    } catch (error) {
      console.error('decodePCM error:', error);
      return null;
    }
  }

  async playQueue() {
    if (this.isPlaying || this.queue.length === 0) {
      return;
    }

    this.isPlaying = true;

    while (this.queue.length > 0) {
      const audioBuffer = this.queue.shift();
      
      // Create buffer source
      const source = this.audioContext.createBufferSource();
      source.buffer = audioBuffer;
      source.connect(this.audioContext.destination);

      // Schedule playback
      if (this.startTime === null) {
        this.startTime = this.audioContext.currentTime;
        this.nextStartTime = this.startTime;
      }

      source.start(this.nextStartTime);
      this.nextStartTime += audioBuffer.duration;

      // Wait for this chunk to finish before playing next
      await new Promise(resolve => {
        source.onended = resolve;
      });
    }

    this.isPlaying = false;
    this.startTime = null;
    this.nextStartTime = 0;
  }

  clear() {
    this.queue = [];
    if (this.currentSource) {
      try {
        this.currentSource.stop();
      } catch (e) {
        // Source might already be stopped
      }
      this.currentSource = null;
    }
    this.isPlaying = false;
    this.startTime = null;
    this.nextStartTime = 0;
  }
}

