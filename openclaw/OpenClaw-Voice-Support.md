# OpenClaw Voice Support — Nash (NY Library Mac Studio)

## Last Updated: 2026-02-28 12:15 AM EST

## STATUS: NOT WORKING — Calls hang up immediately

## Problem Statement
Nash (OpenClaw on NY Library Mac Studio) should be able to:
1. RECEIVE calls from Bill at +12392274662 on Twilio number +18553933306
2. MAKE calls from +18553933306 to Bill at +12392274662
3. Use ElevenLabs TTS for Nash voice (voice ID CwhRBWXzGAHq8TQ4Fs17, model eleven_turbo_v2_5)

**Current behavior**: When Bill calls 855-393-3306, the call is answered then immediately hangs up. This has persisted for DAYS across multiple troubleshooting sessions (Feb 21, 23, 27, 28).

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
- Twilio Account SID: [REDACTED — starts with ACa7d6]
- Twilio Auth Token: [REDACTED_SECRET] (in gateway env and twilio_setup.json)
- ElevenLabs API Key: [REDACTED_SECRET] (in gateway env, starts with sk_1410)
- ElevenLabs Voice ID: CwhRBWXzGAHq8TQ4Fs17
- ElevenLabs Model: eleven_turbo_v2_5

## Key Config Files
- `~/.openclaw/openclaw.json` — Main config
- `~/.openclaw/settings/tts.json` — TTS settings (WAS BROKEN, NOW FIXED)
- `~/.openclaw/settings/voicewake.json` — Wake word triggers
- `~/.openclaw/workspace/config/twilio_setup.json` — Twilio setup notes
- `~/Library/LaunchAgents/ai.openclaw.gateway.plist` — Gateway service
- Gateway binary: `~/.openclaw/tools/node-v22.22.0/bin/node`
- Gateway entry: `~/.openclaw/lib/node_modules/openclaw/dist/entry.js`

## Log Files (CHECK THESE FIRST)
- `~/.openclaw/logs/gateway.err.log` — Check this FIRST for errors
- `~/.openclaw/logs/gateway.log` — Main gateway log
- `~/.openclaw/health-monitor.log` — Health monitor

## Voice-Call Plugin Config (as of 2026-02-28)
Located at: `plugins.entries.voice-call.config` in openclaw.json

```
enabled: true
provider: twilio
fromNumber: +18553933306
toNumber: +12392274662
twilio.accountSid: [REDACTED — starts with ACa7d6]
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
```

**IMPORTANT**: The voice-call config must NOT contain `tts` or `serve` keys. These cause schema validation errors that block ALL config reloads.

Valid keys for voice-call config: enabled, provider, fromNumber, toNumber, twilio, tailscale, outbound, inboundPolicy, allowFrom, inboundGreeting, streaming, maxDurationSeconds, publicUrl, skipSignatureVerification

