# **Unsupervised Discovery of Steering Vectors**

# **Executive Summary ([Code](https://github.com/fringewidth/steer-clear))**

Searches for steering vectors are often confirmatory: we find “honesty” or “politeness” vectors only because we know to look for them. This work introduces an unsupervised method to discover interesting, steerable behaviours directly from the activation space. I trained 20 LoRAs on Qwen1.5-14b-instruct, out of which five correspond to linear, steerable, and interpretable vectors. I used a modified LLM-as-a-judge method to strictly quantify how well a LoRA corresponds to the extracted linear vector.

## **High-Level Takeaways**

- We can force a model to explore new behaviours by training LoRAs on every block with a modified KL-divergence loss.
- A fair amount of these LoRAs (25%) correspond to linear, interpretable vectors that can be extracted using mean activation differences.
- There are cases where a trained LoRA induces an interpretable behaviour, but does not reduce to a clean linear vector.
- Some converged vectors are linear combinations of separate interpretable vectors. These vectors induce interesting outputs when scaled negatively.
- All tested vectors have the same optimal window for scaling, outside of which the outputs are gibberish.

## **Methodology: How to search for vectors?**

- To induce behaviours without supervision, I trained 48 rank-2 LoRA adapters (one per layer) to generate unique answers to input prompts.
- The prompts were designed to minimise the assistant-like nature of the model and instead encourage unfiltered and honest thoughts (e.g., “Drunk Friends at 3 AM”, “Anonymous Forum Comments”)
- The LoRAs were trained via AdamW for a single epoch with a modified KL Divergence loss:

L \= \-KL(P || Q) \+ NLL(Q, sample(Q))  
where _P_ is the base model output, and _Q_ is the fine-tuned model output.

- The KL Divergence term pushed the finetuned model away from the baseline.
- The NLL is computed between the output probs (_Q_) and a one-hot vector sampled from _Q_.
- This prevents the model from producing gibberish by encouraging more confident predictions.
- For training, I set α \= 1.1 and β \= 0.3. A learning rate of 0.1 worked best.
- The vector v of the LoRA was calculated by the mean activation difference:  
  v \= mean(actLoRA-actbaseline)

## **Measuring Success: Linearity of the LoRA**

- I ran 20 fine-tunes against 96 unseen prompts. I then used Gemini 2.5 Flash to compare these outputs to the baseline. By processing these in random batches, I generated 6 distinct textual summaries per LoRA describing exactly how the behaviour shifted (e.g., “more assertive”, “avoids pleasantries”).
- I repeated this entire process, but replaced the LoRA adapters with the corresponding extracted steering vectors. This resulted in a second set of 6 behavioural summaries.
- To compare these two sets of descriptions, I built a cosine similarity matrix between the LoRA summaries and the vector summaries.
- Since a single model often exhibits multiple sub-behaviours, I treated this as an assignment problem. I used the Hungarian algorithm to find the optimal pairings between the LoRA and vector descriptions.
- The linearity score is the normalised sum of these best-match similarities. This effectively measures how much of the original fine-tuned behaviour survived the transition into a linear steering vector.
- **Linearity Scores** ranged from **\~0.71 to \~0.86** across 20 vectors.
- The top 5 vectors (25%) showed strong alignment with their LoRAs. Among these 5:
  - 3 vectors were cleanly steerable, corresponding to distinct concepts:

1. A **“follow-up question”** vector
2. A **“preachiness”** vector
3. An **“empathy”** vector.
   - One vector was labelled as “adds a third character to the conversation” by Gemini. I found that when the vector scaled negatively, it reliably generated **alliterative and poetic** text.
   - The remaining vector revealed itself as an AI significantly more than the baseline, a property consistent with both the LoRA and the vector finetunes.

## **Experiments: Validation of Steering Effectiveness**

All three experiments show a similar optimal window for the vector scales, and a high degree of agreement with their qualitative interpretation.

### **Experiment \#1: Counting Question Marks in the “Follow Up Question” Vector on the test dataset.**

- As I increased the scaling factor, the number of questions asked increased as well, beating the baseline at scale \= 1\.
- The anomaly at scale \= 7 is caused by the model going on a ramble, asking questions in a continuous stream without ever generating a ‘?’ token in some cases.

### **Experiment \#2: Pitting the Baseline against the Empathy Vector**

- I tested the Empathy vector using 28 prompts categorised into three levels of required empathy (none, medium, high).
- The baseline and the steered model were run against these prompts, and Gemini 2.5 Flash acted as a blind judge to determine which response exhibited more empathy.

