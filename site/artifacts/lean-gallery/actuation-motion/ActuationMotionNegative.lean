import Mathlib.Tactic

/-!
Expected-failure controls for `ActuationMotion.lean`. Each MUTANT is a deliberately
wrong variant of a frozen statement, given the same proof strategy that works for
the correct statement. Lean must reject every MUTANT. The CORRECT twins (same
definitions, correct statement) must compile, so a rejection cannot be blamed on
the setup. This file is self-contained (definitions copied verbatim) so it does not
depend on a compiled `.olean` of the positive file.
-/
namespace ActuationMotionNeg

open Finset BigOperators

noncomputable def momentumStep (m C dt Fint Fext p : ℝ) : ℝ := p + dt * (Fint - (C / m) * p + Fext)
noncomputable def momentumStepHet (mi C dt Fint Fext p : ℝ) : ℝ := p + dt * (Fint - (C / mi) * p + Fext)
noncomputable def fric (ξp ξm v : ℝ) : ℝ := if 0 ≤ v then ξp * v else ξm * v
noncomputable def cycleDisplacement (ξp ξm A : ℝ) : ℝ := A * (ξm - ξp) / (ξp + ξm)

-- CORRECT twin: total momentum with homogeneous mass.
example {N : ℕ} (m C dt : ℝ) (Fint Fext p : Fin N → ℝ) (hint : ∑ i, Fint i = 0) :
    ∑ i, momentumStep m C dt (Fint i) (Fext i) (p i)
      = (1 - dt * (C / m)) * ∑ i, p i + dt * ∑ i, Fext i := by
  unfold momentumStep
  have h1 : ∀ i, p i + dt * (Fint i - C / m * p i + Fext i)
      = (1 - dt * (C / m)) * p i + dt * Fint i + dt * Fext i := by intro i; ring
  simp only [h1, sum_add_distrib, ← mul_sum, hint]
  ring

-- MUTANT-1 (heterogeneous mass): per-node masses, same claim that the total
-- momentum just scales. Same proof strategy; must be rejected.
theorem mutant_heterogeneous_mass {N : ℕ} (mass : Fin N → ℝ) (m C dt : ℝ)
    (Fint Fext p : Fin N → ℝ) (hint : ∑ i, Fint i = 0) :
    ∑ i, momentumStepHet (mass i) C dt (Fint i) (Fext i) (p i)
      = (1 - dt * (C / m)) * ∑ i, p i + dt * ∑ i, Fext i := by
  unfold momentumStepHet
  have h1 : ∀ i, p i + dt * (Fint i - C / mass i * p i + Fext i)
      = (1 - dt * (C / m)) * p i + dt * Fint i + dt * Fext i := by intro i; ring
  simp only [h1, sum_add_distrib, ← mul_sum, hint]
  ring

-- MUTANT-2 (nonzero initial momentum): claim the COM does not move after one
-- step without assuming zero initial momentum.
theorem mutant_no_initial_rest (x0 x1 p0 p1 : Fin 2 → ℝ)
    (hp : ∀ i, p1 i = momentumStep 1 1 (1/2) 0 0 (p0 i))
    (hx : ∀ i, x1 i = x0 i + (1/2) * p1 i / 1) :
    ∑ i, x1 i = ∑ i, x0 i := by
  simp only [Fin.sum_univ_two, hx, hp, momentumStep]
  ring

-- CORRECT twin: cycle displacement for ξp=1, ξm=3, A=1 is 1/2.
example : cycleDisplacement 1 3 1 = 1/2 := by norm_num [cycleDisplacement]

-- MUTANT-3 (factor-2 error in the cycle law): A(ξm−ξp)/(2(ξp+ξm)).
theorem mutant_cycle_factor_two :
    cycleDisplacement 1 3 1 = 1 * (3 - 1) / (2 * (1 + 3)) := by
  norm_num [cycleDisplacement]

-- MUTANT-4 (anisotropy not needed): claim zero cycle displacement for all drags.
theorem mutant_no_anisotropy_needed (ξp ξm A : ℝ) (hp : 0 < ξp) (hm : 0 < ξm) :
    cycleDisplacement ξp ξm A = 0 := by
  unfold cycleDisplacement
  field_simp
  ring

-- CORRECT twin: drag-weighted centroid is unchanged by one step.
example : let ξ : Fin 2 → ℝ := ![1, 3]; let F : Fin 2 → ℝ := ![1, -1]
    ∑ i, ξ i * (0 + 1 * F i / ξ i) = 0 := by
  norm_num [Fin.sum_univ_two]

-- MUTANT-5 (arithmetic centroid fixed under heterogeneous drag).
theorem mutant_arithmetic_centroid : let ξ : Fin 2 → ℝ := ![1, 3]; let F : Fin 2 → ℝ := ![1, -1]
    ∑ i, (0 + 1 * F i / ξ i) = 0 := by
  simp [Fin.sum_univ_two]
  norm_num

-- MUTANT-6 (wrong direction): forward motion iff forward drag exceeds backward drag.
theorem mutant_wrong_direction {ξp ξm A : ℝ} (hp : 0 < ξp) (hm : 0 < ξm) (hA : 0 < A) :
    0 < cycleDisplacement ξp ξm A ↔ ξm < ξp := by
  unfold cycleDisplacement
  have hs : 0 < ξp + ξm := by linarith
  rw [div_pos_iff_of_pos_right hs]
  constructor
  · intro h; nlinarith
  · intro h; nlinarith

-- MUTANT-7 (crawler step without friction anisotropy coefficient): claim the midpoint
-- step is |δ|/2 independent of the drags, at ξp=1, ξm=3, a₁=−1/4, a₂=3/4.
theorem mutant_step_drag_free :
    fric 1 3 (-1/4) + fric 1 3 (3/4) = 0 → ((-1/4 : ℝ) + 3/4) / 2 = |(1:ℝ)| / 2 := by
  intro _
  norm_num

-- CORRECT twin: the mirrored pair balances friction once the drags are EXCHANGED.
example : fric 3 1 (-(3/4)) + fric 3 1 (-(-1/4)) = 0 := by norm_num [fric]

-- MUTANT-8 (mirror without exchanging drags): reflect and relabel the nodes but keep
-- (ξp, ξm) = (1, 3); the balance claim must be rejected.
theorem mutant_mirror_without_swap : fric 1 3 (-(3/4)) + fric 1 3 (-(-1/4)) = 0 := by
  norm_num [fric]

noncomputable def momentumStepRatio (γ dt Fint Fext p : ℝ) : ℝ := p + dt * (Fint - γ * p + Fext)

-- CORRECT twin: with a uniform damping ratio the MASS-WEIGHTED COM is fixed after one step
-- (masses 1 and 2, γ = 1, dt = 1/2, internal force ±1, start at rest).
example : let mass : Fin 2 → ℝ := ![1, 2]; let F : Fin 2 → ℝ := ![1, -1]
    ∑ i, mass i * (0 + (1/2) * momentumStepRatio 1 (1/2) (F i) 0 0 / mass i) = 0 := by
  norm_num [momentumStepRatio, Fin.sum_univ_two]

-- MUTANT-9 (unweighted COM claimed fixed under heterogeneous mass, same instance).
theorem mutant_unweighted_com_ratio : let mass : Fin 2 → ℝ := ![1, 2]; let F : Fin 2 → ℝ := ![1, -1]
    ∑ i, (0 + (1/2) * momentumStepRatio 1 (1/2) (F i) 0 0 / mass i) = 0 := by
  norm_num [momentumStepRatio, Fin.sum_univ_two]

end ActuationMotionNeg
