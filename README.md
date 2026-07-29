<h1>Prelude</h1>
<p>Hi I just want to say few words about the project to make a little more clear as to what I did. 
  This is a full-stack web application that utilizes an ai engine to help users rationalize their decisions. 
  It was my first time building an ai and creating its own state persistence so please by gentle 😅.
</p>

<p>
  When I first started thinking of projects to create, it was very difficult. 
  I was in the headspace of making somethign that other people want and need. How would I know what people that I do not know need? huh.
  I didn't stop to think of what I found 
  interesting and what problems that I wanted to solve. Problems that were close to heart and I had direct experience with. 
  Once such problem wass the decision 
  making process. Like many others, I find myself decisive at many times. Not knowing if a certain path is what I ultimately 
  want. Sure I have made decisions that, at the time, I was sure I wanted/needed, but even those came with regrets. Not knowing what is 
  unknown can be so dangerous at times, especially when it is comes to the unknowns about ourselves. There is something I find interesting
  in the human struggle to
  remain aware, or even knowing, of the moments we are making a mistake. Mistake is probably not the best word, as it is too vague.
  What I mean is the moments in which we are not staying true to the person we are or want to be. There is a quote that has always
  stuck with me from one of my favorite books of the Licanious Trilogy that has guided by decision making in times of distress 
  - "Be the man you aspire to be".
  What would that man do?
</p>

<p>
  When making decisions, one popular method that some people choose to use is to make a pros and cons list.
  Although there is nothing wrong with this (I myself used this a ton of times), I've become accustomed to problems 
  associated with it. In my view, this doesn't truly speak or give justice to the person's beliefs or values in its entirety.
  In order to do so, it would need to be a very long list as we are all complex beings. You couldn't possibly have the time
  to analyze yourself, your life, and come up with a true list irrespective of superficiality. To list everything, all the possible
  tangible and not so tangible benefits, and then weigh them all.
  We are just too complex in order for this to be possible. Our complexity cripples us in the decision making process
  and creates situation in which people believe they are more capable than they actually are.
</p>

<p>
  All this begs the question, What is the wrong choice? For the purposes of this project, and my life; a decision that ultimately leads
  you to stray away from your core beliefs and values is inherently a wrong choice. I know that I touched
  on the popular pros and cons list (and its denominations), but I would like to speak a little to those who believe they make their decisions
  off of what they are feeling. Those who you who "listen to your heart" as they say 😄. What does this actually mean?
  All of our emotions and feelings that we get due external stimuli is a based off of the worldview of the person.
  This includes all of the core values, habits, philosophies, etc that they have. To put simply, you cannot be sad about murder if you don't
  believe that murder is wrong in the first place. In my opinion, making decisions off of feel like is winging a presentation. 
  Sometimes you'll kill and sometimes you'll fall on your face. Sometimes you'll marry your soulmate, sometimes you'll marry someone who isn't
  Its always bad to do so, but when you look at it from that lens, it seems a bit unreliable.
</p>

<h3><strong>What does this mean for the project?</strong></h3>
<p>
  This project aims to solve the challenge in understanding ourselves in order to aid in the decision making process.
  It does this by having an ai learn about user through text conversation. The ai will then be able to reason decisions out for the user
  in order to help them stay morally consistent and true to themselves. 
</p>

<h1> Here is a look of what the web application of this project looks like</h1>
<img width="1436" height="811" alt="Screenshot 2026-07-28 at 3 14 53 PM" src="https://github.com/user-attachments/assets/6a1bfcc3-fe09-497d-88b3-656263d55f26" />


<h1> Tech Stack</h1>
<ul>
  <li>React.js,CSS for the front end development UI</li>
  <li> Python for backend development</li>
  <li> FASTAPI web framework for building backend API endpts</li>
  <li> OPENAI API ChatGPT-mini model </li>
  <li> .json files for data storage </li>
  
</ul>

<h1> About the Project (How it works)</h1>
<h3>Under the hood</h3>
<p>
  The way this project works is by wrapping an OPENAI ai model and manually keeping track of data persistence. The ai has no state management, so the ai's memory and purpose has to be built manually. This is done by prompting and having specific files that are fed into the ai with instructions.  There are 3 primary data collections that I am using to make this application work. The first I will talk about is profile.json. This file keeps the key value pairs of all of the attributes/characteristics of the person. This includes core values, interests, hobbies, etc.. The next file or files is chat_log.txt. These files store conversations of all the sessions. When a conversation balloons the chat_log.txt to a certain size. A new file is created for the next session, leaving the old file to be named archive_log.txt. Lastly, there is summary.json. This is meant to be the long term memory of the model. This file contains the higher level overview of each conversation/session that a user has with the model. This means that it tracks the milestones and import parts of a user's life. It is updated at the end of each session with all logs of the current conversation, so that not all conversations ever recorded have to be fed into the OPENAI api call. With regards to real time conversation, the profile.json is fed into the OPENAI api call so that the query has the instructions on how to reason with the user by using the profile.json as a reference. This file is then updated at the end of the session similarly to summary.json so that it is up to date.
</p>
<h3>The applicaton</h3>
<p> 
  So for simplicity sake to get a user facing prototype I chose to opt for a web based "deployment".
  I also went for a web build because I wanted to teach myself React, so I just used this project idea as a way to
  learn React. The UI is pretty straight forward. The only interactables are the chat bar, the send button, and then the right side panel
  buttons. The chat bar allows you to chat inside of the chat window of course, and the right viewing panel shows what information
  the ai has of you stored on the server.
  
  Notes: So because I didn't really see this being used by other people I've omitted a couple things I would have otherwise implemented. Right now the profile.json is hard coded template of me with a few base values. If this was a real deployment for a 
  product I would allow the user to customize the starting template and to reset any data that the ai has on either or all of the 3 file system. This is mainly why I have the settings/profile vertical bar to the left. The idea was for the user to click settings for something like color preference and have the profile icon for customizing app specific stuff.
</p>


<h3>Closing word</h3>
<p>
  Well that is all I have to say and I think I have covered everything there is to know from start to finish
  about this project. If there is anything more that is needed to know please do not hesitate to ask me. I do see this as a completed work, so I will be moving on other projects that I have in mind. I will mostly not be coming back here unless it is to reference something or build ontop of something else. This project idea came from something bigger and better that I wanted to create, but I am not yet at the level or knowledge to do so. I see 
  this is as a stepping stone in that direction. It's not a perfect system/ai, but I think it speaks to the ongoing process that facilitates self betterment. Self-betterment only ever happens gradually. Einstein didn't become Einstein overnight. Arnold didn't become Arnold after one workout. Self betterment and change in general happens incrementally. I see myself as a reflection of researchers worldwide that are continuously going through iterations of work to achieve the bigger and better breakthroughs. At least, thats what I like to think anyways. whenever I am feeling down about my abilities or whenever I am longing to be better. I know many of you are not going to every read this.  In fact, I am guessing maybe 1 person actually reads any of this, but I very much appreciate all of those that do take the time to do so. 
  
Note: Journalng may have recently affected me, so I apologize for the style of this ReadMe.I do not normally write in a blog like fashion this, so maybe I'll delete it later. There is a fine like between being "professional" or "proper" and being me, and sometimes I just like to be me at whatever cost. Also, I think it's just nice to have the ability to speak to both no one and everyone at the same time. Bye all 😊
</p>
