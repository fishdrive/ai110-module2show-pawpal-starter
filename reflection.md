# PawPal+ Project Reflection

## 1. System Design

//Three core actions that I would add. First would be to schedule daily walks for the pet. Then, the owners would be able to add scheduled grooming appointments their animals needs. Lastly, the owner would need to be able to add a pet in order for this app to work. 


//I included 4 different classes. This included the owner class, pet class, task class and scheduler class. The owner class included information about the owner and their preferences and avalibilty for the pet. The pet class listed the pet and all of the information necessary for this pet: ex.. weight, health information. The task class included tasks and how it related to the pet. Lastly the scheduler class included the plans and what times they were being scheduled. 

//I did not make any design changes

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

//My scheduler has a nested scan that makes it easier to report every conflicting pair, which is necessary when many tasks can overlap. However, sorting intervals and comparing tasks would be simpler and faster, but doesn't account for when many tasks overlap. This tradeoff is fine because comparing tasks could miss conflicts when I need all warnings. 


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
