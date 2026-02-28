# OpenClaw Voice Support — Nash (NY Library Mac Studio)
## Last Updated: 2026-02-27 9:50 PM EST

## STATUS: NOT WORKING — Calls hang up immediately

## Problem Statement
Nash (OpenClaw on NY Library Mac Studio) should be able to:
1. RECEIVE calls from Bill at +12392274662 on Twilio number +18553933306
2. MAKE calls from +18553933306 to Bill at +12392274662
3. Use ElevenLabs TTS for Nash voice (voice ID CwhRBWXzGAHq8TQ4Fs17, model eleven_turbo_v2_5)

Current behavior: When Bill calls 855-393-3306, the call is answered then immediately hangs up. This has persisted for DAYS across multiple troubleshooting sessions.

## Architecture
- Host: NYLibraacStudio.localdomain (Mac Studio M4 Max)
- User: williamverhelle
- OpenClaw: Native install (NOT Docker), gateway as launchd service
- Gateway: Port 18800 (localhost), PID varies
- Voice webhook: Port 3334 (localhost)
- Tailscale funnel: https://ny-library-mac-studio.tail3f7308.ts.net
  - /voice/webhook -> http://127.0.0.1:3334/voice/webhook
  - /voice/stream -> http://127.0.0.1:3334
- Twilio phone: +18553933306 (SID: PN672a9deb5a7bc4f5e639ccb995dff073)
- Bill cell: +12392274662

## Credentials
- Twilio Account SID: [TWILIO_SID]
- Twilio Auth Token: [REDACTED_SECRET]
- ElevenLabs API Key: [REDACTED_SECRET] (in gateway env)
- ElevenLabs Voice ID: CwhRBWXzGAHq8TQ4Fs17
- ElevenLabs Model: eleven_turbo_v2_5

## Key Config Files
- ~/.openclaw/openclaw.json — Main config
- ~/.openclaw/settings/tts.json — TTS settings
- ~/.openclaw/settings/voicewake.json — Wake word triggers
- ~/.openclaw/workspace/config/twilio_setup.json — Twilio setup notes
- ~/Library/LaunchAgents/ai.openclaw.gateway.plist — Gateway service
- Gateway binary: ~/.openclaw/tools/node-v22.22.0/bin/node
- Gateway entry: ~/.openclaw/lib/node_modules/openclaw/dist/entry.js

## Log Files (CHECK THESE FIRST)
- ~/.openclaw/logs/gateway.err.log — Check this FIRST for errors
- ~/.openclaw/logs/gateway.log — Main gateway log
- ~/.openclaw/health-monitor.log — Health monitor

## Voice-Call Plugin Config (as of 2026-02-27)
Located at: plugins.entries.voice-call in openclaw.json

enabled: true
provider: twilio
fromNumber: +18553933306
toNumber: +12392274662
twilio.accountSid: [TWILIO_SID]
twilio.authToken: [REDACTED_SECRET]
tailscale.mode: funnel
tailscale.path: /voice/webhook
outbound.defaultMode: notify
inboundPolicy: allowlist
allowFrom: [+12392274662]
inboundGreeting: Hey Bill, it is Nash. What can I help you with?
streaming.enabled: true
streaming.streamPath: /voice/stream
maxDurationSeconds: 300
publicUrl: https://ny-library-mac-studio.tail3f7308.ts.net/voice/webhook
skipSignatureVerification: true

## TTS Config (messages.tts in openclaw.json)

auto: always
provider: elevenlabs
elevenlabs.voiceId: CwhRBWXzGAHq8TQ4Fs17
elevenlabs.modelId: eleven_turbo_v2_5

## TTS Settings File (~/.openclaw/settings/tts.json)

tts.auto: always
tts.provider: elevenlabs
tts.elevenlabs.voiceId: CwhRBWXzGAHq8TQ4Fs17
tts.elevenlabs.modelId: eleven_turbo_v2_5

## Twilio Phone Number Config (verified via API)
- Phone: +18553933306
- Voice URL: https://ny-library-mac-studio.tail3f7308.ts.net/voice/webhook
- Voice Method: POST
- Status Callback: https://ny-library-mac-studio.tail3f7308.ts.net/voice/webhook
- SID: PN672a9deb5a7bc4f5e639ccb995dff073

