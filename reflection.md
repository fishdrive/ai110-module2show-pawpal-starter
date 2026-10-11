# PawPal+ Project Reflection

## 1. System Design

//Three core actions that I would add. First would be to schedule daily walks for the pet. Then, the owners would be able to add scheduled grooming appointments their animals needs. Lastly, the owner would need to be able to add a pet in order for this app to work. 


//I included 4 different classes. This included the owner class, pet class, task class and scheduler class. The owner class included information about the owner and their preferences and avalibilty for the pet. The pet class listed the pet and all of the information necessary for this pet: ex.. weight, health information. The task class included tasks and how it related to the pet. Lastly the scheduler class included the plans and what times they were being scheduled. 

//I did not make any design changes

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

//My scheduler had to consider task priority, deadlines, duration, completion status, and the owner's daily time budget. I prioritized high-priority tasks and earlier deadlines while keeping the plan within the time budget. A constraint is that owner preferences are stored but are not currently used by the scheduling algorithm.

**b. Tradeoffs**

//My scheduler has a nested scan that makes it easier to report every conflicting pair, which is necessary when many tasks can overlap. However, sorting intervals and comparing tasks would be simpler and faster, but doesn't account for when many tasks overlap. This tradeoff is fine because comparing tasks could miss conflicts when I need all warnings. 


---

## 3. AI Collaboration

**a. How you used AI**

//I used AI for advice on the third type of algorithm I wanted to create. It also helped me clean up all of my code into something more neat and readable. It helped me debug some of my code and clean up the overall UI. The types of prompts that were most helpful for me were prompts like, "How could I make so and so better without fully changing the idea?". 


**b. Judgment and verification**

//When I asked Ai for some methods that might useful for a specific class, I got a few that seemed redundant. I did not directly add all of the suggested methods it wanted. I re-evaluated by only adding the ones that seemed important to me. 

---

## 4. Testing and Verification

**a. What you tested**

I tested that pets and tasks stay connected correctly when tasks are added or removed and that an owner can collect tasks across their pets. I tested multiple types of completion, including creation of the next recurring task and prevention of duplicate occurrences. I also tested priority-based scheduling within the owner's time budget, chronological deadline sorting, pet workload ranking, filtering by pet/type/status, and conflict warnings for overlapping tasks and budget overruns.

These tests were important because they check the relationships and scheduling rules the app relies on. They help catch errors such as losing a task when it is reassigned, repeating a task incorrectly, scheduling more care than the owner has time for, or failing to warn about overlapping appointments. The tests also verify edge cases like undated tasks, completed tasks, and future-due tasks so the plan is more dependable.

**b. Confidence**

//I'm very confident my scheduler works well. 
//If I had more time, I would test a task that fills multiple types of time budgets, including daily and a long task being skipped while a shorter task executes. I would also verify that completed and future-due tasks are excluded from today's plan, that back-to-back tasks or a task ending exactly at its deadline do not produce false conflict warnings, and that recurring tasks continue correctly across month or year boundaries.

---

## 5. Reflection

**a. What went well**

//I was happy that this project didn't have too many hiccups. Most of the directions I gave to the agent were clear and worked well in terms of getting things properly done. Overall, this project worked well with my vision for it. 

**b. What you would improve**

//I believe in this project, we had a sort of rubric we had to follow that made it a bit more simple to construct this application. In the future, I'd like to try something independently to see how I would do without direct commands to help me build something properly. 

**c. Key takeaway**

//In this project, something important I learned was making sure AI was properly working based off of my creative direction. Whilst something technically worked, it wasn't the result I wanted which meant I had to do it again. One of the most important things about working with AI is making sure it can properly display your vision. 

