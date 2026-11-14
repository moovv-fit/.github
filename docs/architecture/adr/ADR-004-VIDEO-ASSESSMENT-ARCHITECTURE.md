# ADR-004: Video Assessment Architecture

**Status**: ✅ Current  
**Date**: 2025-01-20

## Context

Moovv Fit's mobility assessment system originally relied on manual self-tests where users self-report their range of motion through multiple-choice, timed, and counted test formats (see PDR-013). While functional, manual assessments have inherent limitations:

- **Subjectivity**: Users may over- or under-estimate their capabilities
- **Inconsistency**: Test execution varies between sessions
- **Limited data**: No kinematic telemetry for Physical AI training pipeline

The platform's evolution toward Physical AI (PDR-017) requires objective measurement data—specifically, joint angles, range-of-motion (ROM) velocity, and movement patterns captured during assessment execution.

## Decision

Implement video-based mobility assessments using on-device pose estimation with the following architecture:

### 1. Pose Estimation Model

**MediaPipe BlazePose 33-keypoint model** selected for cross-platform pose estimation:

| Consideration | Decision |
|---------------|----------|
| Model | BlazePose Full (33 keypoints) |
| Execution | On-device (Flutter via `google_mlkit_pose_detection`) |
| Frame rate | 15-30 FPS depending on device capability |
| Keypoint confidence | Minimum 0.5 threshold for ROM calculation |

BlazePose provides full-body landmark detection including face, hands, and feet keypoints necessary for comprehensive mobility assessment (hip flexion, shoulder rotation, ankle dorsiflexion, etc.).

### 2. Client-Side ROM Calculation with Server Storage

**Privacy-first architecture**: Raw video never leaves the device.

```
┌─────────────────────────────────────────────────────────────┐
│                      MOBILE DEVICE                          │
├─────────────────────────────────────────────────────────────┤
│  Camera → MediaPipe → Keypoint Extraction → ROM Calculation │
│                              │                              │
│                              ▼                              │
│                    Computed Scores Only                     │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND (Lambda)                        │
├─────────────────────────────────────────────────────────────┤
│  Kinematic Session → Frame Storage → Assessment Score       │
│         │                  │                 │              │
│         ▼                  ▼                 ▼              │
│  user_kinematic_   kinematic_    user_video_assessment_     │
│     sessions         frames           scores                │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
                    S3 Parquet Export (Physical AI)
```

### 3. Graceful Degradation Strategy

When camera access is unavailable, the system falls back to manual self-tests:

| Scenario | Behavior |
|----------|----------|
| Camera permission denied | Automatic fallback to manual UI |
| Device lacks camera | Manual-only mode |
| Pose detection fails (lighting, occlusion) | Retry prompt → manual fallback |
| Low confidence keypoints | Discard frame, continue capture |

The `assessment_type` ENUM (`manual`, `video`, `both`) on the `self_tests` table enables per-test configuration of available assessment modes.

### 4. Frame Batching Approach

Kinematic frame data is batched for efficient transmission and storage:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Batch size | 100 frames | Balance between network efficiency and data freshness |
| Max frames/session | 1000 | ~30-60 seconds of assessment at 15-30 FPS |
| Insert strategy | Bulk insert per batch | Reduce database round-trips |

### 5. Database Schema

Three new tables support video assessments:

```sql
-- Session container for kinematic capture
user_kinematic_sessions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  self_test_id UUID REFERENCES self_tests(id),
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  device_info JSONB
)

-- Raw keypoint frames (33 landmarks × 3 coordinates per frame)
kinematic_frames (
  id UUID PRIMARY KEY,
  session_id UUID REFERENCES user_kinematic_sessions(id),
  frame_index INT,
  timestamp_ms BIGINT,
  keypoints JSONB,  -- [{landmark_type, x, y, z, confidence}, ...]
  created_at TIMESTAMPTZ
)

-- Computed assessment results
user_video_assessment_scores (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  self_test_id UUID REFERENCES self_tests(id),
  session_id UUID REFERENCES user_kinematic_sessions(id),
  score DECIMAL,
  rom_measurements JSONB,  -- {peak_angle, velocity, symmetry}
  created_at TIMESTAMPTZ
)
```

### 6. API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/mobility/kinematic-session` | POST | Create session, batch insert frames |
| `/api/mobility/video-assessment-result` | POST | Submit computed ROM scores |

## Consequences

### Positive

- **Objective measurements**: ROM angles calculated from actual joint positions, not self-reported
- **Physical AI data pipeline**: Kinematic telemetry populates training datasets for future AI models
- **Privacy preserved**: No video storage; only computed coordinates and scores
- **Graceful fallback**: Users without camera access retain full functionality via manual tests
- **Extensibility**: `assessment_type` ENUM allows gradual rollout of video assessments per test

### Negative

- **Device requirements**: Requires devices with adequate camera and processing capability
- **Environmental sensitivity**: Poor lighting or occlusion can degrade pose estimation quality
- **Storage growth**: Kinematic frames add significant data volume (mitigated by S3 archival)
- **Complexity**: Two assessment paths (video/manual) require UI state management

### Mitigations

| Risk | Mitigation |
|------|------------|
| Pose estimation failures | Confidence thresholds + retry UX + manual fallback |
| Storage costs | S3 lifecycle policies for frame archival |
| Device compatibility | Minimum device spec documentation; graceful degradation |

## References

- `#[[file:../../../repos/docs/product/docs/product/pdr/clinical-exercise-engine/PDR-013-SELF-TEST-MOBILITY-CATALOG-AND-DUAL-FRAMING.md]]` — Self-test catalog and dual framing
- `#[[file:../../../repos/docs/product/docs/product/pdr/clinical-exercise-engine/PDR-017-PHYSICAL-AI-AGENT-ARCHITECTURE.md]]` — Physical AI agent architecture
- [MediaPipe Pose Documentation](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker)
- Backend PR #79: Kinematic telemetry API implementation
- Mobile PR #11: MediaPipe pose estimation integration