## Tailscale Funnel Config (verified)
- /voice/webhook -> proxy http://127.0.0.1:3334/voice/webhook
- /voice/stream -> proxy http://127.0.0.1:3334

## What Has Been Verified Working
1. Gateway starts and runs on port 18800
2. Voice webhook port 3334 is listening
3. Local curl to webhook returns TwiML with Connect and Stream
4. Tailscale funnel curl to webhook returns same TwiML
5. Twilio phone number points to correct webhook URL
6. Voice-call plugin initializes: TTS configured, media stream wired, runtime initialized
7. Inbound call from +12392274662 is accepted (in allowlist)
8. Call record is created in logs

## What Is NOT Working
1. Call hangs up immediately after answering — Despite webhook returning valid TwiML
2. The TwiML response is a Connect and Stream (WebSocket media stream), NOT a Say/Play greeting
3. The inboundGreeting config value is NOT being rendered as TwiML Say or Play
4. Possible: WebSocket stream connection fails silently, causing Twilio to drop the call
5. Possible: ElevenLabs TTS generation fails before audio can be streamed
6. Possible: The Stream URL (wss://ny-library-mac-studio.tail3f7308.ts.net/voice/stream) is unreachable from Twilio servers

## Troubleshooting History

### Session 2026-02-21
- First Twilio setup attempt
- Created twilio_setup.json with credentials
- Status: pending_installation

### Session 2026-02-23
- Major architecture rebuild: migrated from Docker to native + OpenClaw.app
- Gateway port changed from 18789 to 18800
- Multiple backup files created

### Session 2026-02-27 (prior chat — crashed about dozen times)
- Installed GitHub CLI, pushed OpenClaw-Context.md to GitHub
- Identified EADDRINUSE port conflicts
- Identified TTS config conflicts between settings files
- Claude crashed repeatedly due to context window overflow from large osascript outputs
- Nash self-identified the voice problem as potential TTS/audio runtime init failure

### Session 2026-02-27 9:35 PM EST (current session)
- Found ROOT CAUSE of config reload blocking: tts.json had wrong schema
  - voiceId/modelId were at tts root instead of under tts.elevenlabs
  - This caused: invalid config tts must NOT have additional properties
  - This error appeared 800+ times in gateway.err.log
  - Config reloads were being SKIPPED due to validation failure
- Fixed tts.json schema
- Verified openclaw.json voice-call config is clean
- Restarted gateway — zero schema errors
- All verification tests pass (webhook, funnel, Twilio config)
- BUT: Live call STILL hangs up immediately — the TTS schema fix was necessary but not sufficient

## Prior Fix Attempt Backups (evidence of repeated work)
- openclaw.json.bak.pre-voice-fix-20260227
- openclaw.json.bak.pre-voicefix-202602271720
- openclaw.json.bak.pre-voicefix-20260227-2052
- openclaw.json.bak.pre-voicefix2-20260227
- openclaw.json.bak.claude-session-20260227-2140
- archive-20260223/openclaw.json.bak.voicecall.20260221-163617
- archive-20260223/voice-call.bak.20260221
- archive-20260223/voice-call-config-backup.json

## NEXT STEPS TO INVESTIGATE (in priority order)
1. Check Twilio call logs via API for disconnect reason codes — WHY is call dropping?
2. Test if wss:// stream URL is reachable from Twilio (may need port 443 via HTTPS)
3. Check if WebSocket stream handler receives any connection at all during a call
4. Test ElevenLabs API key directly (curl to elevenlabs API)
5. Try simplest possible TwiML first: just a Say verb, no streaming — does THAT work?
6. If Say works, then the issue is in the streaming/WebSocket path
7. If Say does NOT work, the issue is in Tailscale funnel or Twilio webhook delivery

## CRASH PREVENTION NOTES FOR CLAUDE
- Do NOT cat full config files — use python3 to extract specific keys
- Do NOT grep entire log files — use tail with small line limits
- Keep osascript outputs under 2000 chars
- Write documentation in SEPARATE fresh chats, not during troubleshooting
- Context overflow from large tool reads is the crash cause
- Always save work to this file BEFORE proceeding with new troubleshooting steps