### **Experiment \#3: Pitting the Baseline against the Preachiness Vector**

- The Preachiness vector was evaluated using the same methodology as the empathy test.
- Like the other experiments, the degradation in output quality beyond scale=4 caused the steered model to be rated lower than the baseline.

# **Details**

## **Details on Training and Loss Function**

- To induce a behavioural change from which I can extract vectors, I use 48 rank-2 LoRA adapters, one attached to each transformer block of Qwen1.5-14B, trained with AdamW.
- The approach relies on a modified loss. I first used negative KL divergence to push the finetuned model’s probabilities away from the baseline. This worked, but as expected, the model collapsed into gibberish by spreading probability mass too evenly across tokens. To fix it, I added an auxiliary NLL term on the model’s own sampled token, which encouraged sharper, more confident predictions while still differing from the base.
- The LoRAs are trained with a [dataset of generic prompts](https://github.com/fringewidth/stupid-search/blob/master/datasets/scenarios_cleaned.csv) that attempt to minimise the assistant-like nature of the pretrain and instead encourage unfiltered and honest thoughts. Here is one example:![Drunk Friends at 3AM: Two close friends who've been drinking, inhibitions are down, and they're having one of those raw, honest conversations that only happen when alcohol removes the social filters.Friend1: What's the worst thing you've ever done that no one knows about?Friend2:][image1]

- Remarkably, the LoRAs converged to well-discernible behaviours after just one epoch, consisting of 384 prompts and a maximum of 128 generated tokens.
- This work uses the same method as [Panickssery](https://arxiv.org/abs/2312.06681) et al. for extracting a vector from LoRAs of rank 2 and above, viz., train a LoRA and compute the mean activation difference between the finetuned and base model. I compute _`mean(act_lora - act_base)`_ for each transformer block over all prompts (both test and train).

## **Details on the Linearity Score**

- Simple metrics such as WordClouds and differences in embedding vectors were not general enough. I used LLM-based evaluation to create a linearity score.
- I ran the 20 finetunes on [96 unseen prompts](https://github.com/fringewidth/stupid-search/blob/master/datasets/test.csv). I then sent Gemini 2.5 Flash each of the 96 answers with the baseline as reference. I did this in six randomly sampled batches, giving me [6 textual summaries](https://github.com/fringewidth/stupid-search/tree/master/outputs_interp/phase1) per LoRA describing deviations from baseline.
- I repeated the process after replacing the LoRAs with the corresponding external vectors, generating a second set of summaries.
- I generated a cosine similarity matrix between both sets. Each summary may describe a different behaviour, so I had to match each summary in the LoRA set with one in the vector set. This is the assignment problem, so I used the Hungarian algorithm to find the optimal pairing.
- The normalised sum of best-match similarities gave the final linearity score, showing how well the linear vectors captured the original behaviour.

## **Discussion of the Results**

The **25% success rate** was not the universal method I hoped for, but achieving it when discovering complex, steerable concepts from an unsupervised search was surprising. This suggests a high density of linear behaviours in the activation space, so even simple optimisation reveals them. (Not surprising in hindsight.)

The **poetic/alliterative behaviour** is an important consequence of the method. _Extracted vectors can be linear combinations of several linearly encoded behaviours._  
I suspect the vector v may be `v ≈ w₁ * v_character - w₂ * v_alliteration, where w₂ >> w₁`. At positive scales, the `v_character` effect dominates. At negative scales, the `-w₂ * v_alliteration` term reverses, activating a latent alliterative/poetic style which was otherwise suppressed. I hope to validate this in a future project. A similar effect may occur when ablating the preachiness vector, causing an almost motherly love, perhaps the opposite of preachy advice. That’s open to interpretation. Philosophically, whether a vector is a “pure concept” or a “linear combination” is human-defined, indistinguishable to the model.

The vector that shows itself as more AI-like than the baseline but doesn’t generalise well may be due to the data. The “situations begetting honesty” prompts likely helped escape the model’s assistant-like behaviour, but train and test shared scenarios with different prompts, which may not be ideal. A better dataset might yield higher success with fewer non-generalizable behaviours. I did not have time to run ablations here.

One surprising result was a LoRA finetune that became brash and rude almost universally, yet its vector scored only 0.80 in linearity and could not replicate this behaviour. This was unexpected. Perhaps some subtle misalignments are expressed non-linearly? I want to explore this further.
