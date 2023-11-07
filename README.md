# whats-in-my-fridge
Flask app for tracking and checking what's in your fridge, when it expires, and what you can make with what's not expired in your fridge.

## Team Roster
Thomas Delgado - Developer 

Pierre-Alex Journes - Developer

Dena Murr - Developer + Scrum Master

Ivan Solovyev - Developer

Lester Leong - Developer + Product Owner

Scott M - Developer

## Schedule
Standup Monday after class
Sprint planning Wednesdays at 6pm EST

### Stakeholders
* Caroline Mak
* Thomas Delgado
* Dena Murr

We believe in "dogfooding" our work. In particular, this project was born of the desire of Thomas' partner, Caroline, for a more ergonomic system for tracking the contents of their fridge and freezer. Accordingly, Thomas and Caroline are stakeholders in this project, and will be testing it at home and providing feedback. Dena, as one of our developers specializing in UI/UX, will also be part of this effort. 

We generally believe this project will be suitable for anyone who is forgetful, or simply too busy to keep track of what's in their fridge or freezer.


## Far Vision
We envision a future where:
* You have 100% visibility into the contents of your fridge,
* You always know what you can make with what you have on hand,
* And where food waste because those leftovers got buried in the back of the fridge is a thing of the past

## Near Vision
As our first step towards transforming the refrigerator experience, we are going to develop a web app in Flask that:
* Empowers users to enter items they want to keep track of, along with their expiration dates
* Allows users to mark when they threw out or consumed an item, and tracks that info
* Displays to users a filterable and sortable list of their fridge's contents, including expiration dates
* Allows users to enter (the ingredients that go into) recipes
* Allows users to see what recipes they can or cannot make with the food they have on hand
* Displays alerts for soon-to-expire foods
* Possibly produces .ics / emacs org-mode files for putting expiration dates on your gcal
* Maybe allows multiple users to log in?

## Who is this for? (Stakeholder types)
We think this project is suitable for most everyone with a fridge, including:
* forgetful people
* busy people
* people with lots of stuff in fridge
* people who cook a lot
* people who dislike food waste??

## Project Management Notes

Backlog link - <https://miro.com/app/board/uXjVNU4Q6oo=/?share_link_id=601517274408>

### Rationale for ordering project backlog
We order the items in our product backlog first by the value we expect they will deliver to our stakeholders, and then by the order in which they need to be done. (e.g., if PBI A depends on PBI B to be done, then we list B first, then A, assuming they have the same value to our stakeholders.) 

### Definition of Ready
We consider a product backlog item ready when:
* It has a title
* The user story has at least an opening sentence
* Acceptance criteria have been enumerated
* The story has been estimated using story points
* Additional details are filled out as needed, possibly including:
    * Developer tasks
    * Plan of execution
 
### User Persona
As part of our development process, we performed an initial interview with stakeholder CM, and constructed a user persona from her input, which can be found [here]
(https://docs.google.com/document/d/1qXMOOKYEAWKNkg7sG3r7SIuSYhcEVEM7Kuf6qchsjVU/edit?usp=sharing).
 
### Other notes
To generate our initial backlog estimates, we used the estimation method "big uncertain small", as found here: 
<https://www.parabol.co/blog/agile-estimation-techniques/>
We then further refined our estimates and assigned story points by going through our backlog as a team in a manner similar to "magic estimation" (see same link above).

Only developers participate in our PBI estimates.