## TTS Config (messages.tts in openclaw.json)
Correct schema (verified against OpenClaw docs at https://docs.openclaw.ai/tts):
```json
{
  "auto": "always",
  "provider": "elevenlabs",
  "elevenlabs": {
    "voiceId": "CwhRBWXzGAHq8TQ4Fs17",
    "modelId": "eleven_turbo_v2_5"
  }
}
```
Note: voiceId and modelId MUST be nested under `elevenlabs` sub-object, NOT at the tts root level.

## TTS Settings File (~/.openclaw/settings/tts.json)
Correct schema (FIXED on 2026-02-27 at 9:40 PM):
```json
{
  "tts": {
    "auto": "always",
    "provider": "elevenlabs",
    "elevenlabs": {
      "voiceId": "CwhRBWXzGAHq8TQ4Fs17",
      "modelId": "eleven_turbo_v2_5"
    }
  }
}
```
**CRITICAL**: The old broken format had voiceId/modelId at the tts root level (NOT under elevenlabs). This caused `must NOT have additional properties` errors 800+ times and blocked ALL config reloads.

## Twilio Phone Number Config (verified via API 2026-02-27)
- Phone: +18553933306
- Voice URL: https://ny-library-mac-studio.tail3f7308.ts.net/voice/webhook
- Voice Method: POST
- Status Callback: https://ny-library-mac-studio.tail3f7308.ts.net/voice/webhook
- SID: PN672a9deb5a7bc4f5e639ccb995dff073

## Tailscale Funnel Config (verified)
- / -> proxy http://127.0.0.1:18800
- /readai -> proxy http://127.0.0.1:8891
- /voice/webhook -> proxy http://127.0.0.1:3334/voice/webhook
- /voice/stream -> proxy http://127.0.0.1:3334

## Webhook Response (verified via curl 2026-02-27)
Both local (127.0.0.1:3334) and Tailscale funnel URLs return:
```xml
<Response>
  <Connect>
    <Stream url="wss://ny-library-mac-studio.tail3f7308.ts.net/voice/stream">
      <Parameter name="token" value="[generated-token]" />
    </Stream>
  </Connect>
</Response>
```

## What Has Been Verified Working (as of 2026-02-28 ~12:00 AM)
1. Gateway starts and runs on port 18800
2. Voice webhook port 3334 is listening
3. Local curl to webhook returns TwiML with Connect and Stream
4. Tailscale funnel curl to webhook returns same TwiML
5. Twilio phone number points to correct webhook URL
6. Voice-call plugin initializes: TTS configured, media stream wired, runtime initialized
7. Inbound call from +12392274662 is accepted (in allowlist)
8. Call record is created in logs
9. TTS schema errors are GONE (fixed tts.json)
10. Gateway error log is clean after restart (only expected skipSignatureVerification warning)

## What Is NOT Working
1. **Call hangs up immediately after answering** — Despite webhook returning valid TwiML
2. The TwiML response is a `<Connect><Stream>` (WebSocket media stream), NOT a `<Say>` greeting
3. The `inboundGreeting` config value "Hey Bill, it is Nash..." is NOT being rendered as TwiML `<Say>` or `<Play>` before the Stream
4. Possible: WebSocket stream connection from Twilio -> wss:// fails silently, causing Twilio to drop the call
5. Possible: ElevenLabs TTS generation fails before audio can be streamed to the call
6. Possible: The Stream URL (wss://ny-library-mac-studio.tail3f7308.ts.net/voice/stream) is unreachable from Twilio's external servers
7. Possible: Tailscale funnel does NOT support WebSocket upgrade for the /voice/stream path

## Troubleshooting History

### Session 2026-02-21
- First Twilio setup attempt
- Created twilio_setup.json with credentials
- Status: pending installation

### Session 2026-02-23
- Major architecture rebuild: migrated from Docker to native + OpenClaw.app
- Gateway port changed from 18789 to 18800
- Multiple backup files created

### Session 2026-02-27 (earlier — Claude crashed ~12 times)
- Installed GitHub CLI, pushed OpenClaw-Context.md to GitHub
- Identified EADDRINUSE port conflicts
- Identified TTS config conflicts between settings files
- Claude crashed repeatedly due to context window overflow from large osascript outputs
- Nash self-identified the voice problem as potential TTS/audio runtime init failure

### Session 2026-02-27 9:35 PM EST
- Found ROOT CAUSE of config reload blocking:
  - `~/.openclaw/settings/tts.json` had WRONG schema
  - voiceId/modelId were at tts root instead of under tts.elevenlabs
  - This caused: `invalid config tts must NOT have additional properties`
  - This error appeared 800+ times in gateway.err.log
  - Config reloads were being SKIPPED due to validation failure
  - All prior fix attempts to openclaw.json were INEFFECTIVE because tts.json was the blocker
- Fixed tts.json schema (moved voiceId/modelId under elevenlabs sub-object)
- Verified openclaw.json voice-call config is clean (no tts or serve keys)
- Verified messages.tts in openclaw.json already had correct nested structure
- Backed up config as: openclaw.json.bak.claude-session-20260227-2140
- Cleared error log (saved as gateway.err.log.pre-fix-backup)
- Restarted gateway via `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`
- Post-restart: ZERO TTS schema errors in log
- All verification tests pass (webhook, funnel, Twilio config, plugin init)
- **BUT: Live call STILL hangs up immediately — the TTS schema fix was necessary but NOT sufficient**

### Session 2026-02-28 ~12:00 AM EST
- Bill confirmed: call STILL hangs up, same as before
- Documented all work to this context file
- The TTS schema fix resolved the config blocking issue but did NOT fix the actual call hang-up

## Prior Fix Attempt Backups
- openclaw.json.bak.pre-voice-fix-20260227
- openclaw.json.bak.pre-voicefix-202602271720
- openclaw.json.bak.pre-voicefix-20260227-2052
- openclaw.json.bak.pre-voicefix2-20260227
- openclaw.json.bak.claude-session-20260227-2140
- archive-20260223/openclaw.json.bak.voicecall.20260221-163617
- archive-20260223/voice-call.bak.20260221
- archive-20260223/voice-call-config-backup.json

## NEXT STEPS TO INVESTIGATE (in priority order)

### Priority 1: Why does Twilio drop the call?
1. **Check Twilio call logs via API** for disconnect reason codes — what does Twilio say happened?
   ```
   curl -u "[TWILIO_SID]:[AUTH_TOKEN]" "https://api.twilio.com/2010-04-01/Accounts/[TWILIO_SID]/Calls.json?To=+18553933306&Status=completed&PageSize=5"
   ```
2. Look for: `disconnect_reason`, `duration`, `status`, `error_code`, `error_message`

### Priority 2: Is the WebSocket stream reachable?
3. **Test if wss:// stream URL is reachable from outside** (not just localhost)
4. Test: `wscat -c wss://ny-library-mac-studio.tail3f7308.ts.net/voice/stream` from an external machine
5. Check if Tailscale funnel supports WebSocket upgrade on the /voice/stream path
6. Check gateway.log during a live call for WebSocket connection attempts

### Priority 3: Simplest possible test
7. **Try simplest possible TwiML first**: just a `<Say>` verb, no streaming — does THAT work?
8. Temporarily replace the webhook response with static TwiML like `<Response><Say>Hello Bill</Say></Response>`
9. If Say works, the issue is in the streaming/WebSocket path
10. If Say does NOT work, the issue is in Tailscale funnel or Twilio webhook delivery

### Priority 4: ElevenLabs connectivity
11. Test ElevenLabs API key directly: `curl -H "xi-api-key: [KEY]" https://api.elevenlabs.io/v1/user`
12. Test TTS generation: POST to /v1/text-to-speech/CwhRBWXzGAHq8TQ4Fs17

### Priority 5: OpenClaw voice-call plugin behavior
13. Check OpenClaw GitHub issues for known voice-call + Twilio streaming bugs
14. Check if newer OpenClaw version fixes voice-call streaming
15. Examine the voice-call skill source at `~/.openclaw/sandboxes/agent-main-0d71ad7a/skills/voice-call/`

## CRASH PREVENTION NOTES FOR CLAUDE
- Do NOT `cat` full config files — use python3 to extract specific keys
- Do NOT `grep` entire log files — use `tail` with small line limits (15-30 max)
- Keep osascript outputs under 2000 chars
- Write documentation in SEPARATE fresh chats, not during troubleshooting
- Context overflow from large tool reads is the crash cause
- Always save work to this file BEFORE proceeding with new troubleshooting steps
- Use `python3 -c` one-liners for JSON extraction, not jq or cat
- When restarting gateway: `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`

## OpenClaw Official TTS Docs
- TTS config reference: https://docs.openclaw.ai/tts
- Voice setup guide: https://www.getopenclaw.ai/help/voice-tts-setup
- Voice mode tutorial: https://www.open-clawai.com/en/tutorials/voice
- GitHub issue (Vapi+ElevenLabs): https://github.com/openclaw/openclaw/issues/13354

## Session Feb 28 2026 — Root Cause Found

### Diagnosis
**Root cause: Tailscale funnel was NOT running during test calls.**

### Evidence
1. Twilio call logs: webhook responded with correct TwiML (Connect/Stream)
2. Twilio error 31920: Stream Connection Declined (WebSocket unreachable)
3. Gateway log: Inbound call accepted but NO WebSocket upgrade during calls
4. WebSocket upgrades only appeared AFTER funnel started in later session

### What Was Verified Working (with funnel running)
- WebSocket upgrade through funnel: 101 SUCCESS
- Data flow through WebSocket: CONFIRMED
- MediaStream start processing: CONFIRMED
- Server correctly processes Twilio start messages

### Funnel Command
tailscale funnel --bg 3334
(Full path: /Applications/Tailscale.app/Contents/MacOS/Tailscale funnel --bg 3334)

### Remaining Risk
- Funnel persistence across reboots - may need launchd service
- Live call test with Bill still needed to confirm end-to-end
