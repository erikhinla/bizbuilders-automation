import { useState } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { CheckCircle, ChevronRight, ArrowLeft } from 'lucide-react'

const LAYERS = [
  {
    id: 'context',
    label: 'Context Layer',
    subtitle: 'Source of truth and decision framework',
    questions: [
      {
        id: 'source_of_truth',
        text: 'Do you have one place where your business logic, offer structure, and positioning are documented and consistently referenced?',
        options: [
          { value: 'documented_current', label: 'Yes — documented, current, and used' },
          { value: 'exists_outdated', label: 'Partially — exists but outdated or inconsistently used' },
          { value: 'in_my_head', label: 'No — lives in my head or scattered notes' },
          { value: 'not_built', label: 'No — not built yet' },
        ]
      },
      {
        id: 'terminology_consistency',
        text: 'When you or your team describe what you do, is the language consistent across channels?',
        options: [
          { value: 'consistent', label: 'Yes — consistent across all surfaces' },
          { value: 'mostly', label: 'Mostly — minor inconsistencies' },
          { value: 'inconsistent', label: 'No — shifts depending on who is communicating' },
        ]
      },
      {
        id: 'decision_framework',
        text: 'When a new opportunity or problem arises, do you have a defined framework for deciding what to pursue?',
        options: [
          { value: 'documented', label: 'Yes — documented decision process' },
          { value: 'informal', label: 'Informally — mental rules but nothing written' },
          { value: 'none', label: 'No — decisions happen case by case' },
        ]
      }
    ]
  },
  {
    id: 'system',
    label: 'System Architecture Layer',
    subtitle: 'Workflows, execution paths, and tooling',
    questions: [
      {
        id: 'workflow_documentation',
        text: 'Are your core business workflows documented and repeatable?',
        options: [
          { value: 'documented_followed', label: 'Yes — documented, followed, and updated' },
          { value: 'partially', label: 'Partially — some documented, others not' },
          { value: 'not_written', label: 'No — exist in practice but not written down' },
          { value: 'inconsistent', label: 'No — inconsistent or underdefined' },
        ]
      },
      {
        id: 'execution_paths',
        text: 'When a client moves through your system, is the path from first contact to delivered outcome clearly defined?',
        options: [
          { value: 'fully_defined', label: 'Yes — every step is defined and owned' },
          { value: 'gaps_exist', label: 'Partially — path exists but has gaps' },
          { value: 'unclear', label: 'No — unclear or varies significantly' },
        ]
      },
      {
        id: 'automation_coverage',
        text: 'What percentage of your repeatable operational tasks are automated?',
        options: [
          { value: 'above_60', label: 'More than 60%' },
          { value: '30_to_60', label: '30 to 60%' },
          { value: 'below_30', label: 'Less than 30%' },
          { value: 'none', label: 'Essentially none' },
        ]
      }
    ]
  },
  {
    id: 'activation',
    label: 'Activation Layer',
    subtitle: 'Lead capture, follow-up, and outreach systems',
    questions: [
      {
        id: 'lead_capture',
        text: 'Do you have a defined and functioning system for capturing leads?',
        options: [
          { value: 'functional', label: 'Yes — functional, tested, producing leads' },
          { value: 'partial', label: 'Partially — exists but not consistently used' },
          { value: 'none', label: 'No — leads come in ad hoc' },
        ]
      },
      {
        id: 'follow_up',
        text: 'Is your follow-up process documented and executed consistently?',
        options: [
          { value: 'consistent', label: 'Yes — automated or consistently manual' },
          { value: 'partial', label: 'Partially — varies by rep or situation' },
          { value: 'reactive', label: 'No — reactive and inconsistent' },
        ]
      },
      {
        id: 'content_system',
        text: 'Do you have a defined system for producing and distributing content or outreach?',
        options: [
          { value: 'defined_system', label: 'Yes — calendar, workflow, and distribution exist' },
          { value: 'partial', label: 'Partially — content produced without a consistent system' },
          { value: 'none', label: 'No — happens when time allows' },
        ]
      }
    ]
  },
  {
    id: 'interface',
    label: 'Interface Layer',
    subtitle: 'Client-facing accuracy and intake experience',
    questions: [
      {
        id: 'client_facing_accuracy',
        text: 'Does your website, onboarding, and sales materials accurately reflect how your system actually works?',
        options: [
          { value: 'aligned', label: 'Yes — fully aligned' },
          { value: 'mostly', label: 'Mostly — minor gaps' },
          { value: 'significant_gaps', label: 'No — significant gaps between promise and delivery' },
        ]
      },
      {
        id: 'intake_experience',
        text: 'When a new client enters your system, is the experience consistent and governed by a defined process?',
        options: [
          { value: 'consistent', label: 'Yes — consistent, documented, and tested' },
          { value: 'partial', label: 'Partially — a process exists but varies' },
          { value: 'ad_hoc', label: 'No — handled ad hoc' },
        ]
      }
    ]
  }
]

