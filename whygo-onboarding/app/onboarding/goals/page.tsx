'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useOnboarding } from '@/lib/context/OnboardingContext'
import { createGoal } from '@/lib/api/goals'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Loader2, Plus, Trash2 } from 'lucide-react'

interface OutcomeForm {
  description: string
  metric_type: string
  owner_id: string
  target_annual: number
  target_q1: number
  target_q2: number
  target_q3: number
  target_q4: number
}

export default function GoalsPage() {
  const router = useRouter()
  const { data, setCurrentStep } = useOnboarding()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  const [formData, setFormData] = useState({
    parent_goal_ids: [] as string[],
    why: '',
    goal: '',
    outcomes: [
      { description: '', metric_type: 'number', owner_id: '', target_annual: 0, target_q1: 0, target_q2: 0, target_q3: 0, target_q4: 0 },
      { description: '', metric_type: 'number', owner_id: '', target_annual: 0, target_q1: 0, target_q2: 0, target_q3: 0, target_q4: 0 },
    ] as OutcomeForm[],
  })

  useEffect(() => {
    setCurrentStep(4)

    // Redirect if no data
    if (!data) {
      router.push('/onboarding/profile')
      return
    }

    // Pre-fill owner_id with current user
    setFormData(prev => ({
      ...prev,
      outcomes: prev.outcomes.map(o => ({ ...o, owner_id: data.person.id }))
    }))
  }, [data, router])

  if (!data) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsSubmitting(true)

    try {
      await createGoal(formData)
      router.push('/onboarding/complete')
    } catch (err: any) {
      setError(err.message || 'Failed to create goal')
    } finally {
      setIsSubmitting(false)
    }
  }

  const addOutcome = () => {
    if (formData.outcomes.length < 3) {
      setFormData(prev => ({
        ...prev,
        outcomes: [...prev.outcomes, {
          description: '',
          metric_type: 'number',
          owner_id: data.person.id,
          target_annual: 0,
          target_q1: 0,
          target_q2: 0,
          target_q3: 0,
          target_q4: 0
        }]
      }))
    }
  }

  const removeOutcome = (idx: number) => {
    if (formData.outcomes.length > 2) {
      setFormData(prev => ({
        ...prev,
        outcomes: prev.outcomes.filter((_, i) => i !== idx)
      }))
    }
  }

  const updateOutcome = (idx: number, field: keyof OutcomeForm, value: string | number) => {
    const newOutcomes = [...formData.outcomes]
    newOutcomes[idx] = { ...newOutcomes[idx], [field]: value }
    setFormData(prev => ({ ...prev, outcomes: newOutcomes }))
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Create Your Individual Goal</h2>
        <p className="mt-2 text-gray-600">
          {data.person.level === 'department_head'
            ? "As a department head, you can set both department and individual goals. Let's start with one personal goal."
            : "Set your first individual goal for 2026. Remember: maximum 3 goals total."}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Goal Alignment</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="parent">Connect to Department Goal *</Label>
              <Select
                value={formData.parent_goal_ids[0] || ''}
                onValueChange={(val) => setFormData(prev => ({ ...prev, parent_goal_ids: [val] }))}
                required
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select department goal..." />
                </SelectTrigger>
                <SelectContent>
                  {data.department_goals.map((dg, idx) => (
                    <SelectItem key={dg.id} value={dg.id}>
                      Dept Goal #{idx + 1}: {dg.goal.substring(0, 60)}...
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-xs text-gray-500 mt-1">Your goal must ladder up to a department goal</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>WHY & GOAL</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="why">WHY (Strategic importance) *</Label>
              <Textarea
                id="why"
                placeholder="Why does this goal matter to Kartel? (Max 500 characters)"
                value={formData.why}
                onChange={(e) => setFormData(prev => ({ ...prev, why: e.target.value }))}
                maxLength={500}
                rows={3}
                required
              />
              <p className="text-xs text-gray-500 mt-1">{formData.why.length}/500 characters</p>
            </div>

            <div>
              <Label htmlFor="goal">GOAL (What will be achieved) *</Label>
              <Textarea
                id="goal"
                placeholder="Clear, specific objective (Max 300 characters)"
                value={formData.goal}
                onChange={(e) => setFormData(prev => ({ ...prev, goal: e.target.value }))}
                maxLength={300}
                rows={2}
                required
              />
              <p className="text-xs text-gray-500 mt-1">{formData.goal.length}/300 characters</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>OUTCOMES (2-3 required)</CardTitle>
              {formData.outcomes.length < 3 && (
                <Button type="button" variant="outline" size="sm" onClick={addOutcome}>
                  <Plus className="w-4 h-4 mr-1" />
                  Add Outcome
                </Button>
              )}
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {formData.outcomes.map((outcome, idx) => (
              <div key={idx} className="border rounded-lg p-4 space-y-4">
                <div className="flex items-center justify-between">
                  <h4 className="font-semibold">Outcome {idx + 1}</h4>
                  {formData.outcomes.length > 2 && (
                    <Button type="button" variant="ghost" size="sm" onClick={() => removeOutcome(idx)}>
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  )}
                </div>

                <div>
                  <Label>Description *</Label>
                  <Input
                    placeholder="What will you measure?"
                    value={outcome.description}
                    onChange={(e) => updateOutcome(idx, 'description', e.target.value)}
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label>Metric Type *</Label>
                    <Select
                      value={outcome.metric_type}
                      onValueChange={(val) => updateOutcome(idx, 'metric_type', val)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="number">Number</SelectItem>
                        <SelectItem value="percentage">Percentage</SelectItem>
                        <SelectItem value="currency">Currency</SelectItem>
                        <SelectItem value="boolean">Yes/No</SelectItem>
                        <SelectItem value="milestone">Milestone</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label>Annual Target *</Label>
                    <Input
                      type="number"
                      placeholder="e.g., 100"
                      value={outcome.target_annual || ''}
                      onChange={(e) => updateOutcome(idx, 'target_annual', parseFloat(e.target.value))}
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-4 gap-2">
                  <div>
                    <Label className="text-xs">Q1 Target</Label>
                    <Input
                      type="number"
                      placeholder="Q1"
                      value={outcome.target_q1 || ''}
                      onChange={(e) => updateOutcome(idx, 'target_q1', parseFloat(e.target.value) || 0)}
                    />
                  </div>
                  <div>
                    <Label className="text-xs">Q2 Target</Label>
                    <Input
                      type="number"
                      placeholder="Q2"
                      value={outcome.target_q2 || ''}
                      onChange={(e) => updateOutcome(idx, 'target_q2', parseFloat(e.target.value) || 0)}
                    />
                  </div>
                  <div>
                    <Label className="text-xs">Q3 Target</Label>
                    <Input
                      type="number"
                      placeholder="Q3"
                      value={outcome.target_q3 || ''}
                      onChange={(e) => updateOutcome(idx, 'target_q3', parseFloat(e.target.value) || 0)}
                    />
                  </div>
                  <div>
                    <Label className="text-xs">Q4 Target</Label>
                    <Input
                      type="number"
                      placeholder="Q4"
                      value={outcome.target_q4 || ''}
                      onChange={(e) => updateOutcome(idx, 'target_q4', parseFloat(e.target.value) || 0)}
                    />
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded p-4">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        <div className="flex justify-between pt-6">
          <Button type="button" variant="outline" onClick={() => router.back()}>
            Back
          </Button>
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Creating Goal...
              </>
            ) : (
              'Create Goal & Complete'
            )}
          </Button>
        </div>
      </form>
    </div>
  )
}
