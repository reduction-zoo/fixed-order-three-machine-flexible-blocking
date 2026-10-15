module

public import Mathlib.Computability.TuringMachine.Computable

@[expose] public section

namespace FixedOrderThreeMachineFlexibleBlocking

/-- Q001's self-delimiting binary natural; length is logarithmic, not unary. -/
def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeOption {α : Type} (encode : α → List Bool) : Option α → List Bool
  | none => [false]
  | some x => true :: encode x

/-- None denotes mathematical nonexistence, never an execution error. -/
def searchOutput {I W : Type} (legal : I → Bool) (witness : I → W → Bool)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w = true
  | none => legal x = true ∧ ¬ ∃ w, witness x w = true

/-- Relational version for witnesses with quantified real or optimality conditions. -/
def relationalOutput {I W : Type} (legal : I → Bool) (witness : I → W → Prop)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w
  | none => legal x = true ∧ ¬ ∃ w, witness x w

def legalSource (x : List Nat) : Bool := x.all (fun w => w > 0)

def sourceWitness (x : List Nat) (subset : List Nat) : Bool :=
  decide subset.Nodup && subset.all (fun i => i < x.length) &&
  2 * (subset.map (fun i => x[i]?.getD 0)).sum == x.sum

def encodeSource := encodeList encodeNat

def validSourceOutput := searchOutput legalSource sourceWitness

structure Job where
  first : Nat
  firstFlexible : List (Nat × Nat)
  second : Nat
  secondFlexible : List (Nat × Nat)
  third : Nat
  deriving Repr
abbrev Instance := List Job × Nat
def legalTarget (x : Instance) : Bool := x.1.all (fun j =>
  j.first > 0 && j.second > 0 && j.third > 0 &&
  (j.firstFlexible ++ j.secondFlexible).all (fun p => p.1 > 0 && p.2 > 0))
def durations (j : Job) (splits : Nat × Nat) : Nat × Nat × Nat :=
  (j.first + ((j.firstFlexible.take splits.1).map Prod.fst).sum,
   j.second + ((j.firstFlexible.drop splits.1).map Prod.snd).sum + ((j.secondFlexible.take splits.2).map Prod.fst).sum,
   j.third + ((j.secondFlexible.drop splits.2).map Prod.snd).sum)
def advance (prior duration : Nat × Nat × Nat) : Nat × Nat × Nat :=
  let secondStart := max (prior.1+duration.1) prior.2.1
  let thirdStart := max (secondStart+duration.2.1) prior.2.2
  (secondStart,thirdStart,thirdStart+duration.2.2)
def targetWitness (x : Instance) (splits : List (Nat × Nat)) : Bool :=
  splits.length == x.1.length && (x.1.zip splits).all (fun (j,s) => s.1 ≤ j.firstFlexible.length && s.2 ≤ j.secondFlexible.length) &&
  (((x.1.zip splits).map (fun (j,s) => durations j s)).foldl advance (0,0,0)).2.2 ≤ x.2
def encodeTarget (x : Instance) :=
  encodeList (fun j => encodeNat j.first ++ encodeList (fun p => encodeNat p.1 ++ encodeNat p.2) j.firstFlexible ++
    encodeNat j.second ++ encodeList (fun p => encodeNat p.1 ++ encodeNat p.2) j.secondFlexible ++ encodeNat j.third) x.1 ++ encodeNat x.2
def encodeWitness := encodeList (fun p : Nat × Nat => encodeNat p.1 ++ encodeNat p.2)
def validTargetOutput := searchOutput legalTarget targetWitness

/-- Both algorithms use Q001's explicit bit encoding and TM2 cost model.
Recovery receives the full pair of source instance and target output. -/
def Reduction (forward : (List Nat) → Instance)
    (recover : (List Nat) × Option (List (Nat × Nat)) → Option (List Nat)) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeSource encodeTarget forward) ∧
  Nonempty (Turing.TM2ComputableInPolyTime
    (fun input => encodeSource input.1 ++ (encodeOption encodeWitness) input.2)
    (encodeOption (encodeList encodeNat)) recover) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeTarget (forward x)).length ≤ bound.eval (encodeSource x).length) ∧
  (∃ bound : Polynomial Nat, ∀ input,
    ((encodeOption (encodeList encodeNat)) (recover input)).length ≤
      bound.eval (encodeSource input.1 ++ (encodeOption encodeWitness) input.2).length) ∧
  (∀ x, legalSource x = true → legalTarget (forward x) = true) ∧
  (∀ x, legalSource x = true → ∀ y, validTargetOutput (forward x) y →
    validSourceOutput x (recover (x, y)))


def Goal : Prop :=
  ∃ (forward : (List Nat) → Instance)
    (recover : (List Nat) × Option (List (Nat × Nat)) → Option (List Nat)), Reduction forward recover

/-- Open question only; this placeholder is not a solution. -/
theorem solve : Goal := by
  sorry

end FixedOrderThreeMachineFlexibleBlocking