const GAP_VALUES = {
  source_of_truth: ['in_my_head', 'not_built'],
  terminology_consistency: ['inconsistent'],
  decision_framework: ['none'],
  workflow_documentation: ['not_written', 'inconsistent'],
  execution_paths: ['unclear'],
  automation_coverage: ['below_30', 'none'],
  lead_capture: ['none'],
  follow_up: ['reactive'],
  content_system: ['none'],
  client_facing_accuracy: ['significant_gaps'],
  intake_experience: ['ad_hoc'],
}

function computeGaps(answers) {
  const layerGaps = {}
  LAYERS.forEach(layer => {
    const gaps = layer.questions.filter(q => {
      const val = answers[q.id]
      return val && GAP_VALUES[q.id]?.includes(val)
    })
    layerGaps[layer.id] = gaps.length
  })
  return layerGaps
}

function getRouting(gapCount) {
  if (gapCount >= 3) return { label: 'Full engagement', description: 'Gaps detected across multiple layers. A scoping conversation will map the right starting point.' }
  if (gapCount === 2) return { label: 'Infrastructure conversation', description: 'Two layers need attention. We will address them in canonical sequence.' }
  if (gapCount === 1) return { label: 'Targeted resource', description: 'One layer needs work. We will send you the relevant playbook or next step.' }
  return { label: 'Stable system', description: 'No major gaps detected. We will confirm your baseline and offer a check-in.' }
}

