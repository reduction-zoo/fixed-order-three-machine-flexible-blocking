import Challenge
open FixedOrderThreeMachineFlexibleBlocking
example : targetWitness ([⟨1,[(1,100)],1,[],1⟩],4) [(1,0)] = true := by native_decide
example : targetWitness ([⟨1,[(1,100)],1,[],1⟩],4) [(0,0)] = false := by native_decide
example : targetWitness ([⟨1,[],1,[],5⟩,⟨1,[],1,[],1⟩,⟨1,[],1,[],1⟩],9) [(0,0),(0,0),(0,0)] = true := by native_decide
