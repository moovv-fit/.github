# 👋 Welcome to Moovv

<p align="center">
  <a href="https://www.moovv.fit"><img src="https://img.shields.io/badge/Website-moovv.fit-blue?style=for-the-badge" alt="Website"/></a>
  <a href="https://play.google.com/store/apps/details?id=fit.moovv.app"><img src="https://img.shields.io/badge/Google_Play-Download-green?style=for-the-badge&logo=google-play" alt="Google Play"/></a>
</p>

<p align="center">
  <strong>AI-Powered Mobility Coaching & Pain Relief — Designed by Physiotherapists</strong>
</p>

---

## 🎯 What is Moovv?

**Moovv Fit** is an AI-driven healthtech platform democratizing physical therapy through personalized, accessible MSK (musculoskeletal) solutions.

We're solving real problems:
- 🏥 **Abandoned rehab** — Patients drop exercises post-clinic because plans are scribbled on paper
- 📺 **Generic content** — YouTube videos lack personalization for your specific injury
- 📊 **No pain tracking** — No continuous, longitudinal pain-level monitoring exists
- 💰 **Cost barrier** — In-person follow-ups cost ₹1,000–₹2,000 per session

### Our Approach
- **AI recommends, physios approve** — Human-in-the-Loop verification for clinical safety
- **Real clinician videos** — 300+ exercises recorded by certified physiotherapists (never AI avatars)
- **Pain management, not painkillers** — We help bring pain from 9/10 to 3/10 over time through movement

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **AI-Powered Plans** | Personalized mobility routines that adapt to your progress |
| **Physio-Verified** | Every exercise vetted by certified MSK specialists (48h SLA) |
| **OPQRST Pain Framework** | Clinical-grade pain assessment (Onset, Provocation, Quality, Region, Severity, Timing) |
| **Daily Micro-Workouts** | 10-15 minute sessions that fit your schedule |
| **Progress Tracking** | Monitor improvements in flexibility and pain levels |
| **Tele-Rehab Sessions** | 45-min video consultations with verified physios |

---

## 👥 Who Uses Moovv?

| Segment | Use Case |
|---------|----------|
| 💼 **Desk Workers** | Back and neck stiffness from sedentary work |
| 🎾 **Athletes** | Sport-specific mobility (tennis elbow, runner's knee) |
| 🦴 **Recovery Patients** | Post-rehab continuation and adherence |
| 👴 **Seniors** | Maintaining movement and independence |
| 🏥 **Clinics** | Digital HEP (Home Exercise Programs) for patients |

---

## 🏗️ Platform Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Moovv Platform                         │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Mobile Apps   │    Web Portal   │      Partner SDK        │
│  (iOS/Android)  │  (Patient/Clinic)│   (B2B Integrations)   │
├─────────────────┴─────────────────┴─────────────────────────┤
│                    Core API (Node.js/TypeScript)            │
├─────────────────────────────────────────────────────────────┤
│  AI Recommendation   │  Clinical Verification  │  Billing   │
│       Engine         │      (HITL Gate)        │   Engine   │
├─────────────────────────────────────────────────────────────┤
│                   AWS Infrastructure (CDK)                  │
│            Lambda • Aurora • S3 • CloudFront                │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Mobile** | Flutter |
| **Backend** | Node.js, TypeScript, Fastify |
| **Database** | Prisma, PostgreSQL (Aurora) |
| **Infrastructure** | AWS CDK, Lambda, S3, CloudFront |
| **Video** | Agora RTC (Telehealth) |
| **AI/ML** | ONNX embeddings, semantic scoring |

---

## 🗺️ Roadmap: From MSK Care to Physical AI

### Phase 1: Clinical Data Moat (Current)
- Mobile apps on App Store & Google Play
- WhatsApp-first clinic handoffs
- 20-exercise mobility self-test catalog

### Phase 2: Biomechanical Digital Twins
- On-device pose estimation (MediaPipe)
- Real-time biofeedback during exercises
- Autonomous AI Physio (Human-on-the-Loop)

### Phase 3: Physical AI & Robotics
- Movement intent prediction for assistive exoskeletons
- Sim-to-real dataset licensing for robotics labs
- Impedance control for humanoid care robots

---

## 👨‍💼 Founders

| Name | Role | Focus |
|------|------|-------|
| **Rahul Jain** | Growth & Partnerships | GTM, Sales |
| **Ujwal Parker** | Fractional CTO | Technical Architecture |
| **Pawan Deshmukh** | Product & Clinical | Product, ISB MBA |

---

## 📱 Get the App

<p align="center">
  <a href="https://play.google.com/store/apps/details?id=fit.moovv.app">
    <img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg" alt="Get it on Google Play" height="60"/>
  </a>
</p>

**7-day free trial** → ₹200/month

---

## 📬 Contact

- **Website:** [moovv.fit](https://www.moovv.fit)
- **Email:** [hello@moovv.fit](mailto:hello@moovv.fit)

---

<p align="center">
  <sub>Built with ❤️ for better movement</sub>
</p>
