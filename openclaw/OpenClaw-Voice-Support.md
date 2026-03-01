# OpenClaw Voice Support — Nash (NY Library Mac Studio)

## Last Updated: 2026-03-01 5:00 PM EST
## STATUS: WORKING — Twilio voice optimized and tested

## Current Configuration (Optimized 2026-03-01)

### Voice Pipeline
```
Bill speaks → Twilio captures audio → OpenAI Realtime STT (400ms silence detect)
→ Anthropic Haiku 4.5 generates response → ElevenLabs TTS → Twilio streams audio back
```

### Key Settings (openclaw.json → plugins.entries.voice-call.config)
```
provider: twilio
fromNumber: +18553933306 (Nash)
inboundPolicy: allowlist
allowFrom: [+12392274662, +12393492332] (Bill cell + office VOIP)
inboundGreeting: "Hey Bill, Nash here. What can I do for you?"
responseModel: anthropic/claude-haiku-4-5
maxDurationSeconds: 1800 (30 minutes)
silenceTimeoutMs: 400 (was 800 default)
responseTimeoutMs: 15000
skipSignatureVerification: true (dev only)
```

### Streaming Config
```
streaming.enabled: true
streaming.streamPath: /voice/stream
streaming.silenceDurationMs: 400 (was 800 default)
streaming.vadThreshold: 0.6 (was 0.5 default)
streaming.sttProvider: openai-realtime
streaming.sttModel: gpt-4o-transcribe
```

### TTS Config (in voice-call config)
```
tts.provider: elevenlabs
tts.elevenlabs.voiceId: CwhRBWXzGAHq8TQ4Fs17
tts.elevenlabs.modelId: eleven_turbo_v2_5
tts.elevenlabs.voiceSettings:
  stability: 0.7 (was 0.6 — reduces first-word distortion)
  similarityBoost: 0.75 (was 0.8)
  style: 0.1 (was 0.15)
  useSpeakerBoost: true
```

### Voice System Prompt
```
You are Nash, Bill Verhelle's AI assistant, on a phone call. Keep responses
concise and conversational — 2-3 sentences max unless Bill asks for detail.
No markdown, no bullet points, no formatting. Speak naturally like a trusted
advisor on a phone call. If you need to think through something complex, give
a quick summary first, then ask if Bill wants more detail.
```

### Network / Infrastructure
```
Gateway: Port 18800 (localhost)
Voice webhook: Port 3334 (localhost)
Tailscale funnel: https://ny-library-mac-studio.tail3f7308.ts.net
  /voice/webhook → http://127.0.0.1:3334/voice/webhook
  /voice/stream  → http://127.0.0.1:3334
Twilio Phone SID: PN672a9deb5a7bc4f5e639ccb995dff073
Twilio Voice URL: https://ny-library-mac-studio.tail3f7308.ts.net/voice/webhook
```

## Latency Optimization History (Session 34, 2026-03-01)

### Problem: 8-10 second latency per voice turn

### Fixes Applied (in order of impact)
1. **Response model**: Opus 4.6 → Sonnet 4.5 → **Haiku 4.5** (biggest win, ~3-5s saved)
2. **Silence detection**: 800ms → **400ms** (both silenceTimeoutMs and streaming.silenceDurationMs)
3. **VAD threshold**: 0.5 → **0.6** (fewer false "still talking" pauses)
4. **Voice system prompt**: Added concise-response instructions (shorter generation = faster)
5. **TTS stability**: 0.6 → **0.7** (smoother first-word playback, less distortion)
6. **Inbound greeting**: Added instant greeting so Nash speaks immediately on pickup
7. **maxDurationSeconds**: Fixed from 300 default to 1800 (previous field name was wrong)

### Result: ~3-4 second latency (down from 8-10)

### What Did NOT Work
- **OpenAI GPT-5-mini**: High distortion, latency, confused responses. OpenClaw's agent
  pipeline is Anthropic-native; non-Anthropic models go through a compatibility translation
  layer that adds latency and loses prompt fidelity. Voice requires native Anthropic models.
- **Kimi K2.5 (Moonshot)**: Not tested for voice. Asia-based API servers would add 200-400ms
  network round-trip before model even starts thinking. Not viable for real-time voice.

## Model Selection Guide for Voice

| Model | Voice Viable? | Notes |
|-------|:---:|-------|
| anthropic/claude-haiku-4-5 | ✅ BEST | Fastest Anthropic model, native API path |
| anthropic/claude-sonnet-4-5 | ✅ Good | Smarter but ~2x slower than Haiku |
| anthropic/claude-opus-4-6 | ❌ | Too slow for voice (3-5s generation time) |
| openai/gpt-5-mini | ❌ | Translation layer kills latency + quality |
| openai/gpt-5.2 | ❌ | Same translation layer issue |
| moonshot/kimi-k2.5 | ❌ | Asia servers, high network latency |

**Rule: Voice responses must use Anthropic models only.**

## Future Optimization Opportunities

### When Anthropic Releases New Models
- Re-evaluate if a new Haiku successor or speed-tier model is available
- Test any model marketed as "low latency" or "real-time" optimized
- Sonnet successor may become fast enough for voice if inference speed improves

### When Discord Voice Bug Is Fixed
- Upstream bug: @discordjs/voice DAVE E2EE breaks STT (issues #24825, #26108)
- Do NOT attempt Discord voice fix until after April 1, 2026 or new OpenClaw version
- When fixed: Discord voice would bypass Twilio entirely (no telephony latency)
- Will need separate voice config optimized for Discord's audio pipeline
- Discord supports higher quality audio than Twilio's 8kHz mulaw

### Other Potential Improvements
- Monitor OpenClaw issues #9635 and #5338 for streaming TTS buffer fixes
  (would reduce first-word audio distortion)
- ElevenLabs Turbo v3 or successor models may reduce TTS latency
- OpenAI Realtime STT improvements could reduce transcription time
- Consider Deepgram STT as alternative if OpenAI Realtime latency is a bottleneck

## Architecture Reference

### Config Files
- Main: ~/.openclaw/openclaw.json
- TTS settings: ~/.openclaw/settings/tts.json
- Gateway logs: ~/.openclaw/logs/gateway.err.log
- Session logs: ~/.openclaw/workspace/DISCORD-VOICE-SESSION-*.md

### Critical Schema Notes
- voice-call config DOES support `tts` key (with elevenlabs sub-config + voiceSettings)
- voice-call config DOES support `silenceTimeoutMs` at top level
- TTS settings file (~/.openclaw/settings/tts.json): voiceId/modelId MUST be nested
  under `elevenlabs` sub-object, NOT at tts root level
- Field name is `maxDurationSeconds` (NOT maxCallDurationSec)

### Gateway Management
- Restart: `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`
- Or: Config changes auto-trigger gateway restart (watch gateway.err.log for confirmation)
- Stop: `openclaw gateway stop`
- Health: `lsof -i :18800 && lsof -i :3334`

### Crash Prevention (for Claude sessions)
- Do NOT cat full config files — use python3 to extract specific keys
- Do NOT grep entire log files — use tail with small line limits
- Keep osascript outputs under 2000 chars
- Always create/update session log FILE on disk before debugging