export function Intake() {
  const [step, setStep] = useState('intro') // intro | questions | contact | submitted
  const [currentLayer, setCurrentLayer] = useState(0)
  const [answers, setAnswers] = useState({})
  const [friction, setFriction] = useState('')
  const [stalling, setStalling] = useState('')
  const [contact, setContact] = useState({ name: '', email: '', company: '' })
  const [submitting, setSubmitting] = useState(false)

  const currentLayerData = LAYERS[currentLayer]
  const allQuestionsAnswered = currentLayerData?.questions.every(q => answers[q.id])
  const totalLayers = LAYERS.length

  function selectAnswer(questionId, value) {
    setAnswers(prev => ({ ...prev, [questionId]: value }))
  }

  function nextLayer() {
    if (currentLayer < totalLayers - 1) {
      setCurrentLayer(prev => prev + 1)
      window.scrollTo({ top: 0, behavior: 'smooth' })
    } else {
      setStep('contact')
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }

  function prevLayer() {
    if (currentLayer > 0) {
      setCurrentLayer(prev => prev - 1)
      window.scrollTo({ top: 0, behavior: 'smooth' })
    } else {
      setStep('intro')
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSubmitting(true)

    const gaps = computeGaps(answers)
    const totalGaps = Object.values(gaps).filter(v => v > 0).length
    const routing = getRouting(totalGaps)

    const payload = {
      ...contact,
      answers,
      friction,
      stalling,
      gaps,
      routing: routing.label,
      source: 'bizbuilders.ai/intake',
      submitted_at: new Date().toISOString(),
    }

    // Submit to webhook
    try {
      const webhookResp = await fetch('https://intake.srv1413136.hstgr.cloud/intake', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      if (!webhookResp.ok) throw new Error('webhook failed')
      setStep('submitted')
      setSubmitting(false)
      return
    } catch (_) {
      // Fallback to mailto
    }

    // Mailto fallback
    const subject = encodeURIComponent(`Context Architecture Assessment — ${contact.name}`)
    const body = encodeURIComponent(
      `Name: ${contact.name}\nEmail: ${contact.email}\nCompany: ${contact.company}\n\n` +
      `Gaps by layer:\n${Object.entries(gaps).map(([k, v]) => `  ${k}: ${v} gap(s)`).join('\n')}\n\n` +
      `Routing: ${routing.label}\n\n` +
      `Biggest friction: ${friction}\nWhat is stalling: ${stalling}`
    )
    window.open(`mailto:erik@bizbuilders.ai?subject=${subject}&body=${body}`, '_self')

    setStep('submitted')
    setSubmitting(false)
  }

  const progress = step === 'questions' ? ((currentLayer) / totalLayers) * 100 : step === 'contact' ? 100 : 0

  return (
    <div className="min-h-screen bg-[#0A0E27] text-white">
      {/* Header */}
      <div className="border-b border-white/10 px-6 py-4 flex items-center justify-between">
        <a href="/" className="flex items-center gap-2 text-[#00D9FF] hover:opacity-80 transition-opacity text-sm">
          <ArrowLeft size={16} />
          BizBuilders
        </a>
        {step === 'questions' && (
          <div className="flex items-center gap-3">
            <div className="w-48 h-1 bg-white/10 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-[#00D9FF] rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${((currentLayer + 1) / totalLayers) * 100}%` }}
                transition={{ duration: 0.4 }}
              />
            </div>
            <span className="text-xs text-white/40">{currentLayer + 1} of {totalLayers}</span>
          </div>
        )}
      </div>

      <div className="max-w-2xl mx-auto px-6 py-12">

        {/* Intro */}
        {step === 'intro' && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <div className="text-xs font-mono text-[#00D9FF] mb-4 tracking-widest uppercase">Context Architecture Assessment</div>
            <h1 className="text-3xl font-semibold mb-4 leading-snug">Map where digital friction is blocking momentum.</h1>
            <p className="text-white/60 mb-8 leading-relaxed">
              This is not a quiz and there is no score. It produces a baseline — an honest picture of
              where your current state is stable and where it is not. Completion takes 10 to 15 minutes.
              You will receive observations, not a sales call.
            </p>
            <div className="grid gap-3 mb-10">
              {LAYERS.map((layer, i) => (
                <div key={layer.id} className="flex items-center gap-3 text-sm text-white/50">
                  <span className="w-6 h-6 rounded-full border border-white/20 flex items-center justify-center text-xs text-white/30">{i + 1}</span>
                  <span>{layer.label}</span>
                </div>
              ))}
            </div>
            <Button
              onClick={() => setStep('questions')}
              className="bg-[#00D9FF] text-[#0A0E27] hover:bg-[#00D9FF]/90 font-medium px-8"
            >
              Begin Assessment <ChevronRight size={16} className="ml-1" />
            </Button>
          </motion.div>
        )}

        {/* Questions */}
        {step === 'questions' && (
          <motion.div key={currentLayer} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.3 }}>
            <div className="text-xs font-mono text-[#00D9FF] mb-1 tracking-widest uppercase">{currentLayerData.label}</div>
            <p className="text-white/40 text-sm mb-8">{currentLayerData.subtitle}</p>

            <div className="space-y-8">
              {currentLayerData.questions.map((question, qi) => (
                <div key={question.id}>
                  <p className="text-sm text-white/80 mb-3 leading-relaxed">{question.text}</p>
                  <div className="space-y-2">
                    {question.options.map(option => {
                      const selected = answers[question.id] === option.value
                      return (
                        <button
                          key={option.value}
                          onClick={() => selectAnswer(question.id, option.value)}
                          className={`w-full text-left px-4 py-3 rounded-lg border text-sm transition-all ${
                            selected
                              ? 'border-[#00D9FF] bg-[#00D9FF]/10 text-white'
                              : 'border-white/10 bg-white/5 text-white/60 hover:border-white/30 hover:text-white/80'
                          }`}
                        >
                          <span className={`inline-block w-3 h-3 rounded-full border mr-3 transition-all ${selected ? 'bg-[#00D9FF] border-[#00D9FF]' : 'border-white/30'}`} />
                          {option.label}
                        </button>
                      )
                    })}
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-between mt-10">
              <Button variant="ghost" onClick={prevLayer} className="text-white/40 hover:text-white/70">
                <ArrowLeft size={16} className="mr-1" /> Back
              </Button>
              <Button
                onClick={nextLayer}
                disabled={!allQuestionsAnswered}
                className="bg-[#00D9FF] text-[#0A0E27] hover:bg-[#00D9FF]/90 font-medium disabled:opacity-30"
              >
                {currentLayer < totalLayers - 1 ? 'Next' : 'Continue'} <ChevronRight size={16} className="ml-1" />
              </Button>
            </div>
          </motion.div>
        )}

        {/* Contact + Context */}
        {step === 'contact' && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
            <div className="text-xs font-mono text-[#00D9FF] mb-1 tracking-widest uppercase">Operational Context</div>
            <p className="text-white/40 text-sm mb-8">Two questions and your contact details.</p>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="text-sm text-white/60 block mb-2">Biggest operational friction right now</label>
                <textarea
                  value={friction}
                  onChange={e => setFriction(e.target.value)}
                  required
                  rows={3}
                  placeholder="In plain language — 2 to 4 sentences."
                  className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-sm text-white placeholder-white/20 focus:outline-none focus:border-[#00D9FF]/50 resize-none"
                />
              </div>
              <div>
                <label className="text-sm text-white/60 block mb-2">What is stalling</label>
                <textarea
                  value={stalling}
                  onChange={e => setStalling(e.target.value)}
                  required
                  rows={2}
                  placeholder="The one thing that, if resolved, would most change how your business operates."
                  className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-sm text-white placeholder-white/20 focus:outline-none focus:border-[#00D9FF]/50 resize-none"
                />
              </div>

              <div className="pt-2 border-t border-white/10 space-y-4">
                <p className="text-xs text-white/30">Where should we send your baseline?</p>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm text-white/60 block mb-2">Name</label>
                    <input
                      value={contact.name}
                      onChange={e => setContact(p => ({ ...p, name: e.target.value }))}
                      required
                      className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-sm text-white placeholder-white/20 focus:outline-none focus:border-[#00D9FF]/50"
                    />
                  </div>
                  <div>
                    <label className="text-sm text-white/60 block mb-2">Email</label>
                    <input
                      type="email"
                      value={contact.email}
                      onChange={e => setContact(p => ({ ...p, email: e.target.value }))}
                      required
                      className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-sm text-white placeholder-white/20 focus:outline-none focus:border-[#00D9FF]/50"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-sm text-white/60 block mb-2">Company (optional)</label>
                  <input
                    value={contact.company}
                    onChange={e => setContact(p => ({ ...p, company: e.target.value }))}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-sm text-white placeholder-white/20 focus:outline-none focus:border-[#00D9FF]/50"
                  />
                </div>
              </div>

              <div className="flex justify-between pt-2">
                <Button type="button" variant="ghost" onClick={() => { setStep('questions'); setCurrentLayer(totalLayers - 1) }} className="text-white/40 hover:text-white/70">
                  <ArrowLeft size={16} className="mr-1" /> Back
                </Button>
                <Button
                  type="submit"
                  disabled={submitting}
                  className="bg-[#00D9FF] text-[#0A0E27] hover:bg-[#00D9FF]/90 font-medium px-8 disabled:opacity-50"
                >
                  {submitting ? 'Submitting...' : 'Submit Assessment'}
                </Button>
              </div>
            </form>
          </motion.div>
        )}

        {/* Submitted */}
        {step === 'submitted' && (
          <motion.div initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.5 }} className="text-center">
            <CheckCircle size={48} className="text-[#00D9FF] mx-auto mb-6" />
            <h2 className="text-2xl font-semibold mb-3">Assessment submitted.</h2>
            <p className="text-white/50 mb-8 max-w-md mx-auto">
              Your baseline has been recorded. We will review it and reach out with observations within one business day.
              Not a sales call.
            </p>
            <a href="/" className="text-[#00D9FF] text-sm hover:opacity-80 transition-opacity">
              Return to BizBuilders
            </a>
          </motion.div>
        )}
      </div>
    </div>
  )
}
