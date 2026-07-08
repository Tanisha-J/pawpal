# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
- Briefly describe your initial UML design.
        - should be able to add pet, see timings for walk, create task list for day
- What classes did you include, and what responsibilities did you assign to each?
        - task: name of task and duration in minutes
        - pet: name of pet, breed of pet, age of pet
        - owner: name of owner and available time
        - plan: owner name, pet name, leftover time, tasks list

**b. Design changes**

- Did your design change during implementation?
        - yes 
- If yes, describe at least one change and why you made it.
        - it changed because i included the leftover time so the owner knows how long they have during the day and how long will taking care of their pets will take 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
        -time
- How did you decide which constraints mattered most?
        - i believed time mattered most because it was the owner doing the work so they should know how much time to block out for their pet

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
        - if the tasks go overtime, it shows that instead of deleting it based on priority
- Why is that tradeoff reasonable for this scenario?
        - the tasks here are already important for the pet so you should know how much time to allocate for your pet instead of deciding importance for it 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
        - helped me brainstorm what are the most useful classes and shortlisted
        - had it create the uml diagram
        - tested the main.py 
- What kinds of prompts or questions were most helpful?
        - creating the classes
        - asking what specific commands and extensions were used for 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
        - it told me to just run pytest and since it didn't work so it wanted me to import new things and make it more complicated with conftest.py
- How did you evaluate or verify what the AI suggested?
        - i verified using the instructions and knew that i probably didn't need to do that so i copy-pasted the instructions and asked if it was a better approach and it agreed

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
        - marking a test as done
        - adding a task to a pet
        - sorting with duration
        - split tasks into completed and pending
        - making sure there is no overlap for recurring tasks
        - more described in README
- Why were these tests important?
        - these tests were important because it ensures all the data flows correctly and an owner can use this app to create a schedule for their pet 

**b. Confidence**

- How confident are you that your scheduler works correctly?
        - i am 80% confidence
- What edge cases would you test next if you had more time?
        - i would test to make sure everything can be edited and updated in real time 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
        - i am most satisifed with the classes and uml diagram because it shows what the program can/may do

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
        i would make sure it can edit everything in real time


**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
        - i learned that it is important to have a plan for AI to do 
